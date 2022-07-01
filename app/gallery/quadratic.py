import numpy as np
import json
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def quad_pizza():
    '''
    draw proportional pizza sizes (including edges),
    and plot the difference
    '''
    return create_plot()


def quad_demand():
    # TODO: this should be dash dashboard
    return


###########
# helpers #
###########
def create_plot():
    # data
    d = np.linspace(0, 50, 101)
    d_diff = np.linspace(1, 20, 20)
    # f = 2*np.pi*(d/2)**2 - np.pi*((d + d_diff)/2)**2

    fig = go.Figure()
    fig = make_subplots(rows=1, cols=2)

    # this will be pizza shapes
    fig.add_trace(
        go.Scatter(
            x=[1, 2, 3],
            y=[1, 4, 9],
            name='quad function',
            line={'color': 'red'},
            visible=True,
            showlegend=True
            ), row=1, col=1)

    for diff in d_diff:
        fig.add_trace(
            go.Scatter(
                visible=False,
                x=d,
                y=2*np.pi*(d/2)**2 - np.pi*((d + diff)/2)**2,
                name='Area diff',
                line={'color': 'blue'},
                ), row=1, col=2)

        # x,y = do_fft(func[0], ft_series_square(func[0], 1, step+1))
        # fig.add_trace(
        # go.Scatter(
        #     visible=False,
        #     x=x,
        #     y=y,
        #     name='FT amplitudes',
        #     line={'color':'green'},
        #     ), row=1, col=2)

    # three sliders
    # slider 1: diameter diff
    steps = []
    counter = 1
    for i in range(1, len(fig.data), 1):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                  ],  # layout attribute
            label=str(counter),
            )
        step["args"][0]["visible"][i] = [True]
        steps.append(step)
        counter += 1

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Difference in diameter: "},
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(
        sliders=sliders
        )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
