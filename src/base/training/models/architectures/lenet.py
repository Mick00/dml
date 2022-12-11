import torch
from torch import nn
import pytorch_lightning as pl

from src.base.training.models.aes_utils import get_enc_dec


class LeNet(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.encoder, _ = get_enc_dec([
            {
                "in_channels": 1,
                "out_channels": 6,
                "padding": 2,
                "kernel_size": 5,
                "scale_factor": 1 / 2
            },
            {
                "in_channels": 6,
                "out_channels": 16,
                "padding": 0,
                "kernel_size": 5,
                "scale_factor": 1 / 2
            }
        ])
        self.classifier = nn.Sequential(
            nn.Flatten(start_dim=1),
            nn.Linear(400, 120),
            nn.Sigmoid(),
            nn.Linear(120, 84),
            nn.Sigmoid(),
            nn.Linear(84, 10),
            nn.Softmax(dim=1)
        )
        self.learning_rate = 1e-3
        self.batch_size = 64

    def forward(self, x):
        return self.encoder(x)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1)
        return [optimizer], [lr_scheduler]

    def step(self, x, y):
        x = self.encoder(x)
        pred = self.classifier(x)
        return pred

    def calc_metric(self, pred, y, log_label=''):
        accuracy = torch.sum(pred.argmax(1) == y) / len(y)
        if log_label:
            self.log(log_label, accuracy)
        return accuracy

    def training_step(self, train_batch, batch_idx):
        x, y = train_batch
        pred = self.step(x, y)
        return self.calc_metric(pred, y, 'training_loss')

    def validation_step(self, val_batch, batch_idx):
        x, y = val_batch
        pred = self.step(x, y)
        self.calc_metric(pred, y, 'validation_loss')

    def test_step(self, batch, batch_idx):
        x, y = batch
        pred = self.step(x, y)
        self.calc_metric(pred, y, 'test_loss')