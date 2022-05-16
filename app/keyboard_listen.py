from pynput import keyboard

def on_press(key):
    global adaptiveThreshWinSizeMin
    global adaptiveThreshWinSizeMax
    global adaptiveThreshWinSizeStep
    global adaptiveThreshConstant
    global captureBits
    global bin_threshold
    global margin
    if key == keyboard.Key.space:
        print("SPACE")
        captureBits=True
    if hasattr(key, 'char'):
        # -----------------------
        # adaptiveThreshWinSizeMin
        # -----------------------
        if key.char == 'a':
            adaptiveThreshWinSizeMin = adaptiveThreshWinSizeMin+1
            print("adaptiveThreshWinSizeMin", adaptiveThreshWinSizeMin)
        if key.char == 'A':
            if adaptiveThreshWinSizeMin > 3:
                adaptiveThreshWinSizeMin = adaptiveThreshWinSizeMin-1
                print("adaptiveThreshWinSizeMin", adaptiveThreshWinSizeMin)
        # -----------------------
        # adaptiveThreshWinSizeMin
        # -----------------------
        if key.char == 's':
            adaptiveThreshWinSizeStep = adaptiveThreshWinSizeStep+1
            print("adaptiveThreshWinSizeStep", adaptiveThreshWinSizeStep)
        if key.char == 'S':
            adaptiveThreshWinSizeStep = adaptiveThreshWinSizeStep-1
            print("adaptiveThreshWinSizeStep", adaptiveThreshWinSizeStep)
        # -----------------------
        # adaptiveThreshWinSizeStep
        # -----------------------
        if key.char == 'd':
            adaptiveThreshWinSizeMax = adaptiveThreshWinSizeMax+1
            print("adaptiveThreshWinSizeMax", adaptiveThreshWinSizeMax)
        if key.char == 'D':
            adaptiveThreshWinSizeMax = adaptiveThreshWinSizeMax-1
            print("adaptiveThreshWinSizeMax", adaptiveThreshWinSizeMax)
        # -----------------------
        # adaptiveThreshWinSizeStep
        # -----------------------
        if key.char == 'c':
            adaptiveThreshConstant = adaptiveThreshConstant+1
            print("adaptiveThreshConstant", adaptiveThreshConstant)
        if key.char == 'C':
            adaptiveThreshConstant = adaptiveThreshConstant-1
            print("adaptiveThreshConstant", adaptiveThreshConstant)
        # -----------------------
        # Margin
        # -----------------------
        if key.char == 'm':
            margin = margin+1
            print("margin", margin)
        if key.char == 'M':
            margin = margin-1
            print("margin", margin)
        # -----------------------
        # THRESHOLD
        # -----------------------
        if key.char == 't':
            bin_threshold = bin_threshold+1
            print("bin_threshold", bin_threshold)
        if key.char == 'T':
            margin = margin-1
            bin_threshold = bin_threshold-1
            print("bin_threshold", bin_threshold)

def on_release(key):
    global captureBits
    if key == keyboard.Key.space:
        captureBits=False
    return
    #print('{0} released'.format(key))
 

def keyboard_listen():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
