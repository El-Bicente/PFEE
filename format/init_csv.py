import pandas as pd
from numpy import random

points_df = pd.read_csv("points_ex2.csv")
lines_df = pd.read_csv("lines_ex2.csv")
cells_df = pd.read_csv("faces_split_ex2.csv")

points_df["Weight"] = random.randint(low=0, high=10, size=len(points_df.index))
lines_df["Weight"] = random.randint(low=10, high=20, size=len(lines_df.index))
cells_df["Weight"] = random.randint(low=20, high=30, size=len(cells_df.index))

points_df.to_csv("points.csv", index=False)
lines_df.to_csv("lines.csv", index=False)
cells_df.to_csv("cells.csv", index=False)