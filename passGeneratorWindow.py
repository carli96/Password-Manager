import PySimpleGUI as sg
import passGenerator

def manageWindow():
    sg.theme("DarkBlue")
    layout = [[sg.Text("Length", key="new")],
              [sg.Slider(range=(7, 20), default_value=10,
               expand_x=True, enable_events=True,
                         orientation='horizontal', key='-SL-')],
              [sg.Text("Numbers", key="tx_numbers")],
              [sg.Checkbox('', key="n_numbers", default=True)],
              [sg.Text("Capital letters", key="tx_cp")],
              [sg.Checkbox('', key="cl", default=True)],
              [sg.Text("Special characters", key="tx_sp")],
              [sg.Checkbox('', key="sp", default=True)],
              [sg.Submit(), sg.Cancel()]]
    window = sg.Window("PasswordGenerator", layout, modal=True, no_titlebar=True)
    while True:
        event, values = window.read()
        # Lets you select what kind of characters to add
        if values is not None:
            passWordLength = values['-SL-']
            n_numbers = values["n_numbers"]
            cl = values["cl"]
            sp = values["sp"]
        
        if event == "Exit" or event == "Cancel":
            break
        # Submits the password just generated
        if event == "Submit":
            password = passGenerator.generatePassword(int(passWordLength),
                                                        int(passWordLength)/3 if cl else 0,
                                                        int(passWordLength)/3 if n_numbers else 0,
                                                        int(passWordLength)/3 if sp else 0)
            window.close()
            return password

    window.close()