import random
from robot.api import logger


def random_num():
    return random.randint(0, 100)


def greet_someone(name):
    logger.info("Hi " + name + "! Hope you have a great day!")
