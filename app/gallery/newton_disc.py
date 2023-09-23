import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

size = 200
colors = ['rgb(0, 255, 0)',
            'rgb(0, 0, 255)',
            'rgb(75, 0, 130)',  # indigo
            'rgb(128, 0, 255)',  # violet
            'rgb(255, 0, 0)',
            'rgb(255, 128, 0)',
            'rgb(255, 255, 0)']


fig = go.Figure(
            data=[go.Scatter(x=[0], y=[0],
                             marker=dict(
                                        color=colors[0],
                                        size=size,),)],
            layout=go.Layout(
                xaxis=dict(range=[-1, 1], autorange=False, visible=False),
                yaxis=dict(range=[-1, 1], autorange=False, visible=False),
                plot_bgcolor='rgba(0,0,0, 0)',
                height=300,
                width=300,
                margin=dict(
                    l=10,
                    r=10,
                    b=0,
                    t=0,
                    # pad=4
                ),
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label="Play",
                                  method="animate",
                                  args=[None, {"frame": {"duration": 200, "redraw": False}}],
                                  ),
                             dict(label="Stop",
                                  method="animate",
                                  args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                                  ),
                            ])]
            ),
            frames = [go.Frame(data=[go.Scatter(x=[0], y=[0],
                                            marker=dict(
                                                        color=colors[k % 7],
                                                        size=size,),)]) for k in range(100)],

        )


def nd(server):
    dash_app = Dash(
        __name__,
        server=server,
        routes_pathname_prefix='/demo/app008/',
        external_stylesheets=[
            '/static/style-dash.css'],
        external_scripts=[
            "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js",
            ],
    )
    dash_app.layout = html.Div([
        html.P(children=[
            'Newton disc demonstrates that all the colors of the \
            rainbow combine into a white light. The colors are \
            in order: green, blue, indigo, violet, red, orange and yellow.  \
            '],
            style={
                "width": "90%",
                "text-align": "justify",
            }),

        # Graph
    html.H1('DO not use if you are epileptic.'),
    html.P('You must stop the animation before changing the Frame rate.'),
    
    html.Div([
        html.Div([
            # left graph in separate div element
            dcc.Graph(figure=fig, id='newton_circle')
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        # title of size 4
        html.H4('Frame rate'),
        # div element which contains the slider
        html.Div(dcc.Slider(
            5, 200, step=5,
            id='fr_slider',
            value=5, marks={5: '5', 100: '100', 200: '200'},
            tooltip={"placement": "bottom", "always_visible": True},
        ), style={'width': '60%', 'display': 'inline-block',}),
    ], style={'width': '100%', 'display': 'inline-block'}),
    
    
    ], className='dash-area--main')


    @dash_app.callback(
        Output('newton_circle', 'figure'),
        Input('fr_slider', 'value'),
    )
    def update_graph(frame_rate):
        fig.update_layout(
            updatemenus=[dict(
                        type="buttons",
                        buttons=[dict(label="Play",
                                    method="animate",
                                    args=[None, {"frame": {"duration": 1000 / frame_rate, "redraw": False}}],
                                    ),
                                dict(label="Stop",
                                    method="animate",
                                    args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                                    execute=True,
                                    ),
                                ])],
            )
        return fig
    return dash_app.server
