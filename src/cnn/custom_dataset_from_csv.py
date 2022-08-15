from torch.utils.data import Dataset
import os
import pandas as pd
import numpy as np
from PIL import Image

####################################
#
# labels_map = {
#   ?: sign_in,
#   ?: username,
#   ?: password,
#   ?: sign_up,
#   ?: about,
# }
#


class CustomDatasetFromCSV(Dataset):
    def __init__(self, csv_path, img_dir, height, width, transforms=None):
        self.data = pd.read_csv(csv_path)
        self.file = np.asarray(self.data.iloc[:, 0])
        self.labels = np.asarray(self.data.iloc[:, 1])
        self.height = height
        self.width = width
        self.transforms = transforms
        self.img_dir = img_dir

    def __getitem__(self, index):
        img_path = os.path.join(self.img_dir, self.file[index])

        single_image_label = self.labels[index]
        if self.transforms is not None:
            img_as_tensor = self.transforms(Image.open(img_path))
        # Return image and the label
        return (img_as_tensor, single_image_label)

    def __len__(self):
        return len(self.data.index)
