def grapher(df):
  fig = go.Figure()
  theta = list(df.iloc[:,19:28])
  r = []
  for i in range(19,28):
    r.append(df.loc[0][i])
  fig.add_trace(go.Scatterpolar(
    r = r,
    theta=theta,
    fill = 'toself',
    name = 'input song'
  ))
  r1 = []
  for i in range(19,28):
    r1.append(df.loc[0][i])
  fig.add_trace(go.Scatterpolar(
          r = r1,
    theta=theta,
    fill = 'toself',
    name='Recommended Song'
  ))
  x = fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 1]
    )),
  showlegend=False
  )
  return x.show()