import eel


if __name__ == '__main__':
    eel.init('front')
    
    from pages import *
    from ui_callbacks import *
    
    eel.start('login.html', size=(1270, 980))