import PySimpleGUI as sg
import passGenerator
import EncryptDecrypt
import maskpass


# function to generate the new account window


def window(user, passw, web):
    sg.theme("DarkBlue")
    column_to_centered = [[sg.Text('WebPage:', font=('Arial Bold', 20),
                                   size=20, expand_x=True,
                                   justification='center')],
                          [sg.Text(web, font=('Arial Bold', 14),
                                   size=20, expand_x=True,
                                   justification='center')],
                          [sg.Text('User:', font=('Arial Bold', 20),
                                   size=20, expand_x=True,
                                   justification='center')],
                          [sg.Text(user, font=('Arial Bold', 14),
                                   size=20, expand_x=True,
                                   justification='center')],
                          [sg.Text('Password:', font=('Arial Bold', 20),
                                   size=20, expand_x=True,
                                   justification='center')],
                          [sg.Text(passw, font=('Arial Bold', 14),
                                   size=20, expand_x=True,
                                   justification='center')],
                          [sg.Text(" ", expand_x=True,
                                   justification='center')],
                          [sg.Text(" ", expand_x=True,
                                   justification='center')],
                          [sg.Button("Cancel", auto_size_button=20)]]
    layout = [[sg.VPush()],
              [sg.Push(), sg.Column(column_to_centered,
                                    element_justification='c'), sg.Push()],
              [sg.VPush()]]
    window = sg.Window("Account Information", layout,
                       size=(500, 300))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break

    window.close()


if __name__ == '__main__':
    window()
