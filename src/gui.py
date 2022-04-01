import tkinter as tk
from tkinter import ttk
from typing import List, Dict

import pyperclip

from items import get_best_item_per_vendor, get_items_within_price_threshold


def _create_and_display_items_buttons_prices(entry: tk.Entry, window: tk.Tk, items_with_prices: List[Dict[str, str]]) -> None:
    """
    Creates and displays a window to the user containing item names and prices, along with a "copy to clipboard" button
    to facilitate ease of trading post usage.
    :param entry: user entry from initial window
    :param window: main tk window
    :param items_with_prices: list of dicts of item name, id and price triplets
    :return: None
    """
    threshold = int(entry.get()) * 100
    items_with_prices = get_best_item_per_vendor(items_with_prices)
    items_with_prices = get_items_within_price_threshold(threshold, items_with_prices)
    _destroy_widgets_in_window(window)

    _create_second_page(items_with_prices, window)
    window.update()


def _destroy_widgets_in_window(window: tk.Tk) -> None:
    """
    destroys all widgets in a window, to clean it up before displaying next page.
    :param window: tk.Tk window to cleanup
    :return: None
    """
    for widget in window.winfo_children():
        widget.destroy()


def _create_second_page(items, window):
    mainframe = ttk.Frame(master=window, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky="N, W, E, S")
    _create_purchase_list(mainframe, items)
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)


def _create_purchase_list(mainframe: ttk.Frame, items_list: List[Dict[str, str]]) -> None:
    """
    populates the page with each instance of item name, copy to clipboard button, and price
    :param mainframe: ttk.Frame for the second page
    :param items_list: List[Dict[str, str]] of item id, name and price triplets
    :return: None
    """
    for idx, item in enumerate(items_list):
        _create_purchase_line(mainframe, item, idx)
    tk.Button(master=mainframe, text="QUIT", command=mainframe.quit).grid(column=2, row=len(items_list) + 1)


def copy_to_clipboard(text: str, button_label: tk.StringVar) -> None:
    """
    copies a string to the clipboard, and updates button text to reflect it has been copied
    :param text: str to send to the clipboard
    :param button_label: the label for the button, to change once the text has been copied
    :return: None
    """
    pyperclip.copy(text)
    button_label.set("Copied!")


def _format_price_as_currency(text: str) -> str:
    """
    Formats a price as in game with gold, silver, and copper delimiters
    :param text: str of the price of an item
    :return: str formatted with gold, silver and copper delimiters
    """
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


def _create_purchase_line(mainframe: ttk.Frame, item: Dict[str, str], idx: int) -> None:
    """
    creates a line object consisting of a label of the item's name, a button to copy the name to clipboard, and the item's price
    :param mainframe: ttk.Frame for the second page
    :param item: Dict[str, str] of item name, id and price triplet
    :param idx: int of the line's index down the page
    :return: None
    """
    txt_item = item['name']
    txt_price = _format_price_as_currency(item['price'])
    button_label = tk.StringVar()
    tk.Label(master=mainframe, text=f"{txt_item}", justify=tk.LEFT).grid(column=1, row=idx + 1)
    tk.Button(master=mainframe, textvariable=button_label, command=lambda: copy_to_clipboard(txt_item, button_label)).grid(
        column=2, row=idx + 1)
    tk.Label(master=mainframe, text=f"{txt_price}", justify=tk.RIGHT).grid(column=3, row=idx + 1)
    button_label.set("Copy")


def user_entry_window(items_with_prices: List[Dict[str, str]]) -> None:
    """

    :param items_with_prices:
    :return:
    """
    win_user_entry = create_first_window(items_with_prices)
    win_user_entry.mainloop()


def create_first_window(items_with_prices: List[Dict[str, str]]) -> tk.Tk:
    win_user_entry = tk.Tk()
    win_user_entry.title("Provisioner Token Helper")
    frm_coins = tk.Frame(master=win_user_entry, padx="24", pady="24")
    frm_coins.pack()
    lbl_coins = tk.Label(master=frm_coins, text="Max Cost (Silver)")
    ent_coins = tk.Entry(master=frm_coins, width=40)
    btn_coins = tk.Button(master=frm_coins, text="OK",
                          command=lambda: _create_and_display_items_buttons_prices(ent_coins, win_user_entry,
                                                                                   items_with_prices))
    lbl_coins.pack()
    ent_coins.pack(side=tk.LEFT)
    btn_coins.pack(side=tk.LEFT)
    return win_user_entry
