import glob
import os
import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping
from pytorch_lightning.loggers import MLFlowLogger
from torch.utils.data import DataLoader
from src.protocol.training.models.experiment import Experiment
from src.datasets.data_loader import DataLoader as DTLDataLoader


class TrainingClient:

    def __init__(self,
                 trainer_id: str,
                 data_loader: DTLDataLoader,
                 enable_gpu=False,
                 output_dir=None,
                 tracking_uri=None,
                 exp_name="default",
                 profiler=None,
                 devices=None,
                 epochs=1
                 ):
        self.trainer_id = trainer_id
        self.data_loader = data_loader
        self.output_dir = output_dir
        self.tracking_uri = tracking_uri
        self.enable_gpu = enable_gpu
        self.exp_name = exp_name
        self.profiler = profiler
        self.devices = devices
        self.epochs = epochs
        self.fast_dev_run = False

    def get_logger(self, model: Experiment, test=False, additional_tags={}):
        mlf_logger = MLFlowLogger(
            experiment_name=model.exp_name,
            tags={
                "cluster_id": model.cluster_id,
                "round_id": str(model.round_id),
                "trainer_id": self.trainer_id,
                "test": str(test)
            } | additional_tags,
            tracking_uri=self.tracking_uri,
        )
        return mlf_logger

    def get_trainer(self, model: Experiment, test=False):
        # to early stop callbacks=[EarlyStopping(monitor="validation_loss", mode="max")],
        if self.enable_gpu:
            return pl.Trainer(
                default_root_dir=self.get_output_dir(),
                accelerator="gpu",
                devices=self.devices,
                auto_select_gpus=True,
                auto_scale_batch_size="binsearch",
                logger=self.get_logger(model, test),
                fast_dev_run=self.fast_dev_run,
                profiler=self.profiler,
                num_processes=self.devices,
                max_epochs=self.epochs,
                enable_progress_bar=False
            )
        return pl.Trainer(
            default_root_dir=self.get_output_dir(),
            accelerator="cpu",
            auto_scale_batch_size="binsearch",
            logger=self.get_logger(model, test),
            fast_dev_run=self.fast_dev_run,
            profiler=self.profiler,
            devices=self.devices,
            max_epochs=self.epochs,
            enable_progress_bar=False
        )

    def get_output_dir(self):
        return os.path.join(self.output_dir, "checkpoints")

    def train_model(self, exp: Experiment) -> Experiment:
        train_loader, val_loader = self.get_train_dataloader()
        trainer = self.get_trainer(exp)
        trainer.fit(exp.model, train_loader, val_loader)
        exp.experiment_id = exp.model.logger.experiment_id
        exp.run_id = exp.model.logger.run_id
        exp.checkpoint_uri = self.get_checkpoint_path(exp)
        return exp

    def get_train_dataloader(self):
        train_dataset, train_sampler = self.data_loader.get_train_data()
        val_dataset, val_sampler = self.data_loader.get_val_data()
        return DataLoader(train_dataset, batch_size=32, sampler=train_sampler), DataLoader(val_dataset, batch_size=32, sampler=val_sampler)

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
        test_loader = self.get_test_dataloader()
        trainer = self.get_trainer(exp, test=True)
        trainer.test(exp.model, test_loader)
        exp.experiment_id = exp.model.logger.experiment_id
        exp.run_id = exp.model.logger.run_id
        return exp

    def get_test_dataloader(self):
        test_dataset, test_sampler = self.data_loader.get_test_data()
        return DataLoader(test_dataset, batch_size=32, sampler=test_sampler)
