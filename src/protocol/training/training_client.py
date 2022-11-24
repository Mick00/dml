
import glob
import os
import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping
from pytorch_lightning.loggers import MLFlowLogger
from torchvision import transforms
from torch.utils.data import random_split, DataLoader, Dataset
from torchvision.datasets import MNIST
from src.protocol.training.models.experiment import Experiment


class TrainingClient:

    def __init__(self,
                 trainer_id: str,
                 enable_gpu=False,
                 output_dir=None,
                 tracking_uri=None,
                 exp_name="default"
                 ):
        self.trainer_id = trainer_id
        self.output_dir = output_dir
        self.tracking_uri = tracking_uri
        self.enable_gpu = enable_gpu
        self.exp_name = exp_name
        self.fast_dev_run = False
        self.train_dataset = None
        self.test_dataset = None
        self.train_set_size = 0
        self.valid_set_size = 0

    def set_dataset(self, train_dataset: Dataset, test_dataset: Dataset):
        self.train_dataset = train_dataset
        self.test_dataset = test_dataset
        self.train_set_size = int(len(self.train_dataset) * 0.85)
        self.valid_set_size = len(self.train_dataset) - self.train_set_size

    def get_logger(self, model: Experiment, test=False):
        mlf_logger = MLFlowLogger(
            experiment_name=model.exp_name,
            tags={
                "cluster_id": model.cluster_id,
                "round_id": str(model.round_id),
                "trainer_id": self.trainer_id,
                "test": str(test)
            },
            tracking_uri=self.tracking_uri,
        )
        return mlf_logger

    def get_trainer(self, model: Experiment, test=False):
        if self.enable_gpu:
            return pl.Trainer(
                default_root_dir=self.get_output_dir(),
                accelerator="gpu",
                devices=-1,
                auto_select_gpus=True,
                auto_scale_batch_size="binsearch",
                callbacks=[EarlyStopping(monitor="validation_loss", mode="max")],
                logger=self.get_logger(model, test),
                fast_dev_run=self.fast_dev_run,
                max_epochs=1
            )
        return pl.Trainer(
            default_root_dir=self.get_output_dir(),
            auto_scale_batch_size="binsearch",
            callbacks=[EarlyStopping(monitor="validation_loss", mode="max")],
            logger=self.get_logger(model, test),
            fast_dev_run=self.fast_dev_run,
            max_epochs=1
        )

    def get_output_dir(self):
        return os.path.join(self.output_dir, "checkpoints")

    def train_model(self, exp: Experiment) -> Experiment:
        mnist_train, mnist_val = random_split(self.train_dataset, [self.train_set_size, self.valid_set_size])
        train_loader = DataLoader(mnist_train, batch_size=32)
        val_loader = DataLoader(mnist_val, batch_size=32)
        trainer = self.get_trainer(exp)
        trainer.fit(exp.model, train_loader, val_loader)
        exp.experiment_id = exp.model.logger.experiment_id
        exp.run_id = exp.model.logger.run_id
        exp.checkpoint_uri = self.get_checkpoint_path(exp)
        return exp

    def get_checkpoint_path(self, exp: Experiment):
        checkpoint_folder = os.path.join(self.get_output_dir(), exp.experiment_id, exp.run_id, "checkpoints/")
        checkpoints = glob.glob(f"{checkpoint_folder}*")
        meta_checkpoint = list(map(lambda ckpt_path: os.path.basename(ckpt_path), checkpoints))
        meta_checkpoint = list(map(lambda ckpt_file_name: os.path.splitext(ckpt_file_name)[0], meta_checkpoint))
        meta_checkpoint = list(map(lambda ckpt_file_name: ckpt_file_name.split("-"), meta_checkpoint))
        meta_checkpoint = list(map(lambda metas: {meta.split("=")[0]: int(meta.split("=")[1]) for meta in metas}, meta_checkpoint))
        biggest_epoch = 0
        biggest_step = 0
        last_checkpoint = ""
        for path, meta in zip(checkpoints, meta_checkpoint):
            if meta.get('epoch') > biggest_epoch:
                biggest_epoch = meta.get('epoch')
                biggest_step = meta.get("step")
                last_checkpoint = path
            if meta.get('epoch') == biggest_epoch and meta.get("step") > biggest_step:
                biggest_step = meta.get("step")
                last_checkpoint = path
        return last_checkpoint

    def test_model(self, exp: Experiment):
        test_loader = DataLoader(self.test_dataset, batch_size=32)
        trainer = self.get_trainer(exp, test=True)
        trainer.test(exp.model, test_loader)
        exp.experiment_id = exp.model.logger.experiment_id
        exp.run_id = exp.model.logger.run_id
        return exp
