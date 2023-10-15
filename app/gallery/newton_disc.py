import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

size = 200
colors = [
    'rgb(0, 255, 0)',
    'rgb(0, 0, 255)',
    'rgb(75, 0, 130)',  # indigo
    'rgb(128, 0, 255)',  # violet
    'rgb(255, 0, 0)',
    'rgb(255, 128, 0)',
    'rgb(255, 255, 0)',
]
colors3 = [
    'rgb(255, 0, 0)',
    'rgb(0, 255, 0)',
    'rgb(0, 0, 255)',
]


fig = go.Figure(
            data=[go.Scatter(x=[0], y=[0],
                             marker=dict(
                                        color=colors[0],
                                        size=size,),)],
            layout=go.Layout(
                xaxis=dict(range=[-1, 1], autorange=False, visible=False),
                yaxis=dict(range=[-1, 1], autorange=False, visible=False),
                plot_bgcolor='rgba(0, 0, 0, 1)',
                paper_bgcolor='rgba(0, 0, 0, 1)',
                height=300,
                width=300,
                margin=dict(
                    l=10, r=10, b=0, t=0,
                ),
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label="Play",
                                  method="animate",
                                  args=[None, {"frame": {"duration": 200,
                                                         "redraw": False}}],
                                  ),
                             dict(label="Stop",
                                  method="animate",
                                  args=[[None],
                                        {"frame": {"duration": 0,
                                                   "redraw": False},
                                         "mode": "immediate"},
                                        ],
                                  ),
                             ])]
            ),
            frames=[
                go.Frame(
                    data=[
                        go.Scatter(x=[0],
                                   y=[0],
                                   marker=dict(
                                        color=colors[k % len(colors)],
                                        size=size,),)]) for k in range(100)],

        )

fig3 = go.Figure(
            data=[go.Scatter(x=[0], y=[0],
                             marker=dict(
                                        color=colors3[0],
                                        size=size,),)],
            layout=go.Layout(
                xaxis=dict(range=[-1, 1], autorange=False, visible=False),
                yaxis=dict(range=[-1, 1], autorange=False, visible=False),
                plot_bgcolor='rgba(0, 0, 0, 1)',
                paper_bgcolor='rgba(0, 0, 0, 1)',
                height=300,
                width=300,
                margin=dict(
                    l=10, r=10, b=0, t=0,
                ),
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label="Play",
                                  method="animate",
                                  args=[None, {"frame": {"duration": 200,
                                                         "redraw": False}}],
                                  ),
                             dict(label="Stop",
                                  method="animate",
                                  args=[[None],
                                        {"frame": {"duration": 0,
                                                   "redraw": False},
                                         "mode": "immediate"},
                                        ],
                                  ),
                             ])]
            ),
            frames=[
                go.Frame(
                    data=[
                        go.Scatter(x=[0],
                                   y=[0],
                                   marker=dict(
                                        color=colors3[k % len(colors3)],
                                        size=size,),)]) for k in range(100)],

        )


values = [100]*7

fig_nc = go.Figure(
    data=[go.Pie(values=values, marker_colors=colors,
                 )],
    layout=go.Layout(
        xaxis=dict(range=[-1, 1], autorange=False, visible=False),
        yaxis=dict(range=[-1, 1], autorange=False, visible=False),
        plot_bgcolor='rgba(0, 0, 0, 1)',
        paper_bgcolor='rgba(0, 0, 0, 1)',
        height=300,
        width=300,
        showlegend=False,
        margin=dict(
            l=10, r=10, b=0, t=0,
        ),
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None, {"frame": {"duration": 200,
                                                 "redraw": False}}],
                          ),
                     dict(label="Stop",
                          method="animate",
                          args=[[None], {"frame": {"duration": 0,
                                                   "redraw": False},
                                         "mode": "immediate"}],
                          ),
                     ])]
    ),
    frames=[go.Frame(data=[go.Pie(values=values,
                                  marker_colors=colors)]) for k in range(100)],
)
fig_nc.update_traces(textinfo='none')


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
            'Newton disc demonstrates that 7 principle colors of the \
            rainbow combine into a white light. The colors are: green\
            , blue, indigo, violet, red, orange and yellow.  \
            Why this is supposed to work is because an image persists in the\
            brain \
            for approximatelly 1/16 of a second, due to the ',
            html.A('vision persistence',
                   href="https://en.wikipedia.org/wiki/Persistence_of_vision",
                   target="_blank"),
            ' effect.',
            html.P('Unfortunately the result is underwhelming, compared \
                   to the one you can build yourself at home. \
                   I blame the refresh rate of the computer screen, \
                   which is only 50 Hz.',),
            html.H4('Food for thought:'),
            html.Ol([html.Li('Do you know what is Hz, and how many \
                             images shown per second it corresponds to?'),
                     html.Li('Do you know what is the minimum frequency \
                             (in Hz) \
                             for the images to be percieved as motion\
                             pictures, \
                             ie. a movie?'),
                     html.Li('If the above is true, an image stays in your \
                             brain for 1/16 s and you need to cycle through \
                             7 colors in order to perceive white color, \
                             what frame rate (frequency of changing images)\
                             you need. Is it higher \
                             than 50 Hz?'),
                     ]),
            ],
            style={
                "width": "90%",
                "text-align": "justify",
            }),

        # Graph 1
        html.H1('DO not use if you are epileptic.'),
        html.P('You must stop the animation before changing the Frame rate.'),
        html.Div([
            html.Div([
                html.H3('7 colors, full circle.'),
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
            ), style={'width': '60%',
                      'display': 'inline-block',
                      }),
        ], style={'width': '100%', 'display': 'inline-block'}),

        # Graph 2, only three colors
        html.Div([
            html.Div([
                html.H3('3 colors, full circle.'),
                # left graph in separate div element
                dcc.Graph(figure=fig3, id='newton_circle2')
            ], style={'width': '50%', 'display': 'inline-block'}),

            # title of size 4
            html.H4('Frame rate'),
            # div element which contains the slider
            html.Div(dcc.Slider(
                5, 200, step=5,
                id='fr_slider2',
                value=5, marks={5: '5', 100: '100', 200: '200'},
                tooltip={"placement": "bottom", "always_visible": True},
            ), style={'width': '60%',
                      'display': 'inline-block',
                      }),
        ], style={'width': '100%', 'display': 'inline-block'}),

        # Graph 3, only three colors
        html.Div([
            html.Div([
                html.H3('Full Newton circle.'),
                # left graph in separate div element
                dcc.Graph(figure=fig_nc, id='newton_circle3')
            ], style={'width': '50%', 'display': 'inline-block'}),

            # title of size 4
            html.H4('Frame rate'),
            # div element which contains the slider
            html.Div(dcc.Slider(
                5, 200, step=5,
                id='fr_slider3',
                value=5, marks={5: '5', 100: '100', 200: '200'},
                tooltip={"placement": "bottom", "always_visible": True},
            ), style={'width': '60%',
                      'display': 'inline-block',
                      }),
        ], style={'width': '100%', 'display': 'inline-block'}),


    ], className='dash-area--main')

    @dash_app.callback(
        Output('newton_circle', 'figure'),
        Input('fr_slider', 'value'),
    )
    def update_graph(frame_rate):
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    buttons=[
                        dict(
                            label="Play",
                            method="animate",
                            args=[None,
                                  {"frame": {"duration": 1000 / frame_rate,
                                             "redraw": False},
                                   }],
                             ),
                        dict(
                            label="Stop",
                            method="animate",
                            args=[[None],
                                  {"frame": {"duration": 0,
                                             "redraw": False},
                                   "mode": "immediate",
                                   }],
                            execute=True,
                            ),
                                ])],
            )
        return fig

    @dash_app.callback(
        Output('newton_circle2', 'figure'),
        Input('fr_slider2', 'value'),
    )
    def update_graph2(frame_rate):
        fig3.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    buttons=[
                        dict(
                            label="Play",
                            method="animate",
                            args=[None,
                                  {"frame": {"duration": 1000 / frame_rate,
                                             "redraw": False},
                                   }],
                             ),
                        dict(
                            label="Stop",
                            method="animate",
                            args=[[None],
                                  {"frame": {"duration": 0,
                                             "redraw": False},
                                   "mode": "immediate",
                                   }],
                            execute=True,
                            ),
                                ])],
            )
        return fig3

    @dash_app.callback(
        Output('newton_circle3', 'figure'),
        Input('fr_slider3', 'value'),
    )
    def update_graph3(frame_rate):
        values = [100]*7
        fig_nc.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    buttons=[
                        dict(
                            label="Play",
                            method="animate",
                            args=[None,
                                  {"frame": {"duration": 1000 / frame_rate,
                                             "redraw": True},
                                   }],
                             ),
                        dict(
                            label="Stop",
                            method="animate",
                            args=[[None],
                                  {"frame": {"duration": 0,
                                             "redraw": False},
                                   "mode": "immediate",
                                   }],
                            execute=True,
                            ),
                                ])],
            )
        fig_nc.frames = [go.Frame(
                        data=[
                            go.Pie(values=values,
                                   marker_colors=colors[k % 7:] + colors[:k % 7]),
                                ]) for k in range(100)]
        return fig_nc
    return dash_app.server
