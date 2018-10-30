import dash
import dash_html_components as html
import base64
from pitally.camera import DummyCamera
from datetime import datetime


picture_prefix = "pitally"

app = dash.Dash()
cam = DummyCamera()

app.layout = html.Div([
    html.Div([], id = 'image_div'),
    html.Div([html.Button('Take picture', id='picture-button')])
])

@app.callback(
    dash.dependencies.Output('image_div', 'children'),
    [dash.dependencies.Input('picture-button', 'n_clicks_timestamp')])
def update_image_src(n_clicks_timestamp):
    if n_clicks_timestamp is None:
        return []
    print(n_clicks_timestamp)
    image = cam.capture(n_clicks_timestamp)
    image_str = 'data:image/jpeg;base64,{}'.format(image.decode())
    img = html.Img(id='image', src=image_str, height='500px', width='auto')

    out = html.A(children=img,
                href=image_str,
                download=image_name(timestamp=n_clicks_timestamp)
               )
    return [out]
#
#
def image_name(timestamp):
    s = timestamp//1000
    date = datetime.utcfromtimestamp(s).strftime('%Y-%m-%d_%H-%M-%S')
    ms = s % 1000
    out = '%s-%s.%03d.jpg' % (picture_prefix,date,ms)
    return out


if __name__ == '__main__':
    app.run_server(debug=True)

