import ttkbootstrap as tk
from ttkbootstrap.constants import *
import webbrowser

def cosmiclink(*args):
    global link_string
    global cosmic_ID
    full_link = link_string + cosmic_ID.get()
    webbrowser.open(full_link)
    return

app = tk.Window(themename='lumen')
link_string = "https://cancer.sanger.ac.uk/cosmic/mutation/overview?id="
cosmic_ID = tk.StringVar()
cosmic_ID.set("179417586")
app.geometry('400x400')
button1 = tk.Button(app, text='COSMIC Link Button', command=cosmiclink)
button1.pack(side='top')
label1 = tk.Label(app, text='COSMIC Link Label')
label1.pack(side='top')
label1.bind("<Button-1>", cosmiclink)

app.mainloop()