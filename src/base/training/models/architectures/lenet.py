import torch
import torchmetrics.functional
from torch import nn
import pytorch_lightning as pl
from torch.nn.functional import nll_loss, log_softmax
from torchmetrics import Accuracy

from src.base.training.models.aes_utils import get_enc_dec
from src.base.training.models.layers.conv import ConvLayer


class LeNet(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            ConvLayer(1, 6, 1 / 2, 5, 1, 2),
            ConvLayer(6, 16, 1 / 2, 5, 1, 0),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(start_dim=1),
            nn.Linear(400, 120),
            nn.Sigmoid(),
            nn.Linear(120, 84),
            nn.Sigmoid(),
            nn.Linear(84, 10),
        )
        self.learning_rate = 1e-3
        self.batch_size = 64
        self.val_accuracy = Accuracy()
        self.test_accuracy = Accuracy()

    def forward(self, x):
        x = self.encoder(x)
        pred = self.classifier(x)
        return log_softmax(pred, dim=1)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1)
        return [optimizer], [lr_scheduler]

    def training_step(self, train_batch, batch_idx):
        x, y = train_batch
        logits = self(x)
        return nll_loss(logits, y)

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = nll_loss(logits, y)
        preds = torch.argmax(logits, dim=1)
        self.val_accuracy.update(preds, y)

        # Calling self.log will surface up scalars for you in TensorBoard
        self.log("val_loss", loss, prog_bar=True)
        self.log("val_acc", self.val_accuracy, prog_bar=True)

    def test_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = nll_loss(logits, y)
        preds = torch.argmax(logits, dim=1)
        self.test_accuracy.update(preds, y)

        # Calling self.log will surface up scalars for you in TensorBoard
        self.log("test_loss", loss, prog_bar=True)
        self.log("test_acc", self.test_accuracy, prog_bar=True)