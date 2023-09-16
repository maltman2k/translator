
import PySimpleGUI as sg
import win32api
import pyautogui
import pyperclip
from googletrans import Translator
from gtts import gTTS
import os
from playsound import playsound

oldtext=''
MouseState="none"
translator = Translator()
print ("Translator started.....")



layout = [
          [sg.Checkbox("Enable Translation",default=True, key='-S1-',pad=(5, (5, 10))),sg.Checkbox("Enable Voice", key='-S2-',pad=(5, (5, 10)))],
          [sg.Multiline('Multiline\n', size=(95,25), key='-OUT-')],
          [sg.Button('OK'), sg.Button('Exit')]]

#sg.theme('DarkBlue1')
window = sg.Window('Translator', layout,keep_on_top=True,size=(700, 500))

while True:
    event, values = window.read(timeout = 100)

    if event == 'Exit' or event == sg.WIN_CLOSED:
        break
    
    if event == 'OK' :
        print ('Out of Loop')
        window['-OUT-'].update(values['-IN-'])


    if values["-S1-"] == True:

        # ------------- Translation Enabled
        if win32api.GetKeyState(0x01)<0: #if mouse left button is pressed
            if MouseState!="pressed":
                    print("Pressed")
                    MouseState="pressed"

        else: #if mouse left button is not pressed
                if MouseState=="pressed":
                    print("Released")
                    MouseState="none"
                    pyautogui.hotkey('ctrl', 'c')
                    try:
                         text = pyperclip.paste()
                    except:
                         print ('Error pasting text')
                    #pyperclip.copy('')
                    if text!=oldtext:
                        oldtext=text
                        if text != '' :
                            translation = translator.translate(text, dest='it')
                            print(translation.text)
                            window['-OUT-'].update(translation.text)
                            event, values = window.read(timeout = 10)

                            if values["-S2-"] == True:
                                
                                if len(translation.text) > 0:
                                    audio = gTTS(text=translation.text, lang="it", slow=False)
                                    audio.save("example.mp3")
                                    #os.system("start example.mp3")
                                    try:
                                        playsound("example.mp3")
                                        os.remove("example.mp3")
                                        #os.rename('example.mp3', 'example1.mp3')
                                    except :
                                        print ('Error Opening audio file')
                                
                                


window.close()

"""


http://www.PySimpleGUI.org - Documentation
http://Cookbook.PySimpleGUI.org - Cookbook 
http://Calls.PySimpleGUI.org - detailed call reference
http://www.PySimpleGUI.com - GitHub
http://Demos.PySimpleGUI.org - Demo Programs
http://Trinket.PySimpleGUI.org - Run a bunch of demos online
http://YouTube.PySimpleGUI.org - Playlist of the current instructional videos
http://Issues.PySimpleGUI.org - File an issue, ask a question, report a bug

https://www.youtube.com/watch?v=36BdjuNcQJ4&list=PLl8dD0doyrvFfzzniWS7FXrZefWWExJ2e&index=2

"""