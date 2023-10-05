import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import numpy as np


# Plotting #
############
def plot_slit(fig, d_slit):
    fig.add_shape(
        type="line",
        xref="x", yref="y",
        x0=0, y0=d_slit / 2, x1=0, y1=2,
        line=dict(
            color="Black",
            width=3,
        ),
                 )
    fig.add_shape(
        type="line",
        xref="x", yref="y",
        x0=0, y0=-d_slit / 2, x1=0, y1=-2,
        line=dict(
            color="Black",
            width=3,
        ),
                 )
    return fig


def prism_edges(fig, prism_in, d_slit_prism, prism_h, prism_angle):
    tip = (d_slit_prism, prism_in)

    left = (d_slit_prism - (prism_h * np.tan(prism_angle/2)),
            -(prism_h - prism_in),
            )
    right = (d_slit_prism + (prism_h * np.tan(prism_angle/2)),
             -(prism_h - prism_in),
             )
    fig.add_trace(go.Scatter(x=[tip[0], left[0], right[0], tip[0]],
                             y=[tip[1], left[1], right[1], tip[1]],
                             fill="toself",
                             name='prism'),)
    return [tip, left, right]


def plot_light_beam(fig):
    fig.add_shape(
        type="rect",
        xref="x", yref="y",
        x0=-1, y0=-1,
        x1=0, y1=1,
        line=dict(
            color="yellow",
            width=3,
        ),
        fillcolor="Yellow",
    )


def plot_screen(fig, d_slit_prism, d_prism_screen, y0, y1):
    x = d_slit_prism + d_prism_screen
    fig.add_shape(
        type="line",
        xref="x", yref="y",
        x0=x, y0=y0, x1=x, y1=y1,
        line=dict(
            color="Grey",
            width=3,
        ),
        opacity=0.3,
                 )


def angle2rad(angle):
    return angle * np.pi / 180


def rad2angle(angle):
    return angle * 180 / np.pi


def entry_point(prism_in, y, prism_angle):
    x = (prism_in - y) * np.tan(prism_angle/2)
    return (d_slit_prism - x, y)


def line_from2points(x1, y1, x2, y2):
    slope = (y2-y1) / (x2-x1)
    b = y1 - slope*x1
    return slope, b


def line_point_angle(x1, y1, angle):
    slope = np.tan(angle)
    b = y1 - slope * x1
    return slope, b


def intercept(slope1, b1, slope2, b2):
    A = np.array([[-slope1, 1], [-slope2, 1]])
    b = np.array([b1, b2])
    return np.linalg.solve(A, b)


def refraction(lam, mat1, mat2, alpha1):
    n1 = calc_n(lam, mat=mat1)
    n2 = calc_n(lam, mat=mat2)
    alpha2 = np.arcsin(n1 * np.sin(alpha1) / n2)
    return alpha2


def refraction_path_from_prism(mat, lam, prism, prism_in, prism_angle):
    points_x = []
    points_y = []

    p1 = entry_point(prism_in, 0, prism_angle)
    points_x.append(p1[0])
    points_y.append(p1[1])

    # from the slit to the prism, this return m, b
    m1, b1 = line_from2points(0, 0, p1[0], p1[1])

    angle1 = refraction(lam, mat1='vac', mat2=mat, alpha1=prism_angle/2)

    # total angle of second line
    angle_total = np.arctan(m1) + angle1 - prism_angle/2

    # equation of second line
    m2, b2 = line_point_angle(p1[0], p1[1], angle_total)

    # second prism wall
    m_prism2, b_prism2 = line_from2points(prism[0][0], prism[0][1],
                                          prism[2][0], prism[2][1])

    # intercept with the second prism wall
    p2 = intercept(m_prism2, b_prism2, m2, b2)
    points_x.append(p2[0])
    points_y.append(p2[1])

    # refraction on the second surface
    incidence_angle = abs(prism_angle/2) + abs(angle_total)
    angle2 = refraction(lam, mat1=mat, mat2='vac', alpha1=incidence_angle)

    # total angle of third line
    angle_total = -angle_total - angle2 + prism_angle/2

    # equation of third line
    m3, b3 = line_point_angle(p2[0], p2[1], angle_total)

    # intercept with the screen
    X = d_slit_prism + d_prism_screen
    p3 = [X, m3*X+b3]
    points_x.append(p3[0])
    points_y.append(p3[1])

    return points_x, points_y


prism_height = 5  # same sided triangle
d_slit = 0.1
d_slit_prism = 5
d_prism_screen = 15
n = 1.4
colors = ['rgb(128, 0, 255)',  # violet 400nm
          'rgb(75, 0, 130)',  # indigo  430nm
          'rgb(0, 0, 255)',   # 479
          'rgb(0, 255, 0)',   # 530
          'rgb(255, 255, 0)',  # 580
          'rgb(255, 128, 0)',  # 605
          'rgb(255, 0, 0)',    # 670
          ]
lambdas = [400, 430, 480, 530, 580, 605, 670]
names = ['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']


def calc_n(lam, mat):
    lam = lam/1000  # to um
    if mat == 'BK7':
        n = np.sqrt(1.03961212*lam**2/(lam**2 - 0.00600069867) +
                    0.231792344*lam**2/(lam**2 - 0.0200179144) +
                    1.01046945*lam**2/(lam**2 - 103.560653) + 1)
    elif mat == 'water':
        n = np.sqrt(5.666959820e-1*lam**2/(lam**2 - 5.084151894e-3) +
                    1.731900098e-1*lam**2/(lam**2 - 1.818488474e-2) +
                    2.095951857e-2*lam**2/(lam**2 - 2.625439472e-2) +
                    1.125228406e-1*lam**2/(lam**2 - 10.73842352) +
                    1)
    elif mat == 'vac':
        n = 1
    else:
        raise ValueError
    return n


def spectrometer(server):
    dash_app = Dash(
        __name__,
        server=server,
        routes_pathname_prefix='/demo/app009/',
        external_stylesheets=[
            '/static/style-dash.css'],
        external_scripts=[
            "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js",
            ],
    )
    dash_app.layout = html.Div([
        html.Div([
            html.P(children=[
                'Test your spectrometer design before building it. \
                Change prism material, position and shape of the prism \
                (top prism angle) to see \
                color dispersion through your prism. Do not forget to \
                zoom in to confirm the separation of the \
                colors outside and inside of the prism. Note, that \
                everything is in scale of centimeters. \
                ',
                html.H4('Food for thought:'),
                html.Ol([html.Li('From changing the material, which one does \
                                 have higher refractive index n, water or\
                                 BK7 glass?'),
                         html.Li('Is n higher for blue or red color?'),
                         html.Li('Why do the colors disappear for \
                                 a combination of BK7 glass and 65 degrees \
                                 prism angle?')]),
                ],
                style={
                    "width": "90%",
                    "text-align": "justify",
                }),

            ]),
        html.Div([
            # Graph
            html.Div([
                html.Div([
                    # left graph in separate div element
                    dcc.Graph(id='spectrometer')
                ],
                ),
            ], className='left-panel'),

            html.Div([
                html.H5('Material'),
                html.Div([
                    dcc.Dropdown(options={
                                    'BK7': 'glass (BK7)',
                                    'water': 'Water'},
                                 value='water',
                                 id='mat-dropdown'),
                    html.Div(id='dd-mat')
                ]),

                html.H5('prism in [cm]'),
                html.Div(
                    dcc.Slider(
                        0.1, 3, step=0.2,
                        id='slider_prism_in',
                        value=1, marks={0.1: '0.1', 1: '1', 3: '3'},
                        tooltip={"placement": "bottom",
                                 "always_visible": True},
                    ),
                ),

                html.H5('prism tip angle [degrees]'),
                html.Div(
                    dcc.Slider(
                        10, 70, step=5,
                        id='slider_prism_angle',
                        value=50, marks={10: '10', 30: '30', 60: '60'},
                        tooltip={"placement": "bottom",
                                 "always_visible": True},
                    ),
                ),

                ], className='right-panel'),
            ], className='grid-container dash-area--main'),


    ], className='dash-area--main')

    @dash_app.callback(
        Output('spectrometer', 'figure'),
        Input('slider_prism_in', 'value'),
        Input('slider_prism_angle', 'value'),
        Input('mat-dropdown', 'value'),
    )
    def update_graph(prism_in, prism_angle, material):
        prism_angle = angle2rad(prism_angle)
        fig = go.Figure()
        prism = prism_edges(fig, prism_in, d_slit_prism,
                            prism_height, prism_angle)

        p1 = entry_point(prism_in, 0, prism_angle)

        # from the slit to the prism
        line_from2points(0, 0, p1[0], p1[1])

        plot_light_beam(fig)
        plot_slit(fig, d_slit)

        # line0
        fig.add_trace(go.Scatter(x=[0, p1[0]],
                                 y=[0, p1[1]],
                                 line_color='rgb(255, 255, 0)',
                                 showlegend=False))

        # fig.add_trace(go.Scatter(x=[p1[0]], y=[p1[1]]))
        mn_y, mx_y = 1000, -1000
        for i in range(len(lambdas)):
            points_x, points_y = refraction_path_from_prism(
                                            mat=material,
                                            lam=lambdas[i],
                                            prism=prism,
                                            prism_in=prism_in,
                                            prism_angle=prism_angle)
            mn_y = min(points_y[-1], mn_y)
            mx_y = max(points_y[-1], mx_y)
            fig.add_trace(go.Scatter(x=points_x, y=points_y,
                                     line_color=colors[i],
                                     name=names[i],
                                     opacity=.5))

        plot_screen(fig, d_slit_prism, d_prism_screen, mn_y-1, mx_y+1)
        fig['layout'].update(width=500,
                             height=500,
                             autosize=False,
                             title=f'separation of two outmost colors: \
{np.round(abs(abs(mn_y)-abs(mx_y)), 2)} cm')
        # fig.update_xaxes(showgrid=False)
        # fig.update_yaxes(showgrid=False)
        fig.update_layout(coloraxis_showscale=False,
                          paper_bgcolor='rgba(201, 155,155, 0)',
                          plot_bgcolor='rgba(0, 0, 0, 0.05)',
                          margin=dict(
                                l=0,
                                r=0,
                                b=0,
                                t=30,),
                          )
        fig.update_yaxes(
            scaleanchor="x",
            scaleratio=1,
        )

        return fig
    return dash_app.server
