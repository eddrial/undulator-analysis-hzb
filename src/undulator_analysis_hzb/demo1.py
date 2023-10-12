import matplotlib.pyplot as plt
import numpy as np

def add_one(number):
    return number + 1

def simply_plot():
    a = np.arange(19)
    b = np.arange(19) * a
    
    fig, ax = plt.subplots()
    fig.set_size_inches(8,4)
    ax.plot(a,b)
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
    
    return fig