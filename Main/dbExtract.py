import copy
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
import neutFunctions as nf
import numpy as np
import os
import pandas as pd
import scipy as sp
from scipy import signal
import sqlite3
import sys

outputDir = sys.argv[1]
