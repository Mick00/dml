# Decentralised Machine Learning

DML is an event driven system used for research purposes.

It currently uses RabbitMQ to connect all trainers and MlFlow for experiment tracking

## Experiences

### Federated Average

The simplest experience is the federated average example.
Trainers randomly share and generate an ID, lowest ID creates the seed model in the round 0
then shares it with its peers. All trainers participate for the following round and no update is excluded.

## Installation

### Development

### Requirements
Requires Python 3 (tested on 3.9)
Helpful to have Docker to run the RabbitMQ server and MlFlow, but you can connect
to any instance

### Installation
Install dependencies (Windows) with:`pip install -r requirements.txt`
Start RabbitMQ and MlFlow with `docker compose up -d`

### Production

1. Configure the .env file
2. Launch your experience: `docker compose -f .\docker-compose.yml -f .\fed_avg_sliced.yml up -d --build`

## Architecture Overview

### The Event Listener
The architecture uses an event driven approach with the EventHandler being the centerpiece.
The Event Handler has a thread safe event queue which lets other thread emit events by appending 
events to the queue. The events are then processed by the handler thread. 
The framework has a thread for event processing, and it should be the only one
to modify the state to avoid concurrency issue. 

### The State
The application has a state which lets modules store and access information.
Event Handlers can modify the state, and it should only be done on the event handler thread.
If you want to modify the state from another thread, you should emit an event to
the event handler which will modify the state when processed by the event handler.

### Event Handler
Event handlers are functions which will get registered to the event listener
and will be triggered when an event is received. They can emit new events to trigger
new event handler.

### The Client
The client is used to connect with other nodes. By default, it connects to a RabbitMQ instance 
to broadcast messages to all nodes.

The objective of this architecture is to have an extensible and composable framework
to build complex systems and easily switch between modules. For example, you could switch the client
module by registering a new set of event handlers to handle the events.