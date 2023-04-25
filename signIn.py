import PySimpleGUI as sg
import os
import pathlib
import requests
import google.auth.transport.requests
import webbrowser
import passList
from flask import Flask, session, abort, redirect, request, Response, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol


# declare variables
userId = ""
app = Flask("Google Login App")
app.secret_key = "CodeSpecialist.com"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
client_secrets_file = os.path.join(pathlib.Path(
    __file__).parent, "nonExecutableFiles/client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

# manage if there has been a login
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

# route to manage the login process
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
    global userId
    userId = session["google_id"]
    endExecution()
    return Response(status=200)

# index
@app.route("/")
def index():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

# end the flask execution after recovering the password
def endExecution():
    request.environ.get('werkzeug.server.shutdown')()
    return 'flask is closed'

# -----------------------------------------------------

# Manages the login window
def manageWindow():
    global userId
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
    window = sg.Window("LogIn", layout, size=(
        715, 350), element_justification='c')

    # Start the loop
    while True:
        event, values = window.read()
        # If the "log in wth google" is pressed
        if event == "Log in with Google":
            url = "http://127.0.0.1:5000"
            # Open the URL in a new browser window/tab
            webbrowser.open_new(url)
            app.run(debug=False)
            window.close()
            passList.manageWindow(userId)

        if event == sg.WINDOW_CLOSED:
            break

    # Close windows
    window.close()