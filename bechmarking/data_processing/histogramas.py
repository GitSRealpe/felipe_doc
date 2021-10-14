import sqlite3
import numpy as np
import plotly.graph_objects as go

from plotly.subplots import make_subplots

con = sqlite3.connect('benchmark.db')
cur = con.cursor()

# planners=["RRTConnect", "PRM", "RRT", "LazyPRM", "LBKPIECE", "BKPIECE", "KPIECE", "EST"]
# robots=[(1,"irb_140"),(3,"kr6"),(5,"ur5")]

planners=["RRTConnect", "PRM", "RRT", "LazyPRM", "LBKPIECE", "BKPIECE", "KPIECE", "EST"]
robots=[(1,"irb_140")]


for robot in robots:
    waypoints=[]
    waypoints_fixed=[]
    print(robot[1])

    for planner in planners:
        fig = make_subplots(rows=2, cols=1)

        cur.execute('SELECT waypoints FROM runs WHERE request_planner_id="%s" AND experimentid=%d AND success=1' % (planner,robot[0]))
        rows = cur.fetchall()
        lista=[]

        for row in rows:
            lista.append(row[0])

        data=np.array(lista)
        maxh=np.amax(data)
        minh=np.amin(data)

        trace0 = go.Histogram(x=data)

        # fig = px.histogram(data, nbins=10, range_x=[minh, maxh])
        # fig.update_traces(xbins=dict( # bins used for histogram
        #     size=5
        # ))
        # fig.show()

        print(planner,"waypoints mean:", np.mean(data))
        waypoints.append(np.mean(data))

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
            print("Diezcentil:",tenth_percentile,"Noventancentil:",ninetieth_percentile)
            # outliers = np.where(outliers<tenth_percentile, tenth_percentile, outliers)
            # outliers = np.where(outliers>ninetieth_percentile, ninetieth_percentile, outliers)
            # print("capped values:",outliers)

            data=np.minimum(data,ninetieth_percentile)
            data=np.maximum(data,tenth_percentile)

        print(planner,"waypoints new mean:", np.mean(data))
        waypoints_fixed.append(np.mean(data))
        print("\n")

        trace1 = go.Histogram(x=data, autobinx=False)

        fig.append_trace(trace0, 1, 1)
        fig.append_trace(trace1, 2, 1)

        # fig = px.histogram(data, nbins=10, range_x=[minh, maxh])
        fig.update_traces(
            xbins=dict( # bins used for histogram

                size=5
                ),
            name=planner, # name used in legend and hover labels
            )
        fig.update_xaxes(range=[minh, maxh])
        fig.show()



#
