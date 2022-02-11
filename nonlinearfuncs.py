from ctypes import resize
import tkinter as tk
from math import *

def resize(event):
    frame_main['width'] = event.width
    frame_main['height'] = event.height

    frame_top['width'] = event.width
    frame_top['height'] = event.height - 100
    canv['width'] = int(min(frame_top['width'], frame_top['height'])) - 4
    canv['height'] = int(min(frame_top['width'], frame_top['height'])) - 4

    frame_bottom['width'] = event.width
    frame_bottom['height'] = 100
    build(event)

def build(event):
    dots = []
    sc = scale.get() * 0.01

    real_function = function_val.get().replace('x', '(x)')

    canv.delete('all')
    size = int(min(frame_top['width'], frame_top['height']))

    canv.create_line(size//2, size, size//2, 0, width=2, arrow=tk.LAST)
    canv.create_line(0, size//2, size, size//2, width=2, arrow=tk.LAST)
    canv.create_line(0, size, size, size, width=3)
    for v in range(10):
        canv.create_line(size*v//10, size, size*v//10, 0, width=1)
    for h in range(10):
        canv.create_line(0, size*h//10, size, size*h//10, width=1)

    x = sc * (-100 - 1/8)
    canv.create_text(size//2 + 30, 20, text=str(abs(int(x))), font=('Purisa', 16))
    canv.create_text(size - 20, size//2 + 30, text=str(abs(int(x))), font=('Purisa', 16))
    for _ in range(1600 + 2):
        x += sc/8
        try:
            y = eval(real_function.replace('x', str(x)))
            dots.append((int(x * size//(sc * 200)) + size//2, int(-y * size//(sc * 200)) + size//2))
        except: continue

    # print(dots)
    canv.create_line(*dots, width=3)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Non-linear functions")
    root.minsize(500, 600)
    root.resizable(width=True, height=True)

    frame_main = tk.Frame(root)
    frame_main.pack(fill=tk.BOTH, expand=tk.YES)

    frame_top = tk.Frame(frame_main)
    frame_top.pack(fill=tk.BOTH, expand=tk.YES)

    frame_bottom = tk.Frame(frame_main, height=100)
    frame_bottom.pack(fill=tk.BOTH, side=tk.BOTTOM)

    canv = tk.Canvas(frame_top, width=1000, height=1000)
    canv.pack(fill=tk.BOTH, expand=tk.YES)

    canv.create_line(500, 1000, 500, 0, width=2, arrow=tk.LAST)
    canv.create_line(0, 500, 1000, 500, width=2, arrow=tk.LAST)
    canv.create_line(0, 1000, 1000, 1000, width=3)
    for v in range(10): # horizontal lines
        canv.create_line(100*v, 1000, 100*v, 0, width=1)
    for h in range(10): # vertical lines
        canv.create_line(0, 100*h, 1000, 100*h, width=1)

    function_val = tk.StringVar()
    function_val.set('sin(sin(x))')
    function_entr = tk.Entry(frame_bottom, width=15, textvariable=function_val)
    function_entr.pack()

    button_build = tk.Button(frame_bottom, width=12, height=2, text='Build!')
    button_build.pack()
    button_build.bind("<ButtonPress-1>", build)

    scale = tk.Scale(frame_bottom,
                     from_=1, to=100, 
                     orient=tk.HORIZONTAL, 
                     length=200, command=build)
    scale.pack()

    frame_main.bind("<Configure>", resize)

    root.mainloop()