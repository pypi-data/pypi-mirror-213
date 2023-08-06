from importlib.resources import contents, path
from pm20_3 import q
from PIL import ImageGrab
from IPython.display import display, Image
import os


def theory(qn=0):
    if not qn:
        with path(
                q,
                'task_1.png'
        ) as pt:
            img = Image(filename=pt)
            display(img)

        with path(
                q,
                'task_2.png'
        ) as pt:
            img = Image(filename=pt)
            display(img)

        with path(
                q,
                'task_3.png'
        ) as pt:
            img = Image(filename=pt)
            display(img)

        with path(
                q,
                'task_4.png'
        ) as pt:
            img = Image(filename=pt)
            display(img)

        with path(
                q,
                'task_5.png'
        ) as pt:
            img = Image(filename=pt)
            display(img)

        with path(
                q,
                'task_6.png'
        ) as pt:
            img = Image(filename=pt)
            display(img)

    else:
        qn = str(qn)
        files = sorted(contents(q))
        to_disp = []
        for elem in files:
            if qn + '_' in elem:
                to_disp.append(elem)
        if not to_disp:
            to_disp.append(qn + '.png')
        to_disp.sort()
        for elem in to_disp:
            with path(
                    q,
                    elem
            ) as pt:
                img = Image(filename=pt)
                display(img)


def checker(pt):
    print(os.listdir(pt))
