import sqlite3
import numpy as np
import plotly.graph_objects as go

con = sqlite3.connect('benchmark.db')
cur = con.cursor()

planners=["RRTConnect", "PRM", "RRT", "LazyPRM", "LBKPIECE", "BKPIECE", "KPIECE", "EST"]
robots=[(1,"irb_140"),(3,"kr6"),(5,"ur5")]

fig = go.Figure()

for robot in robots:
    print(robot[1])
    exitos=[]

    for planner in planners:

        cur.execute('SELECT COUNT(*) FROM runs WHERE request_planner_id="%s" AND experimentid=%d AND success=1' % (planner,robot[0]))
        rows = cur.fetchall()
        print(planner, rows[0][0])
        exitos.append(rows[0][0])

    print("\n")


    fig.add_trace(go.Scatterpolar(
          r=exitos,
          theta=planners,
          fill='toself',
          name=robot[1]
    ))

fig.update_layout(
  title="Successfull trajectories out of 100 runs",
  title_font_family="Times New Roman",
  title_font_color="red",
  title_font_size=30,
  legend_title="Robots",
  legend_font_size=18,
  polar=dict(
    radialaxis=dict(
      visible=True
      # range=[0, 5]
    )),
  showlegend=True
)

fig.write_html("success.html")

fig.show()
