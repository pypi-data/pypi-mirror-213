import numpy as np
from concurrent.futures import ProcessPoolExecutor

from scipy.spatial import distance
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from fast_histogram import histogram2d
import colorcet as cc

import seaborn as sns

def make2DHistogram(im0,im1,nbins):
    """
    Compute a 2D histogram from two input images.

    Args:
        im0 (ndarray): First input image.
        im1 (ndarray): Second input image.
        nbins (int): Number of bins for the histogram (same in both dimensions).

    Returns:
        tuple: A tuple containing the following elements:
            - H (ndarray): The 2D histogram.
            - ie (ndarray): Bin edges for the first input image.
            - je (ndarray): Bin edges for the second input image.

    Notes:
        - The function computes a 2D histogram by binning the pixel values of `im0` and `im1`.
        - The `nbins` parameter controls the number of bins to use in each dimension.
        - The range of the histogram bins is determined by the minimum and maximum values of the input images.
        - The computed histogram `H` represents the joint distribution of pixel intensities between `im0` and `im1`.
        - The `ie` and `je` arrays contain the bin edges corresponding to the first and second input images, respectively.
    """

    minval = min(im0.min(),im1.min())
    maxval = max(im0.max(),im1.max())+1 #to catch the last bin
    binrange = [(minval,maxval),(minval,maxval)]
    H=histogram2d(im1.flatten(),im0.flatten(),bins=nbins,range=binrange) #im0 on x im1 on y
    #bin centers
    ie = np.linspace(minval,maxval,num=nbins+1)
    je = np.linspace(minval,maxval,num=nbins+1)
    ic = computeBinCenters(ie)
    jc = computeBinCenters(je)
    return H, ic, jc

def computeBinCenters(edges):
    return (edges[1:] + edges[:-1])/2

def _paintParallel(args):
    im0_chunk, im1_chunk, labels, ic, jc = args
    segmented = np.zeros(im0_chunk.shape)
    for sl, (i0, i1) in enumerate(zip(im0_chunk, im1_chunk)):
        bi = np.digitize(i1, ic, right=True) 
        bj = np.digitize(i0, jc, right=True)
        bj = np.where(bj == bj.max(), bj.max() - 1, bj)  # Extend the last bin
        bi = np.where(bi == bi.max(), bi.max() - 1, bi)
        for ii in range(im0_chunk.shape[1]):
            for jj in range(im0_chunk.shape[2]):
                segmented[sl, ii, jj] = labels[bi[ii, jj], bj[ii, jj]]
    return segmented

def paintVolume(im0, im1, labels, ic, jc, slicenr=None, nprocs=1):
    """
    Apply segmentation labels to a volume based on 2d histogram labelling.

    Args:
        im0 (ndarray): First input image volume.
        im1 (ndarray): Second input image volume.
        labels (ndarray): Segmentation labels.
        ic (ndarray): Bin centers for the first image.
        jc (ndarray): Bin centers for the second image.
        slicenr (int, optional): Slice number to segment. If specified, only the slice with this index will be segmented.
        nprocs (int, optional): Number of processes to use for parallel execution. Default is 1.

    Returns:
        ndarray: Segmented volume based on the given image and intensity thresholds.

    Raises:
        ValueError: If the specified slicenr is out of range.

    Notes:
        - The function segments a volume by assigning labels from the `labels` array based on intensity thresholds.
        - If `slicenr` is provided, only that particular slice is segmented, and a 2D segmented slice is returned.
        - If `slicenr` is not provided, the function segments the entire 3D volume in parallel using multiple processes.
          The `nprocs` parameter controls the number of processes to use.
    """
    if slicenr is not None or im0.ndim==2:
        # Only paint one slice
        if slicenr is not None:
            im0 = im0[slicenr]
            im1 = im1[slicenr]
        segmented = np.zeros(im0.shape)
        bi = np.digitize(im1, ic, right=True)
        bj = np.digitize(im0, jc, right=True)
        bj = np.where(bj == bj.max(), bj.max() - 1, bj)  # Extend the last bin
        bi = np.where(bi == bi.max(), bi.max() - 1, bi)
        for ii in range(im0.shape[0]):
            for jj in range(im0.shape[1]):
                segmented[ii, jj] = labels[bi[ii, jj], bj[ii, jj]]
        return segmented

    n_elements = im0.shape[0]
    chunk_size = (n_elements + nprocs - 1) // nprocs
    chunks = [(im0[i * chunk_size:min((i + 1) * chunk_size, n_elements)],
               im1[i * chunk_size:min((i + 1) * chunk_size, n_elements)],
               labels, ic, jc) for i in range(nprocs)]

    with ProcessPoolExecutor(nprocs) as executor:
        results = list(executor.map(_paintParallel, chunks))
    segmented = np.concatenate(results, axis=0)
    return segmented

def subtractive_mountain_clustering(ra, rb, eps_u, eps_b, threshold, histogram, plot=True):
    """
    Perform subtractive mountain clustering on a 2D histogram.

    Args:
        ra (float): Parameter controlling the width of the influence region for the cluster centers.
        rb (float): Parameter controlling the width of the influence region for reducing potential near existing cluster centers.
        eps_u (float): Threshold ratio for accepting a potential point as a cluster center.
        eps_b (float): Threshold ratio for rejecting a potential point as a cluster center.
        threshold (float): Threshold value for considering a histogram bin as a potential point.
        histogram (ndarray): 2D histogram array representing the data.
        plot (bool): Whether to plot the potential map and cluster centers.

    Returns:
        tuple: A tuple containing the following elements:
            - nclusters (int): The number of clusters found in the histogram.
            - centers (ndarray): An ndarray containing the coordinates of the cluster centers.

    Notes:
        - The subtractive mountain clustering algorithm aims to find clusters in the given histogram.
        - The `ra` parameter controls the width of the influence region for the cluster centers.
        - The `rb` parameter controls the width of the influence region for reducing potential near existing cluster centers.
        - The `eps_u` and `eps_b` parameters determine the threshold ratios for accepting and rejecting potential points as cluster centers, respectively.
        - The `threshold` parameter defines the value threshold for considering a histogram bin as a potential point.
        - The `histogram` parameter is a 2D ndarray representing the data to be clustered.
        - The `plot` parameter specifies whether to visualize the potential map and cluster centers.
        - The function returns a tuple containing the number of clusters and their coordinates.

    """
    alpha = 4 / (ra ** 2)
    beta = 4 / (rb ** 2)

    r_coords, c_coords = np.meshgrid(range(histogram.shape[0]), range(histogram.shape[1]),indexing='ij')
    coordinates = np.column_stack((r_coords.flatten(), c_coords.flatten()))
    data = histogram.flatten()
    idx = np.where(data >= threshold)

    Pi = np.zeros(histogram.shape[0] * histogram.shape[1])
    centers = []

    distances = distance.cdist(np.array(coordinates), np.array(coordinates[idx]))
    for i, cdist in enumerate(distances):
        Pi[i] = np.sum(np.exp(-alpha * np.square(cdist)))

    ii = np.argmax(Pi)
    centers.append([coordinates[ii][0], coordinates[ii][1]])
    Pstar = Pi[ii]
    retstat = 1
    while retstat > 0:
        dist_cen = distance.cdist(np.array(coordinates), np.array(centers[-1:]))
        ii = np.argmax(Pi)
        Pks = Pi[ii]
        for i, cdist in enumerate(dist_cen):
            Pi[i] -= Pks * np.exp(-beta * np.square(cdist))
        retstat,centers,Pi = _selection_criteria(coordinates,centers,Pi,Pstar,eps_u,eps_b,ra)
        
    centers = np.array(centers)
    nclusters = centers.shape[0]
    if plot:
        plt.figure()
        plt.imshow(Pi.reshape(histogram.shape), origin='lower')
        plt.scatter(centers[:, 0], centers[:, 1], marker='o')
        plt.show()

    return nclusters, centers

def _selection_criteria(coordinates,centers,Pi, Pstar, eps_u,eps_b,ra):
    retstat = 2
    while retstat == 2:
        ii = np.argmax(Pi)
        Pks = Pi[ii]
        if Pks > eps_u * Pstar:
            centers.append([coordinates[ii][0], coordinates[ii][1]])
            retstat = 1 #found an acceptable cluster
        elif Pks < eps_b * Pstar:
            retstat = 0 #no more clusters
        else:
            ds = distance.cdist(np.array(centers), np.array([coordinates[ii]]))
            dmin = np.min(ds)
            if dmin / ra + Pks / Pstar >= 1:
                centers.append([coordinates[ii][0], coordinates[ii][1]])
                retstat = 1
            else:
                Pi[ii] = 0
    return retstat, centers, Pi





def kmeans_clustering(H, kcentroids, threshold=0, plot=False, verbose=False, return_cmap=False, maxiter=30):
    """
    Performs k-means clustering on a 2D histogram.

    Args:
        H (ndarray): The 2D histogram.
        kcentroids (ndarray): Initial cluster centroids.
        threshold (int, optional): Threshold for labeling a bin. Defaults to 0.
        plot (bool, optional): Whether to plot the results. Defaults to False.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.
        return_cmap (bool, optional): Whether to return the colormap used for the label plot.
        max_iter (int, optional): Max number of iterations to perform. Defaults to 30.
    Returns:
        tuple: A tuple containing the following elements:
            - updated_centroids (ndarray): An ndarray containing the updated cluster centroids.
            - labels (ndarray): An ndarray of the same shape as `H`, representing the labels assigned to each point in the histogram.
            - cmap (ListedColormap): (optional) A `ListedColormap` object representing the colormap used for the label plot.

    """
    nclusters = len(kcentroids)
    residual = 1
    niter = 0
    # for _ in range(2 * nclusters):
    while residual > 1e-3 and niter <maxiter:
        # Expectation step
        labels = np.zeros(H.shape)
        for ii in range(H.shape[0]):
            for jj in range(H.shape[1]):
                if H[ii, jj] >= threshold:
                    rc = [ii, jj]
                    distances = distance.cdist([rc], kcentroids)
                    labels[ii, jj] = np.argmin(distances) + 1

        if niter > 0:
            n0 = nl
        nl = np.array([np.sum(labels == l) for l in range(nclusters + 1)])

        # Maximization step
        k0 = kcentroids #save from previous iteration
        kcentroids = ndi.center_of_mass(H, labels=labels, index=range(1, nclusters + 1))
        kcentroids = np.array(kcentroids)
        if verbose:
            print('----')
            print(nl)
            print(kcentroids)
        if niter >0:
            residual = np.linalg.norm(n0-nl)
            print(residual)
        niter += 1
        if verbose:
            print(f'Iteration: {niter}, residual: {residual:.3e}')
    
    if not niter < maxiter:
        print('Warning k-means stopped du to max iterations.')

    cmap = colors.ListedColormap(sns.color_palette(cc.glasbey_dark, n_colors=nclusters))

    if plot:
        plt.figure()
        plt.imshow(labels, origin='lower', cmap=cmap)
        for i, j in kcentroids:
            plt.scatter(j,i)
        plt.xlabel('Reference image')
        plt.ylabel('Evolved image')
    if return_cmap:
        return kcentroids, labels, cmap
    return kcentroids, labels
