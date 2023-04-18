import PySimpleGUI as sg
import os
import pathlib
import requests
import google.auth.transport.requests
import webbrowser
from flask import Flask, session, abort, redirect, request, url_for, current_app
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from threading import Timer
from nbimporter import NotebookLoader

# declare variables
userId = ""
app = Flask("Google Login App")
app.secret_key = "CodeSpecialist.com"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = "709048093959-h458e98t1o2rgajm1h293jmv80nnt1ab.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(
    __file__).parent, "nonExecutableFiles/client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

#manage if there has been a login
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

#route to manage the login process
@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    userId = session["google_id"]
    return userId

#route to logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

#index
@app.route("/")
def index():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    redirect(authorization_url)
    closeWindow()
    return endExecution()

#function to closs the window 
def closeWindow():
    return """
    <html>
        <head>
            <title>Respuesta HTTP</title>
            <script>
                window.close();
            </script>
        </head>
        <body>
            <p>Respuesta HTTP recibida</p>
        </body>
    </html>"""

#end the flask execution after recovering the password
def endExecution():
    # Código a ejecutar
    request.environ.get('werkzeug.server.shutdown')()
    return 'flask is closed'


@app.route("/protected_area")
@login_is_required
def protected_area():
    return "Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"

# -----------------------------------------------------


def manageWindow():
    # Define layout
    sg.theme("DarkBlue")
    layout = [[sg.Text(text='Welcome to password vault',
                        font=('Arial Bold', 16),
                        size=20, expand_x=True,
                        justification='center')],
                        [sg.Button("Log in with Google")],
              [sg.Image('img/googleLogo.png',
                         expand_x=True, expand_y=True)]
              ]
    window = sg.Window("LogIn", layout, size=(715,350),element_justification='c')

    # Start the loop
    while True:
        event, values = window.read()
        # If the "log in wth google" is pressed
        if event == "Log in with Google":
            url = "http://127.0.0.1:5000"  
            # Open the URL in a new browser window/tab
            webbrowser.open_new(url)
            app.run(debug=False)
            passListWindow = NotebookLoader().load_module('PassList')
            window.close()
            passListWindow.manageWindow()
            # TODO comprobar si hay una entrada en la tabla con id = google_id
            # TODO si lo hay extraer los nombres de todas las cuentas que ha almacenado
            # TODO si no lo hay, crear una nueva entrada
            
        if event == sg.WINDOW_CLOSED:
            break

    # Close windows
    window.close()

# TODO FUNCIÓN QUE RECIBA VALORES Y LOS COLOQUE EN LA LISTA

'''
if __name__ == '__main__':
    manageWindow()
    # app.run(debug=True)
'''
