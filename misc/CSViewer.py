# CSViewer.py
''' An application to view a csv file. '''

# IMPORTS ------------------------------------------------

import tkinter as tk 
import tkinter.ttk as ttk 
import os 
import json
from tkinter.messagebox import showinfo

# VARIABLES ----------------------------------------------

settings_filename = 'settings.json'
if os.path.exists(settings_filename):
    SETTINGS = json.load(settings_filename)
else:
    SETTINGS = {
        'window_height':400,
        'window_width':600,
        'app_title':"CSViewer",
    }

# MAIN LOOP ----------------------------------------------

def main():

    root = tk.Tk()
    root.title(SETTINGS['app_title'])
    root.resizable(width=True, height=True)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    window_geometry = f"{SETTINGS['window_width']}x{SETTINGS['window_height']}"
    root.geometry(window_geometry)
    
    frame1 = tk.Frame(root, bg='black')
    frame1.columnconfigure(0, weight=1)
    frame1.rowconfigure(0, weight=1)
    frame1.grid(column=0,row=0, sticky='nsew')
    
    # define columns
    columns = (
        'first_name', 
        'last_name', 
        'age',
        'month',
        'day',
        'sign',
        'card',
        'color',
        'preposition',
        'body_part'
    )

    tree = ttk.Treeview(frame1, columns=columns, show='headings')

    # define headings
    tree.heading('first_name', text='First Name', anchor='center')
    tree.heading('last_name', text='Last Name', anchor='center')
    tree.heading('age', text='Age', anchor='center')
    tree.heading('month', text='Month', anchor='center')
    tree.heading('day', text='Day', anchor='center')
    tree.heading('sign', text='Sign', anchor='center')
    tree.heading('card', text='Card', anchor='center')
    tree.heading('color', text='Color', anchor='center')
    tree.heading('preposition', text='Preposition', anchor='center')
    tree.heading('body_part', text='Body Part', anchor='center')
    for x in range(10):
        tree.column(x, anchor='center', width=100)
    
    # generate sample data
    contacts = []
    for n in range(1, 100):
        contacts.append((
            f'first {n}', 
            f'last {n}', 
            f'age {n}', 
            f'month {n}', 
            f'day {n}', 
            f'sign {n}', 
            f'card {n}', 
            f'color {n}', 
            f'preposition {n}',
            f'body part{n}'
        ))

    # add data to the treeview
    for contact in contacts:
        tree.insert('', tk.END, values=contact)


    def item_selected(event):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
            # show a message
            showinfo(title='Information', message=','.join(record))


    tree.bind('<<TreeviewSelect>>', item_selected)

    tree.grid(row=0, column=0, sticky='nsew')

    # add a scrollbar
    scrollbar = ttk.Scrollbar(frame1, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')
    
    root.mainloop()    

    return

if __name__ == '__main__':
    main()
