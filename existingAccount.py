import PySimpleGUI as sg
import pyperclip

#Manage the window where the data of an existing account is showed
def manageWindow(user, passw, web):
    sg.theme("DarkBlue")
    layout = [[sg.Text('WebPage')],
              [sg.InputText(key='web',default_text = web, disabled=True)],
              [sg.Text('User')],
              [sg.InputText(key='user',default_text = user, disabled=True)],
              [sg.Text('Password')],
              [sg.InputText(key='pass', password_char='*', disabled=True,default_text = passw)],
              [sg.Button("Copy password", key='copy'), sg.Cancel(), sg.Button("Show", key='show'),sg.Button("Remove", key='remove')]]
    window = sg.Window("Account Information", layout)
    visible = False

    while True:
        event, values = window.read()
        # Hides and show the password
        if event == 'show':
            if visible is False:
                window['show'].update("Hide")
                window['pass'].update(password_char="")
                visible = True
            else:
                window['show'].update("Show")
                window['pass'].update(password_char="*")
                visible = False
        # Copies the password to the paperclip
        if event == "copy":
            pyperclip.copy(passw)
        if event == "remove":
            window.close()
            return 1
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
    window.close()
