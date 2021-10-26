import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

con = sqlite3.connect('../benchmark.db')
cur = con.cursor()

planners=["RRTConnect", "PRM", "RRT", "LazyPRM", "LBKPIECE", "BKPIECE", "KPIECE", "EST"]
robots=[(1,"irb_140"),(3,"kr6"),(5,"ur5")]

df = pd.DataFrame( )

iterables=[[],planners]

for robot in robots:

    iterables[0].append(robot[1])

    for planner in planners:

        cur.execute('SELECT time FROM runs WHERE request_planner_id="%s" AND experimentid=%d' % (planner,robot[0]))
        rows = cur.fetchall()
        # print(list(rows))
        lista=[]
        for row in rows:
            lista.append(row[0])

        df[robot[1],planner]=lista

print(df)
index=pd.MultiIndex.from_product(iterables, names=["Robots","Planners"])
df.columns=index
print(df)


print("irb_140 \n", df["irb_140"].describe(),"\n")
print("mean \n", df["irb_140"].mean(),"\n")
df.mean().to_csv("tabla.csv")
# print("kr6 \n", df["kr6"].describe(),"\n")
# print("ur5 \n", df["ur5"].describe(),"\n")
