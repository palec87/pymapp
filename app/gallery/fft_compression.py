import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
from PIL import Image

import sys,os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.pardir))

hide_cont1_class = 'hide-cont-1'


def compress_fourier(server):
    dash_app = Dash(
        __name__,
        server=server,
        routes_pathname_prefix='/demo/app007/',
        external_stylesheets=[
            '/static/style-dash.css'],
        external_scripts=[
            "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js",
            ],
    )
    dash_app.layout = html.Div([
        html.Div(
            children=[
                html.P(['Here is a portrait of Sir Joseph Fourier \
                        (courtesy of ',
                        html.A(['gettyimages.com'],
                               href='https://www.gettyimages.com.au/detail/news-photo/engraved-portrait-of-french-mathematician-jean-baptiste-news-photo/169251384',
                               target='_blank', className='text'),
                        ').'],
                       style={'font-weight': 'bold'}),
                ],
        ),
        html.Img(src='/static/fig/fourier_greyscale.png',
                 alt='Portrait of Sir Joseph Fourier.',
                 style={
                    "width": "250px",
                    }),
        # html.P(children=[
        #     'If you want to check how simple Fourier series works, check the\
        #     FFT Introductory demo/notebook.',
        #     ], style={
        #             "width": "90%",
        #             "text-align": "justify",
        #             }),
        html.P(children=[
            'The original size of this image is 1619 x 2048 pixels. \
            In the 8 bit greyscale representation as shown here (every \
            pixel has intensity values between 0-255, because \
            255 = 2 ^ 8bits - 1), the memory necessary to store this image in bits is \
            1619 * 2048 * 8 = 3.31 MB \
            in the worst case scenario if all pixels would be 255 \
            (all white). In reality, it takes about 1.97 MB on my machine.'],
            style={
                "width": "90%",
                "text-align": "justify",
            }),
        html.P(children=[
            'Below on the left is the 2D Fourier transform of maestro \
            Fourier, i.e. represented by amplitudes of sines and cosines. The white \
            color represents high amplitude of particular frequency. \
            The center of the image corresponds to 0 frequency \
            (a constant) and usually dominates. \
            Further from the center will be higher frequencies, which contain \
            finer image details. Note that since the FT is \
            symmetric, the 2D FT is symmetric too.\
            '
        ], style={
            "width": "90%",
            "text-align": "justify",
            }),
        html.P(children=[
            'Use sliders to adjust how many pixels are used to \
             inverse Fourier transform to get compressed original \
            image. Note that the full resolution image is most probably \
            limited in resolution by your screen. The reconstructed image \
            will have dimensions of your selected number of pixels. \
            This type of filtering is \
            also called low-pass filter, because we are throwing out high \
            frequencies of the FT.\
            '
        ], style={
            "width": "90%",
            "text-align": "justify",
            }),
        html.P(children=[
            'You can inspect the results by eye and quantify the saved disk space \
            using so called ',
            html.A(['compression ratio'],
                   href='https://en.wikipedia.org/wiki/Data_compression_ratio',
                   target='_blank', className='text'),
            '.',
        ], style={
            "width": "90%",
            "text-align": "justify",
            }),

        # Graph
        dcc.Graph(id='fourier_fft', ),

        # sliders
        html.P(['How many vertical pixels to take from the FFT image']),
        dcc.Slider(
            id='slider_vertical_pxs',
            min=16,
            max=2048,
            step=2,
            marks={i: '{}'.format(int(i)) for i in range(16, 2048, 100)},
            value=2000,
            tooltip={"placement": "bottom", "always_visible": True},
        ),

        html.P(['How many horizontal pixels to take from teh FFT image']),
        dcc.Slider(
            id='slider_horizontal_pxs',
            min=16,
            max=1619,
            step=2,
            marks={i: '{}'.format(int(i)) for i in range(16, 1619, 100)},
            value=1600,
            tooltip={"placement": "bottom", "always_visible": True},
        ),

    ], className='dash-area--main')
    print('loading...')
    # IMG_fft = np.load('app/static/fft_img_fourier.npy').view(complex)
    print(server)
    img = Image.open('static/fig/fourier_greyscale.png').convert('L')
#     IMG_fft = np.fft.fftshift(np.fft.fft2(img))
#     IMG_fft_to_plot = np.log(abs(IMG_fft))

#     @dash_app.callback(
#         Output('fourier_fft', 'figure'),
#         Input('slider_horizontal_pxs', 'value'),
#         Input('slider_vertical_pxs', 'value'),
#     )
#     def update_graph(npx_hor, npx_ver):
#         fig = go.Figure()
#         fig = make_subplots(
#                 rows=1, cols=2,
#                 subplot_titles=('FFT of Sir Fourier',
#                                 'Compressed Image',
#                                 ),
#                 column_widths=[0.48, 0.48],
#                 horizontal_spacing=0.15
#                 )
#         fig.update_layout(
#             margin=dict(
#                 l=10,
#                 r=10,
#                 b=30,
#                 t=70,
#                 # pad=4
#             ),)
#         fig.add_trace(px.imshow(
#                         IMG_fft_to_plot,
#                         color_continuous_scale='gray',
#                         binary_string=True,
#                         ).data[0],
#                       row=1, col=1)
#         fig.update_layout(coloraxis_showscale=False)
#         img_width = 1619
#         img_height = 2048
#         fig.update_xaxes(showgrid=False,
#                          range=(0, img_width),
#                          row=1, col=1)
#         fig.update_yaxes(showgrid=False,
#                          scaleanchor='x',
#                          range=(0, img_height),
#                          row=1, col=1)
#         # fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
#         fig.add_shape(
#             type="rect",
#             xref="x", yref="y",
#             x0=(img_width - npx_hor)//2, y0=(img_height - npx_ver)//2,
#             x1=(img_width + npx_hor)//2, y1=(img_height + npx_ver)//2,
#             line_color="blue",
#         )

#         # second version of this
#         nx = (img_width - npx_hor)//2
#         ny = (img_height - npx_ver)//2
#         print(nx, ny)

#         fig.add_trace(px.imshow(
#                         # calc_inverse_fft(IMG_fft[iy0:iy1, ix0:ix1]),
#                         calc_inverse_fft(IMG_fft[ny:-ny-1, nx:-nx-1]),
#                         color_continuous_scale='gray',
#                         binary_string=True,
#                         ).data[0],
#                       row=1, col=2)

#         # calculate compressed ratio
#         size_original = np.prod(IMG_fft.shape)  # product of rows*cols
#         size_compressed = np.prod(IMG_fft[ny:-ny-1, nx:-nx-1].shape)
#         saved_space = 100*(1-(size_compressed/size_original))

#         fig.update_xaxes(showgrid=False, range=(0, npx_hor), row=1, col=2)
#         fig.update_yaxes(showgrid=False, range=(0, npx_ver), row=1, col=2)
#         fig.update_layout(coloraxis_showscale=False)
#         fig.update_layout(title=f'saved space: {np.round(saved_space, 3)}% \
# (Zoom to some details to appreciate the resolution)')
#         return fig
    return dash_app.server


def calc_inverse_fft(img_fft):
    img_filt = np.fft.ifft2(np.fft.ifftshift(img_fft))
    return abs(np.flip(img_filt, axis=0))


# if __name__ == '__main__':
#     print(os.getcwd())
#     print(os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                              os.pardir))
