# %%
from src.quikclient import QuikClient
import pandas as pd
import numpy as np
# %%
c= QuikClient()
# %%
# print(c.get_new_func("STOP_ORDERS"))
# print(c.get_new_func("ORDERS"))
# x = c.get_orders("TRADES")
# x = c.get_orders("ORDERS")
x = c.get_orders("ORDERS")
# x = c.get_orders("STOP_ORDERS")
x
# %%
x.columns
# %%
df.columns
# %%
len(x)
# %%

print('all Ok')