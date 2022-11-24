
from torchvision.datasets import MNIST
from torchvision.transforms import transforms


def load_mnist(data_path: str):
    train_dataset = MNIST(
        data_path,
        train=True,
        download=True,
        transform=transforms.ToTensor()
    )
    test_dataset = MNIST(
        data_path,
        train=False,
        download=True,
        transform=transforms.ToTensor()
    )
    return train_dataset, test_dataset
