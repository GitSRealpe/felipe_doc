# imports
import plotly.express as px
import plotly.graph_objects as go

# data
df = px.data.tips()

print(df)
# plotly setup
fig=go.Figure()

# a plotly trace for each subcategory
for i, smokes in enumerate(df['smoker'].unique()):
    df_plot=df[df['smoker']==smokes]

    fig.add_trace(go.Box(x=df_plot['time'], y=df_plot['total_bill'],
                         notched=True,
                         line=dict(color='black'),
                         #line=dict(color=colors[i]),
                         fillcolor='yellow',
                         #fillcolor=colors[i+4],
                         name='smoker=' + smokes))

# figure layout adjustments
fig.update_layout(boxmode='group', xaxis_tickangle=0)
fig.show()
