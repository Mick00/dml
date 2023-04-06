# @version 0.3.4

from .Models import Models
from .Trainers import Trainers
from .Updates import Updates

models: public(Models)
trainers: public(Trainers)
updates: public(Updates)

@external
def setModels(models: address):
    self.models = Models(models)

@external
def setTrainers(trainers: address):
    self.trainers = Trainers(trainers)

@external
def setUpdates(updates: address):
    self.updates = Updates(updates)
