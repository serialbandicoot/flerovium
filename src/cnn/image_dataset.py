import os
import pandas as pd
from torch import tensor
from torchvision.io import read_image
from torch.utils.data import Dataset, Subset
from torchvision.transforms import (
    ToTensor,
    ToPILImage,
    Lambda,
    Compose,
    Resize,
    Grayscale,
)
from sklearn.model_selection import train_test_split
from torch import nn
import torch
import numpy as np
from PIL import Image
from torch.nn import Sequential
import matplotlib.pyplot as plt

####################################
#
# labels_map = {
#   1: sign_in,
#   2: username,
#   3: password,
#   4: sign_up,
#   5: about,
# }
#


class CustomDatasetFromCSV(Dataset):
    def __init__(self, csv_path, img_dir, height, width, transforms=None):
        """
        Args:
            csv_path (string): path to csv file
            height (int): image height
            width (int): image width
            transform: pytorch transforms for transforms and tensor conversion
        """
        self.data = pd.read_csv(csv_path)
        self.labels = np.asarray(self.data.iloc[:, 0])
        self.height = height
        self.width = width
        self.transforms = transforms
        self.img_dir = img_dir

    def __getitem__(self, index):
        img_path = os.path.join(self.img_dir, self.labels[index])
        # image = read_image(img_path)

        single_image_label = self.labels[index]
        # # Read each 784 pixels and reshape the 1D array ([784]) to 2D array ([28,28])
        # img_as_np= np.array(Image.open(img_path)).reshape(1,28,28).astype('uint8')
        # # Convert image from numpy array to PIL image, mode 'L' is for grayscale
        # img_as_img = Image.fromarray(img_as_np)
        # img_as_img = img_as_img.convert('L')
        # Transform image to tensor
        if self.transforms is not None:
            img_as_tensor = self.transforms(Image.open(img_path))
        # Return image and the label
        return (img_as_tensor, single_image_label)

    def __len__(self):
        return len(self.data.index)


class ImageDataset(Dataset):
    def __init__(
        self, annotations_file, img_dir, transform=None, target_transform=None
    ):
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = Lambda(
            lambda y: torch.zeros(10, dtype=torch.float).scatter_(
                dim=0, index=torch.tensor(y), value=1
            )
        )

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        label = self.img_labels.iloc[idx, 1]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label


def create_dataset():
    # return ImageDataset(
    #     annotations_file="/flerovium/src/cnn/data/labels.csv",
    #     img_dir="/flerovium/src/cnn/data/img_dir",
    # )
    transform = Compose([Resize((48, 96)), Grayscale(), ToTensor()])
    return CustomDatasetFromCSV(
        "/Users/sam.treweek/Projects/flerovium/src/cnn/data/labels.csv",
        "/Users/sam.treweek/Projects/flerovium/src/cnn/data/img_dir",
        28,
        28,
        transform,
    )


def train_test_dataset(dataset, test_split=0.25):
    train_idx, test_split = train_test_split(
        list(range(len(dataset))), test_size=test_split
    )
    datasets = {}
    datasets["train"] = Subset(dataset, train_idx)
    datasets["test"] = Subset(dataset, test_split)
    return datasets


def create_split_data():
    dataset = create_dataset()
    datasets = train_test_dataset(dataset)
    return datasets["train"], datasets["test"]


def prepare_dataset():
    from torch.utils.data import DataLoader

    train, test = create_split_data()

    train_dataloader = DataLoader(train, batch_size=64, shuffle=True)
    test_dataloader = DataLoader(test, batch_size=64, shuffle=True)

    return train_dataloader, test_dataloader


# class NeuralNetwork(nn.Module):
#     def __init__(self):
#         super(NeuralNetwork, self).__init__()
#         self.flatten = nn.Flatten()
#         self.linear_relu_stack = nn.Sequential(
#             nn.Linear(28 * 28, 512),
#             nn.ReLU(),
#             nn.Linear(512, 512),
#             nn.ReLU(),
#             nn.Linear(512, 10),
#         )

#     def forward(self, x):
#         x = self.flatten(x)
#         logits = self.linear_relu_stack(x)
#         return logits


# def model():
#     import torch

#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     model = NeuralNetwork().to(device)
#     return model


# import torch
# import torchvision.models as models

# model = models.vgg16(pretrained=True)
# torch.save(model.state_dict(), "model_weights.pth")


def iterate_dataset():
    train_dataloader, test_dataloader = prepare_dataset()

    train_features, train_labels = next(iter(train_dataloader))
    print(f"Feature batch shape: {train_features.size()}")
    print(f"Labels batch shape: {len(train_labels)}")
    img = train_features[3].squeeze()
    label = train_labels[3]
    plt.imshow(img, cmap="gray")
    plt.show()
    print(f"Label: {label}")


# iterate_dataset()
