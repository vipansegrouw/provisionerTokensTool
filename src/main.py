from gui import user_entry_window
from items import _get_items_from_csv, _get_items_prices


def main():
    items = _get_items_from_csv()
    items = _get_items_prices(items)
    user_entry_window(items)


if __name__ == "__main__":
    main()
