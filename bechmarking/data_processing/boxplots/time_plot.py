import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import plotly

con = sqlite3.connect('../data/bench3/benchmark3.db')

planners=["RRTConnect", "PRM", "RRT", "LazyPRM", "LBKPIECE", "BKPIECE", "KPIECE", "EST"]
robots=[(1,"irb_140","orangered"),(3,"kr6","olivedrab"),(5,"ur5","royalblue")]

fig = go.Figure()

for robot in robots:

    df=pd.read_sql("SELECT time,request_planner_id FROM runs WHERE experimentid=%d" % robot[0],con)
    print(df)

    fig.add_trace(go.Box(
        y=df["time"],
        x=df["request_planner_id"],
        name=robot[1],
        marker_color=robot[2]
    ))

fig.update_layout(
    yaxis_title='Computation Time',
    boxmode='group' # group together boxes of the different traces for each value of x
)

fig.write_html("tiempo3.html")

plotly.io.write_image(fig,"timebox.pdf", format="pdf", width=100, height=100)

fig.show()
