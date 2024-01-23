from jinja2 import Environment
import imgkit

html_location = 'cp_output.html'

timg = 'Template.png'

def createImg(text, img_location):

    content = dict(background_img_path = timg, description = text)

    HTML = """
    <!DOCTYPE html>
    <html>
    <head>

    <meta name="imgkit-format" content="png"/>
    <meta name="imgkit-orientation" content="Landscape"/>

    <style type="text/ccs">

    @font-face {
        font-family: OpenSans;
        src: url('OpenSans-ExtraBold.ttf');
    }

    .bottom-left {
        position: absolute;
        bottom: 250px;
        left: 100px;
        width: 60%;
        font-size:50px;
        font-family:'OpenSans';
        line-height: 100%;
        color: #000;
    }

    .top-right {
        position: absolute;
        top: 60px;
        right: 60px;
        width: 100px;
    }

    </style>
    <body>

    <div class="container">
        <img src="{{background_img_path}}" style="width:100%;">
        <div class="bottom-left"><p>"{{description}}"</p></div>
    </div>

    </body>
    </html>
    """

    #rendered_output = Environment().from_string(HTML).render(**content)

    #print(rendered_output)
    #with open(html_location, 'w', encoding='utf8') as f:
    #    f.write(rendered_output)
    
    options = {
        'xvfb': '',
        'encoding': 'UTF-8',
        "enable-local-file-access": None,
        'custom-header': [('Accept-Encoding', 'gzip')]
    }

    config = imgkit.config(wkhtmltoimage='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe')
    imgkit.from_file(html_location, img_location, options=options, configuration=config)

img = 'cp_out.jpg'
msg = 'sample message'

createImg(msg, img)