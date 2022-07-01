from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

import scipy.stats as stats
import scipy.constants as const


dc_water_volumes = {
    'all the oceans': 1.335e9,
    'Pacific ocean': 0.66988e9,
    'Atlantic ocean': 0.3104109e9,
    'Indian ocean': 0.264e9,
    'Southern ocean': 0.0718e9,
    'Arctic ocean': 0.01875e9}


def prob_pee_sea(server):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(
        server=server,
        routes_pathname_prefix='/demo/app002/',
        external_stylesheets=[
            '/static/style.css'
        ]
    )

    dash_app.layout = html.Div([
        html.P([
            'Imagine you have peed (in litres)'
        ]),

        html.P([
            dcc.Input(
                id="pee-vol",
                placeholder='Enter a value...',
                type='number',
                min=0.01,
                max=10,
                value=0.1,
                step=0.01
                )
            ], className='input-field'),

        html.P([
            'After that, you mix your pee perfectly across'
            ]),

        html.P([
            dcc.Dropdown(['all the oceans', 'Pacific ocean',
                          'Atlantic ocean', 'Indian ocean',
                          'Arctic ocean', 'Southern ocean'],
                         'all the oceans',
                         id='ocean_dropdown',
                         )
            ], className='input-field'),

        html.P([
            'The question is, when you draw the same volume of water back into a glass, \
            what is the chance to have more than'
            ]),

        html.P([
            dcc.Input(
                id="pee-guess",
                placeholder='Enter a value...',
                type='number',
                value=10,
                min=10,
                step=10
                )
            ], className='input-field'),

        html.P([
            'molecules of your own pee in the glass of water?'
            ]),


        dcc.Graph(id='pee_dist')
        ],)

    @dash_app.callback(
        Output('pee_dist', 'figure'),
        Input('ocean_dropdown', 'value'),
        Input('pee-vol', 'value'),
        Input('pee-guess', 'value')
    )
    def update_graph(ocean, vol_pee, guess):
        x, n, p = generate_pee_binom(vol_pee, dc_water_volumes[ocean], guess)
        y = stats.binom.pmf(x, n*1e-20, p*1e20)
        prob = 1-stats.binom.cdf(guess, n*1e-20, p*1e20)
        # labels
        fig = go.Figure(
            layout=go.Layout(
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title='Number of pee molecules',
                yaxis_title='Probability'
                )
            )
        fig.update_xaxes(showgrid=True, zeroline=False, gridcolor='LightGrey')
        fig.update_yaxes(showgrid=True, zeroline=False, gridcolor='LightGrey')
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                name='binomial probability'
                )
            )
        fig.add_trace(
            go.Scatter(
                x=x[x.index(guess):],
                y=stats.binom.pmf(x[x.index(guess):],
                                  n*1e-20,
                                  p*1e20),
                fill='tozeroy',
                text=str(round(prob, 3)),
                name='your prob: ' + str(round(prob, 3)),
                textfont=dict(
                    family="sans serif",
                    size=18,
                    color="crimson"
                    )
                )
            )
        return fig

    return dash_app.server


# helper functions ###
def generate_pee_binom(vol_pee, vol_sea, guess):
    '''vol_pee in litres'''
    km3_to_liters = 10000**3
    moles_per_liter = 1000/18.02
    n = vol_pee * moles_per_liter * const.Avogadro  # number of pee mol
    p = n/(vol_sea * km3_to_liters
           * moles_per_liter
           * const.Avogadro)  # probability of picking a pee molecule
    # generate reasonable x axis
    mean = int(n*p)
    x = list(range(
                max(
                    min(guess-50, mean-150),
                    0),
                max(guess+50, mean+150),
                1)
             )
    return (x, n, p)
