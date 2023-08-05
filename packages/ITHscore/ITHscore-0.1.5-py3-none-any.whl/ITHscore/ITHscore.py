import os
import numpy as np
import six
from scipy import ndimage
import matplotlib.pyplot as plt
from radiomics import featureextractor
import SimpleITK as sitk
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

def read_dcm_series(dcm_dir):
    """
    Args:
        dcm_dir: String. Path to dicom series directory
    Returns:
        sitk_image: SimpleITK object of 3D CT volume.
    """
    reader = sitk.ImageSeriesReader()
    series_file_names = reader.GetGDCMSeriesFileNames(dcm_dir)
    reader.SetFileNames(series_file_names)
    sitk_image = reader.Execute()

    return sitk_image


def load_image(path):
    """
    Args:
        path: String. Path to the .nii(.gz) file or dicom series directory
    Returns:
        image: Numpy array. The 3D CT volume.
    """
    if os.path.isdir(path):
        sitk_image = read_dcm_series(path)
    else:
        sitk_image = sitk.ReadImage(path)
    image = sitk.GetArrayFromImage(sitk_image)

    return image


def load_mask(path):
    """
    Args:
        path: String. Path to the .nii or .dcm mask.
    Returns:
        mask: Numpy array. The mask of tumor with the same shape of image.
    """
    sitk_mask = sitk.ReadImage(path)
    mask = sitk.GetArrayFromImage(sitk_mask)

    return mask


def get_largest_slice(img3d, mask3d):
    """
    Get the slice with largest tumor area
    Args:
        img3d: Numpy array. The whole CT volume (3D)
        mask3d: Numpy array. Same size as img3d, binary mask with tumor area set as 1, background as 0
    Returns:
        img: Numpy array. The 2D image slice with largest tumor area
        mask: Numpy array. The subset of mask in the same position of sub_img
    """
    area = np.sum(mask3d == 1, axis=(1, 2))
    area_index = np.argsort(area)[-1]
    img = img3d[area_index, :, :]
    mask = mask3d[area_index, :, :]

    return img, mask


def locate_tumor(img, mask, padding=2):
    """
    Locate and extract tumor from CT image using mask
    Args:
        img: Numpy array. The whole image
        mask: Numpy array. Same size as img, binary mask with tumor area set as 1, background as 0
        padding: Int. Number of pixels padded on each side after extracting tumor
    Returns:
        sub_img: Numpy array. The tumor area defined by mask
        sub_mask: Numpy array. The subset of mask in the same position of sub_img
    """
    top_margin = min(np.where(mask == 1)[0])
    bottom_margin = max(np.where(mask == 1)[0])
    left_margin = min(np.where(mask == 1)[1])
    right_margin = max(np.where(mask == 1)[1])
    # padding two pixels at each edges for further computation
    sub_img = img[top_margin - padding:bottom_margin + padding + 1, left_margin - padding:right_margin + padding + 1]
    sub_mask = mask[top_margin - padding:bottom_margin + padding + 1,
                    left_margin - padding:right_margin + padding + 1]

    return sub_img, sub_mask


def extract_radiomic_features(sub_img, sub_mask, category="all", window_size=2, PCs=None):
    """
    Extract pre-defined radiomic features, you can select a category of features or use all features
    Args:
        sub_img: Numpy array. Rectangle image contains nodule
        sub_mask: Numpy array. Same size as sub_img with binary values, 1 for tumor area and 0 for background
        category: Str. The category of radiomic features. Choices are: "first-order", "texture", "PCA"
        window_size: Int. Size of sliding window when extract radiomic features for each pixel. window_size=2 for a 5x5 window
        PCs: Int, Number of PC when using category "PCA"
    Returns:
        features: Numpy array. A p x n matrix, p is the number of pixels of tumor, n is the number of radiomic features
    """
    features = dict()
    features['first'] = []
    features['shape'] = []
    features['glcm'] = []
    features['gldm'] = []
    features['glrlm'] = []
    features['glszm'] = []
    features['ngtdm'] = []
    for p in range(len(sub_img)):
        for q in range(len(sub_img[0])):
            if sub_mask[p][q] == 1:
                mask = np.copy(sub_img)
                mask[:, :] = 0
                mask[p - window_size:p + window_size + 1, q - window_size:q + window_size + 1] = 1
                img_ex = sitk.GetImageFromArray([sub_img])
                mask_ex = sitk.GetImageFromArray([mask])
                extractor = featureextractor.RadiomicsFeatureExtractor()
                radio_result = extractor.execute(img_ex, mask_ex)
                first_features_temp = []
                shape_features_temp = []
                glcm_features_temp = []
                gldm_features_temp = []
                glrlm_features_temp = []
                glszm_features_temp = []
                ngtdm_features_temp = []
                for key, val in six.iteritems(radio_result):
                    if key.startswith('original_firstorder'):
                        first_features_temp.append(val)
                    elif key.startswith('original_shape'):
                        shape_features_temp.append(val)
                    elif key.startswith('original_glcm'):
                        glcm_features_temp.append(val)
                    elif key.startswith('original_gldm'):
                        gldm_features_temp.append(val)
                    elif key.startswith('original_glrlm'):
                        glrlm_features_temp.append(val)
                    elif key.startswith('original_glszm'):
                        glszm_features_temp.append(val)
                    elif key.startswith('original_ngtdm'):
                        ngtdm_features_temp.append(val)
                    else:
                        pass
                features['first'].append(first_features_temp)
                features['shape'].append(shape_features_temp)
                features['glcm'].append(glcm_features_temp)
                features['gldm'].append(gldm_features_temp)
                features['glrlm'].append(glrlm_features_temp)
                features['glszm'].append(glszm_features_temp)
                features['ngtdm'].append(ngtdm_features_temp)
    if category == 'all':
        features = np.hstack((features['first'], features['shape'], features['glcm'], features['gldm'], features['glrlm'], features['glszm'], features['ngtdm']))
    elif category == 'first-order':
        features = features['first']
    elif category == 'texture':
        features = np.hstack((features['glcm'], features['gldm'], features['glrlm'], features['glszm'], features['ngtdm']))
    elif category == 'PCA':
        features = np.hstack((features['first'], features['shape'], features['glcm'], features['gldm'], features['glrlm'], features['glszm'], features['ngtdm']))
        features = PCA(n_components = PCs).fit_transform(features)
    else:
        raise RuntimeError('inputError')

    return features


def pixel_clustering(sub_img, sub_mask, features, cluster=6):
    """
    Args:
        sub_img: Numpy array. Tumor image
        sub_mask: Numpy array. Same size as tumor_img, 1 for nodule and 0 for background
        features: Numpy array. Matrix of radiomic features. Rows are pixels and columns are features
        cluster: Int. The cluster number in clustering
    Returns:
        label_map: Numpy array. Labels of pixels within tumor. Same size as tumor_img
    """
    features = MinMaxScaler().fit_transform(features)
    label_map = sub_img.copy()
    clusters = KMeans(n_clusters=cluster).fit_predict(features)
    cnt = 0
    for i in range(len(sub_img)):
        for j in range(len(sub_img[0])):
            if sub_mask[i][j] == 1:
                label_map[i][j] = clusters[cnt] + 1
                cnt += 1
            else:
                label_map[i][j] = 0

    return label_map


def visualization(img, sub_img, mask, sub_mask, features, cluster=6):
    """
    Args:
        img: Numpy array. Original whole image, used for display
        sub_img: Numpy array. Tumor image
        mask: Numpy array. Same size as img, 1 for tumor and 0 for background, used for display
        sub_mask: Numpy array. Same size as sub_img, 1 for nodule and 0 for background
        features: Numpy array. Matrix of radiomic features. Rows are pixels and columns are features
        cluster: Int or Str. Integer defines the cluster number in clustering. "all" means iterate clusters from 3 to 9 to generate multiple cluster pattern.
    Returns:
        fig: figure for display
    """
    if cluster != "all":
        fig = plt.figure()
        label_map = pixel_clustering(sub_img, sub_mask, features, cluster)
        plt.matshow(label_map, fignum=0)
        plt.xlabel(f"Cluster pattern (K={cluster})", fontsize=15)

        return fig

    else:   # generate cluster pattern with multiple resolutions, together with whole lung CT
        max_cluster = 9
        # Subplot 1: CT image of the whole lung
        fig = plt.figure(figsize=(12, 12))
        plt.subplot(3, (max_cluster + 2) // 3, 1)
        plt.title('Raw Image')
        plt.imshow(img, cmap='gray')
        plt.scatter(np.where(mask == 1)[1], np.where(mask == 1)[0], marker='o', color='red', s=0.2)

        # Subplot 2: CT iamge of the nodule
        plt.subplot(3, (max_cluster + 2) // 3, 2)
        plt.title('Tumor')
        plt.imshow(sub_img, cmap='gray')

        # Subplot 3~n: cluster label map with different K
        area = np.sum(sub_mask==1)
        for clu in range(3, max_cluster + 1):
            label_map = pixel_clustering(sub_img, sub_mask, features, clu)
            plt.subplot(3, (max_cluster + 2) // 3, clu)
            plt.matshow(label_map, fignum=0)
            plt.xlabel(str(clu) + ' clusters', fontsize=15)
        plt.subplots_adjust(hspace=0.3)
        #     plt.subplots_adjust(wspace=0.01)
        plt.suptitle(f'Cluster pattern with multiple resolutions (area = {area})', fontsize=15)

        return fig


def calITHscore(label_map, min_area=200, thresh=2):
    """
    Calculate ITHscore from clustering label map
    Args:
        label_map: Numpy array. Clustering label map
        min_area: Int. For tumor area (pixels) smaller than "min_area", we don't consider connected-region smaller than "thresh"
        thresh: Int. The threshold for connected-region's area, only valid for tumor < min_area
    Returns:
        ith_score: Float. The level of ITH, between 0 and 1
    """
    size = np.sum(label_map > 0)  # Record the number of total pixels
    num_regions_list = []
    max_area_list = []
    for i in np.unique(label_map)[1:]:  # For each gray level except 0 (background)
        flag = 1  # Flag to count this gray level, in case this gray level has only one pixel
        # Find (8-) connected-components. "num_regions" is the number of connected components
        labeled, num_regions = ndimage.label(label_map==i, structure=ndimage.generate_binary_structure(2,2))
        max_area = 0
        for j in np.unique(labeled)[1:]:  # 0 is background (here is all the other regions)
            # Ignore the region with only 1 or "thresh" px
            if size <= min_area:
                if np.sum(labeled == j) <= thresh:
                    num_regions -= 1
                    if num_regions == 0:  # In case there is only one region
                        flag = 0
                else:
                    temp_area = np.sum(labeled == j)
                    if temp_area > max_area:
                        max_area = temp_area
            else:
                if np.sum(labeled == j) <= 1:
                    num_regions -= 1
                    if num_regions == 0:  # In case there is only one region
                        flag = 0
                else:
                    temp_area = np.sum(labeled == j)
                    if temp_area > max_area:
                        max_area = temp_area
        if flag == 1:
            num_regions_list.append(num_regions)
            max_area_list.append(max_area)
    # Calculate the ITH score
    ith_score = 0
    print(num_regions_list)
    for k in range(len(num_regions_list)):
        ith_score += float(max_area_list[k]) / num_regions_list[k]
    # Normalize each area with total size
    ith_score = ith_score / size
    ith_score = 1 - ith_score

    return ith_score

