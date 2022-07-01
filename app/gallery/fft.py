import numpy as np
from scipy import signal, fft
import json
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def fft_intro():
    line = create_square_f()
    return create_plot(line, 20)


def create_plot(func, max_harmonics):
    fig = go.Figure()
    fig = make_subplots(rows=1, cols=2)

    fig.add_trace(
        go.Scatter(
            x=func[0],
            y=func[1],
            name='square function',
            line={'color': 'red'},
            visible=True,
            showlegend=True
            ), row=1, col=1)

    for step in range(1, max_harmonics):
        fig.add_trace(
            go.Scatter(
                visible=False,
                x=func[0],
                y=ft_series_square(func[0], 1, step+1),
                name='FT sine series',
                line={'color': 'blue'},
                ), row=1, col=1)

        x, y = do_fft(func[0], ft_series_square(func[0], 1, step+1))
        fig.add_trace(
            go.Scatter(
                visible=False,
                x=x,
                y=y,
                name='FT amplitudes',
                line={'color': 'green'},
                ), row=1, col=2)

    fig.data[0].visible = True
    fig.data[1].visible = True
    fig.data[2].visible = True
    fig.update_layout(yaxis_range=[-1.5, 1.5])
    fig.update_xaxes(range=[0, 40], row=1, col=2)

    # slider
    steps = []
    counter = 1
    for i in range(1, len(fig.data), 2):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)}],  # layout attribute
            label=str(counter),
                    )
        step["args"][0]["visible"][0] = True
        # Toggle i'th trace to "visible"
        steps.append(step)
        step["args"][0]["visible"][i:i+2] = [True, True]
        counter += 1

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Number of harmonics: "},
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(
        sliders=sliders
        )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def ft_series_square(x_axis, freq, n_harmonics):
    # first create array of zeros, where I am going to add the sin terms
    f_values = np.zeros(len(x_axis))
    # k is the k from the formula above
    for k in range(1, n_harmonics):
        # for higher frequencies, adding the sin term to my existing values
        f_values = f_values + np.sin(2*np.pi*(2*k-1)*freq*x_axis)/(2*k-1)
    return f_values * 4 / np.pi  # multiplying only once the whole thing


def do_fft(x, f):
    t_step = abs(x[1] - x[0])
    f_fft = fft.fft(f)
    x_fft = fft.fftfreq(len(x), t_step)[:len(x)//2]
    return x_fft, 2.0/len(x) * np.abs(f_fft[0:len(x)//2])


def create_square_f():
    t = np.linspace(0, 2, 500, endpoint=False)
    f = signal.square(2 * np.pi * t)
    return (t, f)
