import os

from src.daeclust.bootstrap_daeclust import bootstrap_daeclust
from src.fed_avg.bootstrap_fed_avg import bootstrap_fed_avg

experiences = {
    "daeclust": bootstrap_daeclust,
    "fed_avg": bootstrap_fed_avg
}

if __name__ == '__main__':
    experience = os.environ.DML_EXPERIENCE
    experiences[experience]()

