import torch
from torch.nn import functional as F
import pytorch_lightning as pl

from src.base.training.models.aes_utils import get_enc_dec


class CaeLeNetLight(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.encoder, self.decoder = get_enc_dec([
            {
                "in_channels": 1,
                "out_channels": 3,
                "padding": 2,
                "kernel_size": 5,
                "scale_factor": 1 / 2
            },
            {
                "in_channels": 6,
                "out_channels": 9,
                "padding": 0,
                "kernel_size": 5,
                "scale_factor": 1 / 2
            }
        ])
        self.learning_rate = 1e-3
        self.batch_size = 64

    def forward(self, x):
        return self.encoder(x)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1)
        return [optimizer], [lr_scheduler]

    def step(self, train_batch, batch_idx):
        x, y = train_batch
        z = self.encoder(x)
        x_hat = self.decoder(z)
        return x, x_hat

    def calc_loss(self, x, x_hat, log_label=''):
        loss = F.mse_loss(x_hat, x)
        if log_label:
            self.log(log_label, loss)
        return loss

    def training_step(self, train_batch, batch_idx):
        x, x_hat = self.step(train_batch, batch_idx)
        return self.calc_loss(x, x_hat, 'training_loss')

    def validation_step(self, val_batch, batch_idx):
        x, x_hat = self.step(val_batch, batch_idx)
        self.calc_loss(x, x_hat, 'validation_loss')

    def test_step(self, batch, batch_idx):
        x, x_hat = self.step(batch, batch_idx)
        self.calc_loss(x, x_hat, 'test_loss')