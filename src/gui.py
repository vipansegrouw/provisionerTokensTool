import tkinter as tk
from tkinter import ttk

import pyperclip

from items import _get_best_item_per_vendor, _get_items_within_price_threshold


def create_output(entry, window, items):
    threshold = int(entry.get()) * 100
    items = _get_best_item_per_vendor(items)
    items = _get_items_within_price_threshold(threshold, items)
    for widget in window.winfo_children():
        widget.destroy()

    create_second_window(items, window)
    window.update()


def create_and_display_purchase_list(master, items_list):
    for idx, item in enumerate(items_list):
        create_line(master, item, idx)
    tk.Button(master=master, text="QUIT", command=master.quit).grid(column=2, row=len(items_list) + 1)


def copy_to_clipboard(text, button_label):
    pyperclip.copy(text)
    button_label.set("Copied!")


def price_formatter(text):
    text = str(text)
    text = text[::-1]
    string = "c"
    for idx, character in enumerate(text):
        if idx == 2:
            string += "s"
        if idx == 4:
            string += "g"
        string += character
    return string[::-1]


def create_line(master, item, idx):
    txt_item = item['name']
    txt_price = price_formatter(item['price'])
    button_label = tk.StringVar()
    tk.Label(master=master, text=f"{txt_item}", justify=tk.LEFT).grid(column=1, row=idx + 1)
    tk.Button(master=master, textvariable=button_label, command=lambda: copy_to_clipboard(txt_item, button_label)).grid(
        column=2, row=idx + 1)
    tk.Label(master=master, text=f"{txt_price}", justify=tk.RIGHT).grid(column=3, row=idx + 1)
    button_label.set("Copy")


def create_second_window(items, window):
    mainframe = ttk.Frame(master=window, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky="N, W, E, S")
    create_and_display_purchase_list(mainframe, items)
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)


def user_entry_window(items):
    win_user_entry = create_first_window(items)
    win_user_entry.mainloop()


def create_first_window(items):
    win_user_entry = tk.Tk()
    win_user_entry.title("Provisioner Token Helper")
    frm_coins = tk.Frame(master=win_user_entry, padx="24", pady="24")
    frm_coins.pack()
    lbl_coins = tk.Label(master=frm_coins, text="Max Cost (Silver)")
    ent_coins = tk.Entry(master=frm_coins, width=40)
    btn_coins = tk.Button(master=frm_coins, text="OK", command=lambda: create_output(ent_coins, win_user_entry, items))
    lbl_coins.pack()
    ent_coins.pack(side=tk.LEFT)
    btn_coins.pack(side=tk.LEFT)
    return win_user_entry
