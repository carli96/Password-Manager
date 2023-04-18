import PySimpleGUI as sg
import passGenerator
import EncryptDecrypt
import maskpass


# function to generate the new account window


def window(user, passw, web):
    sg.theme("DarkBlue")
    layout = [[sg.Text('WebPage:')],
              [sg.Text(web)],
              [sg.Text('User:')],
              [sg.Text(user)],
              [sg.Text('Password:')],
              [sg.Text(passw)]]
    window = sg.Window('Window Title', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break

    window.close()


if __name__ == '__main__':
    window()
