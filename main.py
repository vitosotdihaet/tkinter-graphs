import tkinter as tk
from math import sin
from functools import cache


@cache
def x(t, iter) -> float:
    if iter == 0:
        return t

    if 0 <= t <= 1/3:
        return x(3 * t, iter - 1) + sin(9 * 3.1415 * t)
    elif 1/3 < t < 2/3:
        return x(2 - 3 * t, iter - 1)
    elif 2/3 <= t <= 1:
        return x(3 * t - 2, iter - 1) + sin(9 * 3.1415 * t)

    return 0


def resize(event):
    frame_main['width'] = event.width
    frame_main['height'] = event.height

    frame_top['width'] = event.width
    frame_top['height'] = event.height - 100
    canv['width'] = int(min(frame_top['width'], frame_top['height'])) + 13
    canv['height'] = int(min(frame_top['width'], frame_top['height'])) + 13

    build(event)


def build(_event):
    global size, precision
    dots = []

    it = iters.get()
    sc = scale.get() / 10

    canv.delete('all')
    size = min(frame_top['width'], frame_top['height'])

    c = (200, 200)

    canv.create_line(size//2 - c[0], size, size//2 -
                     c[0], 0, width=2, arrow=tk.LAST)
    canv.create_line(0, size//2 + c[1], size, size //
                     2 + c[1], width=2, arrow=tk.LAST)

    line_factor = 20
    for v in range(int(line_factor*sc)):
        canv.create_line(size*(v + line_factor * sc / 2)//(line_factor * sc) - c[0], size,
                         size*(v + line_factor * sc / 2)//(line_factor * sc) - c[0], 0, width=1)
    for h in range(int(line_factor*sc)):
        canv.create_line(0, size*(h - line_factor * sc / 2)//(line_factor * sc) + c[1], size,
                         size*(h - line_factor * sc / 2)//(line_factor * sc) + c[1], width=1)

    step = 1e-4

    # t and y are real graph numbers
    t = 0

    for _ in range(int(1e4)):
        t = t + step

        y = x(t, it)
        if y == None:
            continue

        xcord = int(t * size//(sc * 2)) + size//2 - c[0]
        ycord = int(-y * size//(sc * 2)) + size//2 + c[1]
        dots.append((xcord, ycord))

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

    frame_input = tk.Frame(frame_main, width=size//2, height=100)
    frame_input.pack(fill=tk.Y, expand=tk.YES, side=tk.LEFT)

    frame_methods = tk.Frame(frame_main, width=size//2, height=100)
    frame_methods.pack(fill=tk.Y, expand=tk.YES, side=tk.RIGHT)

    canv = tk.Canvas(frame_top, width=size, height=size)
    canv.pack(fill=tk.Y, expand=tk.YES)

    iters_label = tk.Label(frame_methods, width=10, text='Iterattions:')
    iters_label.grid(row=1, column=2)

    iters = tk.Scale(frame_methods,
                     from_=1, to=8,
                     orient=tk.HORIZONTAL,
                     length=200, command=build)
    iters.grid(row=2, column=2)

    scale = tk.Scale(frame_input,
                     from_=1, to=50,
                     orient=tk.HORIZONTAL,
                     length=200, command=build)
    scale.grid(row=2, column=0)

    button_build = tk.Button(frame_input, width=20, height=2, text='Build!')
    button_build.grid(row=1, column=0)
    button_build.bind("<ButtonPress-1>", build)

    frame_main.bind("<Configure>", resize)

    root.mainloop()
