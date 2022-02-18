import tkinter as tk
from math import *


def f(x):
    try:
        return eval(real_function.replace('x', str(x)))
    except: return None

def find_all_xs(a, b, iters):
    t = iters

    s = [a, (a + b)/2]
    e = [b, (a + b)/2]

    for _ in range(1, t):
        ls = len(s)
        le = len(e)
        for i in range(1, ls + 1, 2):
            s = s[:i] + [(s[i - 1] + s[i])/2] + s[i:]

        for i in range(1, le + 1, 2):
            e = e[:i] + [(e[i - 1] + e[i])/2] + e[i:]

    s.extend(e[::-1])
    ab = s
    lab = len(ab)
    ab.pop(lab//2)
    # print(ab)

    answ = []

    for i in range(lab - 2):
        current = dichotomy(ab[i], ab[i + 1])
        if current[0] == True:
            answ.append(current[1])
    
    print('Roots in this area:', *answ)

def dichotomy(a, b):
    print('Dichotomy method on', a, 'to', b, '-', end=' ')

    fa = f(a)
    fb = f(b)
    if fa == 0: return True, a
    elif fb == 0: return True, b

    m = (a + b)/2
    while True:
        fa = f(a)
        fb = f(b)

        if fa == None or fb == None:
            fa = f(a + epsilon)
            fb = f(b + epsilon)

        canv.create_line(int(a * size//(sc * 200)) + size//2,
                         int(canv['height'])/2 - 50,
                         int(a * size//(sc * 200)) + size//2,
                         int(canv['width'])/2 + 50,
                         fill='blue')

        canv.create_line(int(b * size//(sc * 200)) + size//2,
                         int(canv['height'])/2 - 50,
                         int(b * size//(sc * 200)) + size//2,
                         int(canv['width'])/2 + 50,
                         fill='blue')

        m = (a + b)/2

        fm = f(m)
        if fm == None:
            m += epsilon
            fm = f(m)

        # print(m, '-', fm)
        if abs(fm) <= epsilon or b == m or a == m:
            break
        else:
            if fm * fa > 0:
                a = m
            else:
                b = m

    if abs(fm) <= epsilon:
        print(m)
        return True, m
    else:
        print('no roots!')
        return False, 0

def chord(a, b):
    print('Chord method on', a, 'to', b, '-', end=' ')

    fa = f(a)
    fb = f(b)

    if fa == 0: return True, a
    elif fb == 0: return True, b

    ap, bp = a - 1, b + 1

    m = (a + b)/2
    while True:
        fa = f(a)
        fb = f(b)

        if fa == None or fb == None:
            fa = f(a + epsilon)
            fb = f(b + epsilon)

        canv.create_line(int(a * size//(sc * 200)) + size//2,
                            int(fa * size//(sc * 200)) + size//2,
                            int(b * size//(sc * 200)) + size//2,
                            int(fb * size//(sc * 200)) + size//2,
                            fill='orange')

        m = (a * fb - b * fa)/(fb - fa)

        fm = f(m)
        if fm == None:
            m += epsilon
            fm = f(m)

        # print(m, '-', fm)
        if (abs(fm) <= epsilon or b == m or a == m or
            abs(a - ap) < epsilon or abs(b - bp) < epsilon):
            break
        else:
            if fm * fa > 0:
                ap = a
                a = m
            else:
                bp = b
                b = m

    if abs(fm) <= epsilon:
        print(m)
        return True, m
    else:
        print('no roots!') 
        return False, 0

def resize(event):
    frame_main['width'] = event.width
    frame_main['height'] = event.height

    frame_top['width'] = event.width
    frame_top['height'] = event.height - 100
    canv['width'] = int(min(frame_top['width'], frame_top['height'])) - 4
    canv['height'] = int(min(frame_top['width'], frame_top['height'])) - 4

    frame_input['height'] = 100
    frame_methods['height'] = 100

    build(event)

def build(event):
    global real_function, sc, size, precision
    dots = []
    sc = scale.get() * 0.01

    real_function = function_val.get().replace('x', '(x)').replace('e', '2.7182818284')

    canv.delete('all')
    size = int(min(frame_top['width'], frame_top['height']))

    canv.create_line(size//2, size, size//2, 0, width=2, arrow=tk.LAST)
    canv.create_line(0, size//2, size, size//2, width=2, arrow=tk.LAST)

    for v in range(10):
        canv.create_line(size*v//10, size, size*v//10, 0, width=1)
    for h in range(10):
        canv.create_line(0, size*h//10, size, size*h//10, width=1)

    precision = int(min(frame_main['width'], frame_main['height']))/1600
    step = round(sc/(8 * precision), 4)

    # x and y are real graph numbers
    x = -sc * 100 - step

    canv.create_text(size//2 + 30, 20, text=str(abs(int(x))), font=('Purisa', 16))
    canv.create_text(size - 20, size//2 + 30, text=str(abs(int(x))), font=('Purisa', 16))

    # print(step, '<- step')
    for _ in range(int(800 * precision + precision*25)):
        x = round(x + step, 4)
        # print(x, end=' ')
        try:
            y = f(x)
            # print(y)
            xcord = int(x * size//(sc * 200)) + size//2
            ycord = int(-y * size//(sc * 200)) + size//2
            if -precision * 100000 < ycord < precision * 100000:
                dots.append((xcord, ycord))
        except:
            # print('error at', x)
            if dots != []:
                canv.create_line(*dots, width=3)

            canv.create_oval(int(x * size//(sc * 200)) - 2 + size//2, size//2 - 2,
                             int(x * size//(sc * 200)) + 2 + size//2, size//2 + 1,
                             fill='red', width=0)
            dots = []
            continue

    x = -step
    for _ in range(int(800 * precision) + 1):
        x = round(x + step, 4)
        # print(x, end=' ')
        try:
            y = f(x)
            # print(y)
            xcord = int(x * size//(sc * 200)) + size//2
            ycord = int(-y * size//(sc * 200)) + size//2
            if -precision * 10000 < ycord < precision * 10000:
                dots.append((xcord, ycord))
        except:
            # print('error at', x)
            if dots != []:
                canv.create_line(*dots, width=3)

            canv.create_oval(int(x * size//(sc * 200)) - 2 + size//2, size//2 - 2,
                             int(x * size//(sc * 200)) + 2 + size//2, size//2 + 1,
                             fill='red', width=0)
            dots = []
            continue

    canv.create_line(*dots, width=3)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Graphs")
    root.minsize(500, 600)
    root.resizable(width=True, height=True)

    size = 700

    frame_main = tk.Frame(root)
    frame_main.pack(fill=tk.BOTH, expand=tk.YES)

    frame_top = tk.Frame(frame_main)
    frame_top.pack(fill=tk.BOTH, expand=tk.YES, side=tk.TOP)

    frame_input = tk.Frame(frame_main, width=size//2, height=100,)
    frame_input.pack(fill=tk.Y, expand=tk.YES, side=tk.LEFT)

    frame_methods = tk.Frame(frame_main, width=size//2, height=100)
    frame_methods.pack(fill=tk.Y, expand=tk.YES, side=tk.RIGHT)


    canv = tk.Canvas(frame_top, width=size, height=size)
    canv.pack(fill=tk.Y, expand=tk.YES)

    function_val = tk.StringVar()
    function_val.set('sin(sin(x))**2/x')
    function_entr = tk.Entry(frame_input, width=25, textvariable=function_val)
    function_entr.grid(row=0, column=0)

    scale = tk.Scale(frame_input,
                    from_=1, to=200, 
                    orient=tk.HORIZONTAL, 
                    length=200, command=build)
    scale.grid(row=2, column=0)

    button_build = tk.Button(frame_input, width=20, height=2, text='Build!')
    button_build.grid(row=1, column=0)
    button_build.bind("<ButtonPress-1>", build)

    button_chord = tk.Button(frame_methods, width=10, height=2, text='Chord',
                             command=lambda: chord(float(from_val.get()), float(to_val.get())))
    button_chord.grid(row=0, column=0)

    button_dich = tk.Button(frame_methods, width=10, height=2, text='Dichotomy',
                             command=lambda: dichotomy(float(from_val.get()), float(to_val.get())))
    button_dich.grid(row=0, column=1)

    button_findxs = tk.Button(frame_methods, width=10, height=2, text='Find all xs',
                             command=lambda: find_all_xs(float(from_val.get()), float(to_val.get()), int(iters.get())))
    button_findxs.grid(row=0, column=2)

    iters = tk.Scale(frame_methods,
                     from_=2, to=10, 
                     orient=tk.HORIZONTAL, 
                     length=60, command=build)
    iters.grid(row=1, column=2)

    from_val = tk.StringVar()
    from_val.set('-2')

    from_label = tk.Label(frame_methods, width=5, text='From:')
    from_label.grid(row=1, column=0, sticky=tk.W)

    from_entr = tk.Entry(frame_methods, width=5, textvariable=from_val)
    from_entr.grid(row=1, column=1)


    to_val = tk.StringVar()
    to_val.set('2')

    to_label = tk.Label(frame_methods, width=5, text='To:')
    to_label.grid(row=2, column=0, sticky=tk.W)

    to_entr = tk.Entry(frame_methods, width=5, textvariable=to_val)
    to_entr.grid(row=2, column=1)

    frame_main.bind("<Configure>", resize)

    epsilon = 1.19209e-07

    root.mainloop()
