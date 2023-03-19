import pandas as pd
import numpy as np 

from function.func import *
field1 = pd.read_csv("data/field_b1mn055x.csv").values.reshape(1,-1).tolist()[0]
