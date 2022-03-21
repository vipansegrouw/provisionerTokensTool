import json
import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Tuple
import pyperclip
import csv

from client import GW2Client


def create_output(entry, window, items):
    ceiling = int(entry.get()) * 100
    items = get_best_items(items)
    items = get_culled_items(ceiling, items)
    for widget in window.winfo_children():
        widget.destroy()

    create_second_window(items, window)
    window.update()


def get_items_from_csv() -> List[Dict[str, str]]:
    items = []
    with open("./resources/all_items.csv", 'r') as infile:
        reader = csv.reader(infile)
        for line in reader:
            id = line[0]
            name = line[1]
            items.append({'id': id, 'name': name})
    return items


def get_items_prices(items_input):
    items_output = []
    ids = [item['id'] for item in items_input]
    client = GW2Client()
    response = client.get_prices_from_api(ids)
    for instance in response:
        for item in items_input:
            if str(instance['id']) == item['id']:
                appender = {'id': str(instance['id']), 'name': item['name'], 'price': instance['sells']['unit_price']}
                items_output.append(appender)
    return items_output


def get_best_items(items_with_prices):
    best_items = []
    with open("./resources/provisioner_token_items.json", 'r') as infile:
        json_items_list: Dict = json.load(infile)
        for vendor, tabs in json_items_list.items():
            for tab in tabs:
                for tab_name, items in tab.items():
                    six_items = make_group_of_6(items, items_with_prices)
                    best_item = choose_best_of_6(six_items)
                    best_items.append(best_item)
    return best_items


def get_culled_items(ceiling, items):
    output_items = []
    for item in items:
        if int(item['price']) <= int(ceiling):
            output_items.append(item)
    return output_items


def choose_best_of_6(items):
    best = 9999999999
    best_item = None
    for item in items:
        price = int(item['price'])
        if int(item['price']) < best:
            best = price
            best_item = item
    return best_item


def make_group_of_6(items_json, items_with_prices):
    output_items = []
    for item in items_json:
        for item_with_price in items_with_prices:
            if item['id'] == item_with_price['id']:
                output_item = {'id': item['id'], 'name': item['name'], 'price': item_with_price['price']}
                output_items.append(output_item)
    return output_items


def create_list(master, items_list):
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
    tk.Button(master=master, textvariable=button_label, command=lambda: copy_to_clipboard(txt_item, button_label)).grid(column=2, row=idx + 1)
    tk.Label(master=master, text=f"{txt_price}", justify=tk.RIGHT).grid(column=3, row=idx + 1)
    button_label.set("Copy")


def create_second_window(items, window):
    mainframe = ttk.Frame(master=window, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky="N, W, E, S")
    create_list(mainframe, items)
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)


def user_entry_window(items):
    win_user_entry = _create_first_window(items)
    win_user_entry.mainloop()


def _create_first_window(items):
    win_user_entry = tk.Tk()
    win_user_entry.title("Provisioner Token Helper")
    frm_coins = tk.Frame(master=win_user_entry, padx="24", pady="24")
    frm_coins.pack()
    # v = tk.IntVar()
    # v.set(1)
    # radios = [("Sells", 1),
    #           ("Buys", 2)]
    #
    # for radio, val in radios:
    #     tk.Radiobutton(frm_coins,
    #                    text=radio,
    #                    padx=20,
    #                    variable=v,
    #                    command=lambda: v.set(val),
    #                    value=val).pack(anchor=tk.W)

    lbl_coins = tk.Label(master=frm_coins, text="Max Cost (Silver)")
    ent_coins = tk.Entry(master=frm_coins, width=40)
    btn_coins = tk.Button(master=frm_coins, text="OK", command=lambda: create_output(ent_coins, win_user_entry, items))
    lbl_coins.pack()
    ent_coins.pack(side=tk.LEFT)
    btn_coins.pack(side=tk.LEFT)
    return win_user_entry


def main():
    items = get_items_from_csv()
    items = get_items_prices(items)
    print(items)
    user_entry_window(items)


def write_script():
    items_list = []
    ids = []
    count = 0
    with open("./resources/provisioner_token_items.json", 'r') as infile:
        json_dict: Dict = json.load(infile)
        for vendor, tabs in json_dict.items():
            for tab in tabs:
                for tab_name, items in tab.items():
                    for item in items:
                        id = item['id']
                        name = item['name']
                        count += 1
                        if id not in ids:
                            id_and_name = [id, name]
                            ids.append(id)
                            items_list.append(id_and_name)

    with open("./resources/all_items.csv", 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(items_list)


if __name__ == "__main__":
    main()
