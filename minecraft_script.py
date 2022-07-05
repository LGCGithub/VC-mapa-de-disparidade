import cv2
import random
import string
from pynput import keyboard
from Window import FindWindows, Window

#FindWindows()

window = Window('Minecraft 1.19 - Singleplayer', 1600, 900)
turn = "left"
name = ""

def save_img():
    global window, turn, name

    if turn == "left": # Se for a primeira imagem, cria um nome aleatorio para ela
        name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))

    img = window.screenshot()
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) # remove alpha
    
    filename = turn + "\\" + name + ".png"
    print(filename)

    cv2.imwrite(filename, img) # Salva a imagem na pasta apropriada

    if turn == "left":
        turn = "right"
    else:
        turn = "left"
        name = ""

def on_press(key):
    try:
        if key.char == "c":
            save_img()

    except AttributeError:
        pass
        #print('special key pressed: {0}'.format(
        #    key))

with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()


