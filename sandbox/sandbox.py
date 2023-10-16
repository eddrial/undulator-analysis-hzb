'''
Created on Oct 5, 2023

@author: oqb
'''

import undulator_analysis_hzb.demo1 as demo1
from tkinter import *
import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
from bokeh.models import canvas

def Tkplay():
    root = Tk()
    
    #window title
    root.title('Ed\'s Window')
    
    #window size
    root.geometry('628x314')
    
    #label for root window
    lbl = Label(root, text = 'The Window Label')
    lbl.grid()
    
    #add entry field
    num = Entry(root, width = 10)
    num.grid(column = 1, row = 0)
    
    #create a function
    def clicked():
        thenum = int(num.get())
        res = '{} + 1 = {}'.format(thenum, demo1.add_one(thenum))
        lbl.configure(text = res)
    
    #button widget with red text
    btn = Button(root, text = 'Cl*ck!', fg = 'red', command = clicked)
    
    #set button grid
    btn.grid(column = 2, row = 0)

    
    
    
    #execute mainloop / window has to be built before this
    root.mainloop()

def Ctkplay():
    ctk.set_appearance_mode("system")
    

    "Here all other widgetts will be added"
    def random_number():
        print(np.random.randint(0,100))

    
    root = ctk.CTk()
    root.geometry("628x314")
    root.update()
    myplot = demo1.simply_plot()
    canvas = FigureCanvasTkAgg(myplot,master=root)
    canvas.draw()
    canvas.get_tk_widget().place(relx=0.15, rely=0.15)
    
    root.mainloop()


class ctkApp:
        
    def __init__(self):
        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.geometry("1200x400+200x200")
        self.root.title("Dynamic Scatterplot")
        self.root.update()
        self.frame = ctk.CTkFrame(master=self.root,
                                  height= self.root.winfo_height()*0.95,
                                  width = self.root.winfo_width()*0.66,
                                  fg_color="darkblue")
        self.frame.place(relx=0.33, rely=0.025)
        self.input =  ctk.CTkEntry(master=self.root,
                                   placeholder_text=100,
                                   justify='center',
                                   width=300,
                                   height=50,
                                   fg_color="darkblue")
        self.input.insert(0,100)
        self.input.place(relx=0.025,rely=0.5)
        self.slider = ctk.CTkSlider(master=self.root,
                                    width=300,
                                    height=20,
                                    from_=1,
                                    to=1000,
                                    number_of_steps=999,
                                    command=self.update_surface)
        self.slider.place(relx= 0.025,rely=0.75) 
        self.button = ctk.CTkButton(master = self.root,
                               text="Update Graph",
                               width=300,
                               height=50,
                               command=self.update_window)
        self.button.place(relx=0.025,rely=0.25)
        self.root.mainloop()
    
    def update_window(self):
        if hasattr(self, 'fig'):
            plt.close(self.fig)
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(11,5.3)
        global x,y,s,c
        x,y,s,c = np.random.rand(4,int(self.input.get()))
        self.ax.scatter(x,y,s*self.slider.get(),c)
        self.ax.axis("off")
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
        canvas = FigureCanvasTkAgg(self.fig,master=self.root)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.33, rely=0.025)
        
#        toolbar = NavigationToolbar2TkAgg(canvas, self)
#        toolbar.update()
#        canvas._tkcanvas.place(relx = 0, rely = 0)
        
        self.root.update()
        
    def update_surface(self,other):
        if hasattr(self, 'fig'):
            plt.close(self.fig)
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(11,5.3)
        self.ax.scatter(x,y,s*self.slider.get(),c)
        self.ax.axis("off")
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
        canvas = FigureCanvasTkAgg(self.fig,master=self.root)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.33, rely=0.025)
        self.root.update()


if __name__ == '__main__':
    demo1.add_one(3)
    
    print('does the add one function work? 4 add 1 = : {}'.format(demo1.add_one(4)))
    
    #test_demo1.simply_plot()
    #Testing Tk
#    Tkplay()

    #Testing CTk
    #Ctkplay()
    #Demo site class/function
    CTK_Window = ctkApp()
    
    print('I am done')
    
    