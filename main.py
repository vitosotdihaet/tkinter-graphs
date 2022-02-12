from ctypes import resize
import tkinter as tk
from math import *


def f(x):
    return eval(real_function.replace('x', str(x)))

def dichotomy(a, b):
    pass

def chord(a, b):
    fa = f(a)
    fb = f(b)
    ap, bp = a - 1, b + 1

    while not (ap == a and bp == b):
        fa = f(a)
        fb = f(b)

        m = (a * fb - b * fa)/(fb - fa)
        print(m)
        fm = f(m)
        if fa * fm < 0:
            ap = a
            a = m
        elif fb * fm < 0:
            bp = b
            b = m
        else: break

    print(m)
        

def resize(event):
    frame_main['width'] = event.width
    frame_main['height'] = event.height

    frame_top['width'] = event.width
    frame_top['height'] = event.height - 100
    canv['width'] = int(min(frame_top['width'], frame_top['height'])) - 4
    canv['height'] = int(min(frame_top['width'], frame_top['height'])) - 4
    
    frame_input['width'] = event.width // 2
    frame_input['height'] = 100
    
    frame_methods['width'] = event.width // 2
    frame_methods['height'] = 100
    build(event)

def build(event):
    global real_function
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
        x += round(sc/8, 6)
        try:
            y = f(x)
            dots.append((int(x * size//(sc * 200)) + size//2, int(-y * size//(sc * 200)) + size//2))
        except:
##            canv.create_line(*dots, width=3)
##            canv.create_oval(size//2 - 2, size//2 - 2,
##                             size//2 + 1, size//2 + 1,
##                             fill='red', width=0)
##            dots = []
            continue

    # print(dots)
    canv.create_line(*dots, width=3)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Non-linear functions")
    root.minsize(500, 600)
    root.resizable(width=True, height=True)

    size = 700

    frame_main = tk.Frame(root)
    frame_main.pack(fill=tk.BOTH, expand=tk.YES)

    frame_top = tk.Frame(frame_main)
    frame_top.pack(fill=tk.BOTH, expand=tk.YES)

    frame_input = tk.Frame(frame_main, width=size//2, height=100)
    frame_input.pack(fill=tk.BOTH, side=tk.LEFT)

    frame_methods = tk.Frame(frame_main, width=size//2, height=100)
    frame_methods.pack(fill=tk.BOTH, side=tk.RIGHT)

    canv = tk.Canvas(frame_top, width=size, height=size)
    canv.pack(fill=tk.BOTH, expand=tk.YES)

    canv.create_line(size//2, size, size//2, 0, width=2, arrow=tk.LAST)
    canv.create_line(0, size//2, size, size//2, width=2, arrow=tk.LAST)
    canv.create_line(0, size - 1, size, size - 1, width=3)
    for v in range(10):
        canv.create_line(size*v//10, size, size*v//10, 0, width=1)
    for h in range(10):
        canv.create_line(0, size*h//10, size, size*h//10, width=1)

    function_val = tk.StringVar()
    function_val.set('sin(sin(x))**2/x')
    function_entr = tk.Entry(frame_input, width=25, textvariable=function_val)
    function_entr.pack()

    button_build = tk.Button(frame_input, width=15, height=2, text='Build!')
    button_build.pack()
    button_build.bind("<ButtonPress-1>", build)

    button_chord = tk.Button(frame_methods, width=15, height=2, text='Chord',
                             command=lambda: chord(float(from_val.get()), float(to_val.get())))
    button_chord.pack()

    from_val = tk.StringVar()
    from_val.set('-5')
    
    from_label = tk.Label(frame_methods, width=5, text='From:')
    from_label.pack(side=tk.LEFT, anchor=tk.NE)

    from_entr = tk.Entry(frame_methods, width=5, textvariable=from_val)
    from_entr.pack(side=tk.TOP)



    to_val = tk.StringVar()
    to_val.set('5')

    to_label = tk.Label(frame_methods, width=5, text='To:')
    to_label.pack(side=tk.LEFT, anchor=tk.NE)
    
    to_entr = tk.Entry(frame_methods, width=5, textvariable=to_val)
    to_entr.pack(side=tk.TOP)

    scale = tk.Scale(frame_input,
                     from_=1, to=100, 
                     orient=tk.HORIZONTAL, 
                     length=200, command=build)
    scale.pack()

    frame_main.bind("<Configure>", resize)

    root.mainloop()
