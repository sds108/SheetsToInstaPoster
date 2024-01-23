from html2image import Html2Image
from jinja2 import Environment

def screenshot(number, text):

  content = dict(title = number, description = text)

  HTML = """

    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@800&display=swap" rel="stylesheet">  
    <style>
    .container {
        position: relative;
        text-align: center;
        height: 1080px;
        width: 1080px;
    }
    .centered {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-family: sans-serif;
        font-size:46px;
        font-weight: 300;
    }
    .top-center {
        position: absolute;
        top: 66px;
        left: 50%;
        transform: translate(-50%, -50%);
        font-family: sans-serif;
        font-size:72px;
        font-weight: 800;
    }
	.bottom-left {
        position: absolute;
        top: 1014px;
        left: 45px;
        transform: translate(0%, -50%);
        font-family: sans-serif;
        font-size:40px;
        font-weight: lighter;
    }
    div {
        word-wrap: break-word;
        width: 1060px;
    }
    body {
        margin: 0;
        padding: 0;
    }
    </style>
    </head>
    <body>
    <div class="container">
        <img src='Test0.png' style="width:1080px;height:1080px;">
	    <div class="top-center"; style="text-align:center; color:white;"></div>
        <div class="centered"; style="text-align:center; color:black;"></div>
		<div class="bottom-left"; style="text-align:left; color:white;">@engineeringconfessionstcd</div>
    </div>
    </body>
    </html>
    
  """
  #rendered_output = Environment().from_string(HTML).render(**content)
  #with open('base.html', 'w', encoding='utf8') as f:
  #  f.write(rendered_output)

  hti = Html2Image()
  hti.screenshot(html_file='base.html', save_as=('test0' + '.png'), size=(1080, 1080))

screenshot('0', '')