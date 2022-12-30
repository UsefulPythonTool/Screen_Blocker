from pynput import keyboard
from pynput import mouse

from tkinter import *
from concurrent import futures

class Blocker:
    def __init__(self):
        self.pool = futures.ThreadPoolExecutor(max_workers=1)
        self.container = []
        self.create = {"alt_l"}
        self.delete = {"alt_l","backspace"}
        self.keypressed = set()
        self.coordinate = [0,0,0,0]
        self.pool.submit(self.start)
        self.root = Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-alpha',0)
        self.root.mainloop()
        
    def addBlock(self, geometry):
        self.container.append(Toplevel())
        self.container[-1].geometry(geometry)
        self.container[-1].overrideredirect(True)
        self.container[-1].attributes('-topmost', True)
        self.container[-1].configure(background = "white")

    def start(self):
        def on_press(key):
            k = str(key).replace("Key.","").replace("'",'')
            self.keypressed.add(k)
            if(self.keypressed==self.delete and self.container):
                self.container[-1].destroy()
                self.container.pop()
 
        def on_release(key):
            k = str(key).replace("Key.","").replace("'",'')
            if all(self.coordinate):
                x1,y1,x2,y2 = self.coordinate
                geometry = f"{abs(x2-x1)}x{abs(y2-y1)}+{min(x1,x2)}+{min(y1,y2)}"
                self.addBlock(geometry)
            self.coordinate = [0,0,0,0]
            self.keypressed.discard(k)

        def on_click(x,y,button,pressed):
            if pressed:
                if self.keypressed == self.create:
                    self.coordinate[0] = x
                    self.coordinate[1] = y
            else:
                if self.keypressed == self.create:
                    self.coordinate[2] = x
                    self.coordinate[3] = y

        self.kl = keyboard.Listener(on_press=on_press,on_release=on_release)
        self.ml = mouse.Listener(on_click=on_click)
        self.kl.start()
        self.ml.start()
        self.kl.join()
        self.ml.join()

if __name__ == "__main__":
    Blocker()