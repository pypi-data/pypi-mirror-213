import csv
import pandas as pd
import numpy as np
import scipy.stats as stats
from pedanlib import Pedigree
import math
import os
from pedanlib import Coseg
from datetime import datetime
import os


class Report:
    stamp = None

    def __init__(self, ):
        self.stamp = datetime.now().strftime("%d-%b-%Y %H:%M:%S.%f")

    def batch(self, path):
        listing = [os.path.join(path, ped) for ped in os.listdir(path)]

