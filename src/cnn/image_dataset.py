from torch.utils.data import Subset
from torchvision.transforms import (
    ToTensor,
    Compose,
    Resize,
    Grayscale,
)
from sklearn.model_selection import train_test_split
import torch
import matplotlib.pyplot as plt
from torchvision.utils import make_grid
import matplotlib.pyplot as plt

from custom_dataset_from_csv import CustomDatasetFromCSV
from neural_network import NeuralNetwork
import os

class CreateDataset(): 

    @classmethod
    def create_dataset(cls, width: int, height: int, labels_csv: str, img_dir: str):
        transform = Compose([Resize((width, height)), Grayscale(), ToTensor()])
        return CustomDatasetFromCSV(
            labels_csv,
            img_dir,
            width,
            height,
            transform,
        )

class TrainDataSet():

    model_name = "auth.pth"

    def __init__(self ):
        pass

    def train_test_dataset(self, dataset, test_split=0.25):
        train_idx, test_split = train_test_split(
            list(range(len(dataset))), test_size=test_split
        )
        datasets = {}
        datasets["train"] = Subset(dataset, train_idx)
        datasets["test"] = Subset(dataset, test_split)
        return datasets


    def create_split_data(self):
        data_root = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data"
        )
        labels = os.path.join(data_root, "labels.csv")
        img_dir = os.path.join(data_root, "img_dir")

        dataset = CreateDataset().create_dataset(48, 48, labels, img_dir)
        datasets = self.train_test_dataset(dataset)
        return datasets["train"], datasets["test"]


    def prepare_dataset(self):
        from torch.utils.data import DataLoader

        train, test = self.create_split_data()

        train_dataloader = DataLoader(train, batch_size=256, shuffle=True)
        test_dataloader = DataLoader(test, batch_size=64, shuffle=True)

        return train_dataloader, test_dataloader


    def display_dataset(self):
        train_dataloader, _ = self.prepare_dataset()

        for images, labels in train_dataloader:
            fig, ax = plt.subplots(figsize=(16, 12))
            ax.set_xticks([])
            ax.set_yticks([])
            ax.imshow(make_grid(images, nrow=16).permute(1, 2, 0))
            break


    def get_default_device(self):
        """Set Device to GPU or CPU"""
        if torch.cuda.is_available():
            return torch.device("cuda")
        else:
            return torch.device("cpu")


    def to_device(self, data, device):
        "Move data to the device"
        if isinstance(data, (list, tuple)):
            return [self.to_device(x, device) for x in data]
        return data.to(device, non_blocking=True)


    def evaluate(self, model, val_loader):
        model.eval()
        outputs = [model.validation_step(batch) for batch in val_loader]
        return model.validation_epoch_end(outputs)


    def fit(self, epochs, lr, model, train_loader, val_loader, opt_func=torch.optim.SGD):

        history = []
        optimizer = opt_func(model.parameters(), lr)
        for epoch in range(epochs):

            model.train()
            train_losses = []
            for batch in train_loader:
                loss = model.training_step(batch)
                train_losses.append(loss)
                loss.backward(retain_graph=True)
                optimizer.step()
                optimizer.zero_grad()

            result = self.evaluate(model, val_loader)
            result["train_loss"] = torch.stack(train_losses).mean().item()
            model.epoch_end(epoch, result)
            history.append(result)

        return history


    def go(self):
        train_dl, test_dl = self.prepare_dataset()

        num_epochs = 10
        # opt_func = torch.optim.Adam
        lr = 0.01

        device = self.get_default_device()
        model = self.to_device(NeuralNetwork(), device)
        # fitting the model on training data and record the result after each epoch
        history = self.fit(num_epochs, lr, model, train_dl, test_dl)
        history
        torch.save(model.state_dict(), self.model_name)


    def load(self):
        model = NeuralNetwork()
        model.load_state_dict(torch.load(self.model_name))
        model.eval()
        return model


# train = TrainDataSet()
# train.go()
