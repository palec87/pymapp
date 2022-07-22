import numpy as np
from scipy.optimize import fsolve
import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots

hide_cont1_class = 'hide-cont-1'


def quad_pizza(server):
    '''
    draw proportional pizza sizes (including edges),
    and plot the difference in areas base on diameter
    '''
    dash_app = Dash(
        __name__,
        server=server,
        routes_pathname_prefix='/demo/app003/',
        external_stylesheets=[
            '/static/style-dash.css'],
        external_scripts=[
            "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js",
            ],
    )

    dash_app.layout = html.Div([
        html.H2(['Imagine you go for a pizza with a friend. \
            The offer is clear:'], style={'font-weight': 'bold'}),
        html.Ol([
            html.Li([
                'One larger pizza costs the same as two smaller ones.'
                ]),
            html.Li([
                'You know (select with a slider) by how many cms\
                has the bigger pizza larger diameter.'
                ]),
            html.Li([
                'You want to decide at which diameter (d), it pays off\
                to share one bigger pizza rather than\
                having two smaller pizzas separately'
                ]),
            html.Li([
                'Additionally you can discard some thickness of the\
                dry edge of the pizzas, which you might not like.'
                ]),
        ], className="nums"),
        html.Button(
            id='hide1-button',
            children=['Figure notes'],
            type="button", className="collapsible"),

            # collapsible content
            html.Div(id='hide-cont-1', children=[
                html.Ul([
                    html.Li(['Left graphic shows relative scales of your pizzas\
                        based on your slider values if diameter of the smaller\
                        one is quite standard 20cm.']),
                    html.Li([
                        'Right graph shows areas of ',
                        html.Span(['two small pizzas'],
                                  style={'color': 'red'}),
                        ' and ',
                        html.Span(['one large pizza'],
                                  style={'color': 'blue'}),
                        ', together with the calculated difference in areas '
                    ]),
                ], style={'list-style-type': 'circle'}),
            ], className='hide-cont-1'),

        # TODO: because latex does not work here.
        # html.Button(
        #     id='hide2-button',
        #     children=['Equations'],
        #     type="button", className="collapsible"),
        #     html.Div(id='hide-cont-2', children=[
        #         html.Ul(children=[
        #             html.Li([r'$\sqrt{(n_\text{c}(t|{T_\text{early}}))}$']),
        #             html.Li(['Right graph shows areas of ']),
        #             ], style={'list-style-type': 'circle'}),
        #     ], className='hide-cont-1'),

        # Graph
        dcc.Graph(id='pizza_areas'),

        # sliders
        html.P(['Larger pizza has diameter greater by [cm]:']),
        dcc.Slider(
            id='slider_diff',
            min=1.0,
            max=15,
            step=0.5,
            marks=list(range(15)),
            value=5.0,
            tooltip={"placement": "bottom", "always_visible": True},
        ),

        html.P(['Thickness of the edge of pizzas to discard [cm]']),
        dcc.Slider(
            id='slider_edge',
            min=0.0,
            max=5,
            step=0.2,
            marks={i: '{}'.format(float(i)) for i in range(25)},
            value=1.0,
            tooltip={"placement": "bottom", "always_visible": True},
        ),
    ], className='dash-area--main')

    @dash_app.callback(
        Output('hide-cont-1', 'className'),
        Input('hide1-button', 'n_clicks'),
        State('hide-cont-1', 'className'),
        prevent_initial_call=True,
    )
    def hide1(n_clicks, curr_classes):
        if 'active' in curr_classes:
            return hide_cont1_class
        return hide_cont1_class + 'active'

    # @dash_app.callback(
    #     Output('hide-cont-2', 'className'),
    #     Input('hide2-button', 'n_clicks'),
    #     State('hide-cont-2', 'className'),
    #     prevent_initial_call=True,
    # )
    # def hide2(n_clicks, curr_classes):
    #     if 'active' in curr_classes:
    #         return hide_cont1_class
    #     return hide_cont1_class + 'active'

    @dash_app.callback(
        Output('pizza_areas', 'figure'),
        Input('slider_diff', 'value'),
        Input('slider_edge', 'value'),
    )
    def update_graph(diff, edge):
        d = np.linspace(0, 50, 101)
        y_small = 2*np.pi*((d-2*edge)/2)**2
        y_big = np.pi*((d + diff-2*edge)/2)**2
        diff_area = y_small-y_big
        roots = fsolve(area_diff, args=(diff, edge), x0=1000)

        small_win, big_win = [], []
        for idx, val in enumerate(diff_area):
            if val > 0:
                small_win.append(idx)
            else:
                big_win.append(idx)

        fig = go.Figure()
        fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('pizza shapes for d=20', 'Pizza areas'),
                column_widths=[0.4, 0.58],
                horizontal_spacing=0.15
                )
        fig.update_layout(
            margin=dict(
                l=20,
                r=20,
                b=50,
                t=50,
                pad=4
            ),)
        # left plot, pizza shapes for d=20
        d_small = 20
        d_big = d_small+diff
        fig.add_shape(
            type="circle",
            xref="x", yref="y",
            x0=0, y0=0,
            x1=d_small, y1=d_small,
            line_color="red",
            fillcolor="SandyBrown"
        )
        fig.add_shape(
            type="circle",
            xref="x", yref="y",
            x0=0, y0=d_small+2,
            x1=d_small, y1=2*d_small+2,
            line_color="red",
            fillcolor="SandyBrown"
        )
        fig.add_shape(
            type="circle",
            xref="x", yref="y",
            x0=d_small, y0=d_small+1-d_big/2,
            x1=d_small+d_big, y1=d_small+1+d_big/2,
            line_color="red",
            fillcolor="SandyBrown"
        )

        # include edges
        fig.add_shape(
            type="circle",
            xref="x", yref="y",
            x0=edge, y0=edge,
            x1=d_small-edge, y1=d_small-edge,
            line_color="red",
            fillcolor="OrangeRed"
        )
        fig.add_shape(
            type="circle",
            xref="x", yref="y",
            x0=edge, y0=d_small+2+edge,
            x1=d_small-edge, y1=2*d_small+2-edge,
            line_color="red",
            fillcolor="OrangeRed"
        )
        fig.add_shape(
            type="circle",
            xref="x", yref="y",
            x0=d_small+edge, y0=d_small+1-d_big/2+edge,
            x1=d_small+d_big-edge, y1=d_small+1+d_big/2-edge,
            line_color="blue",
            fillcolor="RoyalBlue"
        )
        fig.add_trace(
            go.Scatter(
                x=[d_small/2, d_small+d_big/2],
                y=[0, d_small+1-d_big/2],
                mode='text',
                showlegend=False,
                text=['small', 'large'],
                textfont=dict(
                    family="sans serif",
                    size=18,
                    color='black'
                    )
                ), row=1, col=1)
        fig.update_traces(textposition="bottom center", row=1, col=1)
        if edge > 0:
            fig.add_annotation(
                text="dry edge",
                xref="x", yref="y",
                x=d_small+d_big/2, y=d_small+1+d_big/2,
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=1.5,
                arrowcolor="black",
                ax=20,
                ay=-30,
                font=dict(
                    family="sans serif",
                    size=18,
                    color='black'
                    ),
                row=1, col=1)

        # right plot, areas
        fig.add_trace(
            go.Scatter(
                x=d,
                y=y_small,
                name='2x small',
                line={'color': 'red'},
                ), row=1, col=2)
        fig.add_trace(
            go.Scatter(
                x=d,
                y=y_big,
                name='1x large',
                line={'color': 'blue'},
                ), row=1, col=2)
        fig.add_trace(
            go.Scatter(
                x=d,
                y=diff_area,
                mode='lines',
                name='difference',
                line={'color': 'green', 'width': 2},
                ), row=1, col=2)
        fig.add_trace(
            go.Scatter(
                x=d[small_win],
                y=diff_area[small_win],
                mode='none',
                showlegend=False,
                line={'color': 'green'},
                fill='tozeroy',
                fillcolor='rgba(255, 0, 0, 0.3)',
                ), row=1, col=2)
        fig.add_trace(
            go.Scatter(
                x=d[big_win],
                y=diff_area[big_win],
                mode='none',
                name='large dominates',
                showlegend=False,
                fill='tozeroy',
                fillcolor='rgba(0, 0, 255, 0.3)',
                ), row=1, col=2)
        fig.update_yaxes(range=[-500, 2500], row=1, col=2)
        # right plot, solutions
        if len(roots) > 0:
            fig.add_trace(
                go.Scatter(
                    x=roots,
                    y=[0]*len(roots),
                    name='intersection',
                    mode='markers+text',
                    marker_color='rgba(20, 255, 20, .9)',
                    marker_line_width=2,
                    marker_size=10,
                    text=[round(roots[0], 2)],
                    textposition="top right",
                    textfont=dict(
                        family="sans serif",
                        size=21,
                        color='black'
                        )
                    ), row=1, col=2)
        fig.update_yaxes(
            scaleanchor="x",
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            scaleratio=1,
            row=1,
            col=1,
            )
        fig.update_xaxes(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            row=1,
            col=1,
            )
        fig.update_xaxes(
            title_text='pizza diameter [cm]', row=1, col=2,
            )
        fig.update_yaxes(
            title_text='pizza area [cm^2]', row=1, col=2,
            )

        return fig
    return dash_app.server


def area_diff(d, diff, edge):
    return 2*np.pi*((d-2*edge)/2)**2 - np.pi*((d + diff-2*edge)/2)**2


def quad_demand():
    # TODO: this should be dash dashboard
    return
