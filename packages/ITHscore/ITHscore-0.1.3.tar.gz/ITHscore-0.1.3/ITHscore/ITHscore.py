from .load import load_image, load_mask
from .locate import get_largest_slice, locate_tumor
from .features import extract_radiomic_features
from .clustering import pixel_clustering, visualization
from .calculate import calITHscore


class ITHscore:
    def load_image(self, path):
        return load_image(path)

    def load_mask(self, path):
        return load_mask(path)

    def get_slice(self, img3d, mask3d):
        image, mask = get_largest_slice(img3d, mask3d)
        return image, mask

    def locate(self, image, mask, padding=2):
        sub_img, sub_mask = locate_tumor(image, mask, padding)
        return sub_img, sub_mask

    def calfeatures(self, sub_img, sub_mask, category="all", window_size=2, PCs=None):
        return extract_radiomic_features(sub_img, sub_mask, category, window_size, PCs)

    def label_map(self, sub_img, sub_mask, features, cluster=6):
        return pixel_clustering(sub_img, sub_mask, features, cluster)

    def generate_fig(self, img, sub_img, mask, sub_mask, features, cluster=6):
        return visualization(img, sub_img, mask, sub_mask, features, cluster)

    def calITHscore(self, label_map, min_area=200, thresh=2):
        return calITHscore(label_map, min_area, thresh)

    # def assist(self):
    #     return assist(xxx)