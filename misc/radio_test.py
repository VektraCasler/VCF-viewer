import ttkbootstrap as tk
from ttkbootstrap.constants import *
import webbrowser


class testapp(tk.Window):

    def __init__(self):
        super().__init__(self)

        self.geometry('400x400')

        # self.configure(themename='lumen')
        self.frame = tk.Frame(self)
        self.frame.pack(side='top', expand=True, fill='both')

        self.radio_select = tk.StringVar()
        self.radio_select = '1'

        self.bind('<Right>', lambda event: self.goto_next_radio())
        self.bind('<Left>', lambda event: self.goto_prev_radio())

        self.radio1 = tk.Radiobutton(self.frame,variable=self.radio_select, value='1', text='Value 1')
        self.radio1.pack(side='top')
        self.radio2 = tk.Radiobutton(self.frame,variable=self.radio_select, value='2', text='Value 2')
        self.radio2.pack(side='top')
        self.radio3 = tk.Radiobutton(self.frame,variable=self.radio_select, value='3', text='Value 3')
        self.radio3.pack(side='top')
        self.radio4 = tk.Radiobutton(self.frame,variable=self.radio_select, value='4', text='Value 4')
        self.radio4.pack(side='top')
        self.radio5 = tk.Radiobutton(self.frame,variable=self.radio_select, value='5', text='Value 5')
        self.radio5.pack(side='top')

        return


    def goto_next_radio(self):
        print("RIGHT",self.radio_select)
        if not self.radio_select:
            pass
        elif self.radio_select == '1':
            self.radio2.invoke()
        elif self.radio_select == '2':
            self.radio3.invoke()
        elif self.radio_select == '3':
            self.radio4.invoke()
        elif self.radio_select == '4':
            self.radio5.invoke()
        elif self.radio_select == '5':
            self.radio1.invoke()
        return

    def goto_prev_radio(self):
        print("LEFT",self.radio_select)
        if not self.radio_select:
            pass
        elif self.radio_select == '1':
            self.radio5.invoke()
        elif self.radio_select == '2':
            self.radio1.invoke()
        elif self.radio_select == '3':
            self.radio2.invoke()
        elif self.radio_select == '4':
            self.radio3.invoke()
        elif self.radio_select == '5':
            self.radio4.invoke()
        return

my_app = testapp()

my_app.mainloop()