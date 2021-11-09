import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import plotly

num=3

con = sqlite3.connect('../data/bench%d/benchmark%d.db' % (num,num))

planners=["RRTConnect", "PRM", "RRT", "LazyPRM", "LBKPIECE", "BKPIECE", "KPIECE", "EST"]
robots=[(1,"irb_140","orangered"),(3,"kr6","olivedrab"),(5,"ur5","royalblue")]

fig = go.Figure()

for robot in robots:

    df=pd.read_sql("SELECT time,request_planner_id FROM runs WHERE experimentid=%d" % robot[0],con)
    print(df)
    # df["time"].clip(upper=5.05,inplace=True)

    fig.add_trace(go.Box(
        y=df["time"],
        x=df["request_planner_id"],
        name=robot[1],
        marker_color=robot[2]
    ))

fig.update_layout(
    yaxis_title='<b>Computation Time</b>',
    font=dict(
        family="Courier New, monospace",
        # size=18,
    ),
    boxmode='group' # group together boxes of the different traces for each value of x
)

fig.write_html("tiempo"+str(num)+".html")

# plotly.io.write_image(fig,"timebox.pdf", format="pdf", width=1000, height=500)

fig.show()
