import PySimpleGUI as sg
import pyperclip

#TODO: meter un boton de mostrar contraseña y que quite los * (si se vuelve a pulsar que los vuelva a poner)
#TODO: meter un boton de copia, que copie en el portapapeles la contraeña aunque tenga ****

def pass_hide(passw):
    return "*"*len(passw)


def manageWindow(user, passw, web):
    sg.theme("DarkBlue")
    layout = [[sg.Text('WebPage')],
              [sg.InputText(key='web',default_text = web, disabled=True)],
              [sg.Text('User')],
              [sg.InputText(key='user',default_text = user, disabled=True)],
              [sg.Text('Password')],
              [sg.InputText(key='pass', password_char='*', disabled=True,default_text = passw)],
              [sg.Button("Copy password", key='copy'), sg.Cancel(), sg.Button("Show", key='show')]]
    window = sg.Window("Account Information", layout)
    visible = False

    while True:
        event, values = window.read()
        if event == 'show':
             if visible is False:
                window['show'].update("Hide")
                window['pass'].update(password_char="")
                visible = True
             else:
                window['show'].update("Show")
                window['pass'].update(password_char="*")
                visible = False
        if event == "copy":
            pyperclip.copy(passw)
        if event == sg.WIN_CLOSED or event == "Cancel":
            break

    window.close()


if __name__ == '__main__':
    manageWindow()
