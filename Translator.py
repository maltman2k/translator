
import PySimpleGUI as sg
import win32api
import pyautogui
import pyperclip
from googletrans import Translator
from gtts import gTTS
import os
#from playsound import playsound
import pygame
import time

StatusBarInitialStr='JCI'


def StatusBar (msg):
        window['-STAT-'].update(msg)
        window.refresh()  



def PlaySound (sound):
        StatusBar("Playing Voice")
        try:
            pygame.init()
            pygame.mixer.music.load(sound)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                    event, values = window.read(timeout = 10)
                    #if event == 'Voice Play' :
                    #    pygame.mixer.music.play()

                    if event == 'Stop Voice' :
                        pygame.mixer.music.stop()
                                                
                    #if event == 'Pause Voice' :
                    #     pygame.mixer.music.pause()

                    continue
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.quit()

        except Exception as e: print(e)
        StatusBar(StatusBarInitialStr)


def ConvertTextToSpeech(TextToSpeech):
     StatusBar("Converting Text to Speech")
     audio = gTTS(text=TextToSpeech, lang="it", slow=False)       
     audio.save("example.mp3")
     StatusBar(StatusBarInitialStr)
     return("example.mp3")






oldtext=''
MouseState="none"
translator = Translator()
pygame.init()

print ("Translator started.....")

# this is the layout structure

layout = [
          [sg.Checkbox("Enable Translation",default=True, key='-S1-',pad=(5, (5, 10))),sg.Checkbox("Enable Voice", key='-S2-',pad=(5, (5, 10)))],
          #[sg.Button('Play Voice'),sg.Button('Pause Voice'), sg.Button('Stop Voice')],
          [sg.Button('Stop Voice'),sg.Button('Repeat')],
          [sg.Multiline('Multiline\n', disabled=True,size=(95,22), key='-OUT-')],
          [sg.Button('OK'), sg.Button('Exit')],
          [sg.StatusBar("JCI",size=(100,1),justification='center' ,key="-STAT-")]]

#sg.theme('DarkBlue1')
window = sg.Window('Translator', layout,keep_on_top=True,size=(700, 500))

while True:
    event, values = window.read(timeout = 100)

    if event == 'Exit' or event == sg.WIN_CLOSED:
        break
    
    if event == 'OK' :
        print ('Out of Loop')
        window['-OUT-'].update(values['-IN-'])


    if values["-S2-"] != True:
        window['Stop Voice'].update(disabled=True)
        window['Repeat'].update(disabled=True)

    else:
        window['Stop Voice'].update(disabled=False)
        window['Repeat'].update(disabled=False)



    if event == 'Repeat' :
        print ('Repeat')
        if values["-S2-"] == True:
            textToRepeat=values['-OUT-']
            StrAudioFileName=ConvertTextToSpeech(textToRepeat)
            PlaySound(StrAudioFileName)
       
            

  
        

    # -------------Check if translation Enabled
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

                            # Check if Voice is enabled
                            if values["-S2-"] == True:
                                
                                if len(translation.text) > 0:
                                    StrAudioFileName=ConvertTextToSpeech(translation.text)
                                    PlaySound(StrAudioFileName)
                                    


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