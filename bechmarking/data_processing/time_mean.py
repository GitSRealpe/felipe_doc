import sqlite3
import numpy as np
import plotly.graph_objects as go

con = sqlite3.connect('benchmark.db')
cur = con.cursor()

planners=["RRTConnect", "PRM", "RRT", "LazyPRM", "LBKPIECE", "BKPIECE", "KPIECE", "EST"]

robots=[(5,"ur5"),(3,"kr6"),(1,"irb_140")]

fig = go.Figure()

for robot in robots:
    tiempos=[]
    tiempos_fixed=[]
    print(robot[1])

    for planner in planners:

        cur.execute('SELECT time FROM runs WHERE request_planner_id="%s" AND experimentid=%d' % (planner,robot[0]))
        rows = cur.fetchall()
        lista=[]

        for row in rows:
            lista.append(row[0])

        data=np.array(lista)
        print(planner,"time mean:", np.mean(data))
        tiempos.append(np.mean(data))

        outliers = []
        def detect_outliers_iqr(data):
            data = sorted(data)
            q1 = np.percentile(data, 25)
            q3 = np.percentile(data, 75)
            # print(q1, q3)
            IQR = q3-q1
            lwr_bound = q1-(1.5*IQR)
            upr_bound = q3+(1.5*IQR)
            # print(lwr_bound, upr_bound)
            for i in data:
                if (i<lwr_bound or i>upr_bound):
                    outliers.append(i)

            return outliers# Driver code

        outliers = detect_outliers_iqr(data)
        print("Outliers from IQR method: ", outliers)

        if len(outliers)>0:
            # Computing 10th, 90th percentiles and replacing the outliers
            tenth_percentile = np.percentile(data, 10)
            ninetieth_percentile = np.percentile(data, 90)
            print("diezcentil:",tenth_percentile,"noventancentil:",ninetieth_percentile)
            outliers = np.where(outliers<tenth_percentile, tenth_percentile, outliers)
            outliers = np.where(outliers>ninetieth_percentile, ninetieth_percentile, outliers)
            print("capped values:",outliers)

            data=np.minimum(data,ninetieth_percentile)
            data=np.maximum(data,tenth_percentile)

        print(planner,"time new mean:", np.mean(data))
        tiempos_fixed.append(np.mean(data))
        print("\n")

    fig.add_trace(go.Scatterpolar(
          # r=tiempos,
          r=tiempos_fixed,
          theta=planners,
          fill='toself',
          name=robot[1]
    ))

fig.update_layout(
  title="Mean trayectory computation time",
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

fig.write_html("tiempo.html")

fig.show()
