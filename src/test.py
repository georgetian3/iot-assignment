import numpy as np


def add_random_noise(wave):
    noise = np.random.normal(0,1,100)
    wave += noise