import PySimpleGUI as sg
from nbimporter import NotebookLoader
import existingAccount, dataBaseUtil, encryptDecrypt, json, base64

def manageDataLoaded(dataLoaded):
    toReturn = []
    for item in dataLoaded:
        toReturn.append(item['web'])
    return toReturn
    
def storeNewAccount(newAccount,userId):
    web = newAccount[2]
    passToEncrypt = newAccount[1]
    user = newAccount[0]
    decryptionResult = encryptDecrypt.encryptPass(passToEncrypt)
    toStoreInServer = decryptionResult[1]
    encryptedPass = decryptionResult[0]
    IV, HashedKey, privateKey = toStoreInServer
    id = dataBaseUtil.insert(userId, web, privateKey, HashedKey, IV )
    save_to_json(base64.b64encode(encryptedPass).decode("utf-8"), user, web, id, "accounts.json")

def recoverAccount(data, valuesLoadedFromDB):
    id, user, web, encryptedPass = data['id'], data['user'], data['web'], data['encryptedPass']
    encryptedKey,hashedKey,IV = "","",""
    for item in valuesLoadedFromDB:
        if(str(item["_id"]) == id):
            print(item)
            encryptedKey, hashedKey, IV= item["EncryptedKey"],item["HashedKey"],item["IV"]
    passw = encryptDecrypt.decryptPass(base64.b64decode(encryptedPass), IV, hashedKey, encryptedKey)
    return [user, passw, web]

def save_to_json(encryptedPass, user, web, id, filename):
    data = {'id': id, 'user': user, 'web': web, 'encryptedPass':encryptedPass}
    with open(filename, 'r') as f:
        data_list = json.load(f)
    data_list.append(data)

    with open(filename, 'w') as f:
        json.dump(data_list, f, indent = 4)



def read_json(position):
    with open("accounts.json") as f:
        data = json.load(f)
    
    if position < 0 or position >= len(data):
        raise ValueError(f"The position has to be in range [0, {len(data) - 1}].")
    
    return data[position]


#function to manage the password list
def manageWindow(userId):
    valuesLoadedFromDB = dataBaseUtil.searchByUserID(userId) if dataBaseUtil.searchByUserID(userId) != ["newUser"] else ["Add new passwords :)"]
    valuesToShow = manageDataLoaded(valuesLoadedFromDB)

    # Define the layout of the window
    sg.theme("DarkBlue")
    layout = [
        [sg.Listbox(values=valuesToShow, enable_events=True, size=(80, 20), key="list", font=('Arial', 16))],
        [sg.Button("New entry")]
    ]

    # Create window
    window = sg.Window("Passwords stored", layout, size=(600, 350))

    # Manage window
    while True:
        event, values = window.read()
        # If new entry is pressed...
        if event == "New entry":
            # Open the window to store new accounts
            newAccountWindow = NotebookLoader().load_module('newAccount')
            arrayNewEntry = newAccountWindow.manageWindow()
            # If the new element is added we show it in the list
            if arrayNewEntry is not None and arrayNewEntry != "":
                storeNewAccount(arrayNewEntry, userId)
                valuesToShow.append(arrayNewEntry[2])
                window["list"].update(values=valuesToShow)
        if values is not None and event == "list":
            valuesLoadedFromDB = dataBaseUtil.searchByUserID(userId) if dataBaseUtil.searchByUserID(userId) != ["newUser"] else ["Add new passwords :)"]
            listbox = window['list']
            data = read_json(listbox.get_indexes()[0])
            user, passw, web = recoverAccount(data, valuesLoadedFromDB)
            existingAccount.manageWindow(user, passw, web)
        # If the window is closed end the execution
        if event == sg.WINDOW_CLOSED:
            break

    # Cerramos la ventana
    window.close()

#TODO FUNCIÓN QUE RECIBA VALORES Y LOS COLOQUE EN LA LISTA

if __name__ == '__main__':
    manageWindow("114278233747573671006")

