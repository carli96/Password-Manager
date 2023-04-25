import PySimpleGUI as sg
from nbimporter import NotebookLoader
import existingAccount, dataBaseUtil, encryptDecrypt, json, base64

# Function where the data is loaded from the DB and appends it to the array that will be showd in the ListBox
def manageDataLoaded(dataLoaded):
    toReturn = []
    for item in dataLoaded:
        toReturn.append(item['web'])
    return toReturn

# Stores the new account in the JSON and in the DB
def storeNewAccount(newAccount,userId):
    # First we get all the components needed
    user,passToEncrypt, web = newAccount
    decryptionResult = encryptDecrypt.encryptPass(passToEncrypt)
    encryptedPass, toStoreInServer = decryptionResult
    IV, HashedKey, privateKey = toStoreInServer
    
    # We insert the data in the DB
    id = dataBaseUtil.insert(userId, web, privateKey, HashedKey, IV )

    # we insert the datain the JSON    
    save_to_json(base64.b64encode(encryptedPass).decode("utf-8"), user, web, id, "nonExecutableFiles/accounts.json")

# It loads the accounts from the DB and returns the one that the user is looking for
def recoverAccount(data, valuesLoadedFromDB):
    id, user, web, encryptedPass = data['id'], data['user'], data['web'], data['encryptedPass']
    encryptedKey,hashedKey,IV = "","",""
    for item in valuesLoadedFromDB:
        if(str(item["_id"]) == id):
            encryptedKey, hashedKey, IV= item["EncryptedKey"],item["HashedKey"],item["IV"]
    passw = encryptDecrypt.decryptPass(base64.b64decode(encryptedPass), IV, hashedKey, encryptedKey)
    return [user, passw, web, id]

# Removes an account from everywhere
def removeAccount(id, valuesToShow):
    index = None
    index = remove_json(id)
    if index != None: 
        dataBaseUtil.remove(id)
        valuesToShow.pop(index)

# Exports all the accounts stored
def generateExport(valuesLoadedFromDB):
    output = []
    for i in range(len(valuesLoadedFromDB)):
        output.append(recoverAccount(read_json(i),valuesLoadedFromDB))
    # Create and open file to store accounts
    archive = open("passwordVaultExport.txt", "w")
    for element in output:
        archive.write(str(element) + "\n")

    archive.close()

#======================================== json utils ===========================================
# Stores data to JSON
def save_to_json(encryptedPass, user, web, id, filename):
    data = {'id': id, 'user': user, 'web': web, 'encryptedPass':encryptedPass}
    with open(filename, 'r') as f:
        data_list = json.load(f)
    data_list.append(data)

    with open(filename, 'w') as f:
        json.dump(data_list, f, indent = 4)

# Reads the JSON
def read_json(position):
    with open("nonExecutableFiles/accounts.json") as f:
        data = json.load(f)
    if position < 0 or position >= len(data):
        raise ValueError(f"The position has to be in range [0, {len(data) - 1}].")
    return data[position]

# Reads the JSON
def remove_json(id):
    data_list = None
    with open("nonExecutableFiles/accounts.json", 'r') as f:
        data_list = json.load(f)
    for i, element in enumerate(data_list):
        if element["id"] == id:
            data_list.pop(i)
            with open("nonExecutableFiles/accounts.json", 'w') as f:
                json.dump(data_list, f, indent = 4)
            return i


#===================================================================================
#function to manage the password list
def manageWindow(userId):
    valuesLoadedFromDB = dataBaseUtil.searchByUserID(userId) if dataBaseUtil.searchByUserID(userId) != ["newUser"] else ["Add new passwords :)"]
    valuesToShow = manageDataLoaded(valuesLoadedFromDB)

    # Define the layout of the window
    sg.theme("DarkBlue")
    layout = [
        [sg.Listbox(values=valuesToShow, enable_events=True, size=(80, 15), key="list", font=('Arial', 16))],
        [sg.Button("New entry"),sg.Button("Export Accounts", key='export')]
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
        # An element is selected from the list
        if values is not None and event == "list":
            valuesLoadedFromDB = dataBaseUtil.searchByUserID(userId) if dataBaseUtil.searchByUserID(userId) != ["newUser"] else ["Add new passwords :)"]
            listbox = window['list']
            data = read_json(listbox.get_indexes()[0])
            user, passw, web, id = recoverAccount(data, valuesLoadedFromDB)
            outputExistingAccount = existingAccount.manageWindow(user, passw, web)
            if(outputExistingAccount == 1):
                removeAccount(id, valuesToShow)
                window["list"].update(values=valuesToShow)  

        if event == "export":
            sg.popup_auto_close('WARNING a file with all your accounts will be generated, please, store it somwhere witthout internet connectio (a USB Drive for example)')
            valuesLoadedFromDB = dataBaseUtil.searchByUserID(userId) if dataBaseUtil.searchByUserID(userId) != ["newUser"] else ["Add new passwords :)"]
            generateExport(valuesLoadedFromDB)
            break

        # If the window is closed end the execution
        if event == sg.WINDOW_CLOSED:
            break
    window.close()
