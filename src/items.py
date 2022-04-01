import csv
import json
from typing import List, Dict

from client import GW2Client


def _get_items_from_csv() -> List[Dict[str, str]]:
    """
    We keep a local copy of the item id and item name for each crafted item that can be traded for provisioner tokens.
    This method reads the csv file and builds a list of dictionaries of item ids and names.
    :return: List[Dict[str,str]] of item id and name pairs.
    """
    items = []
    with open("resources/all_items.csv", 'r') as infile:
        reader = csv.reader(infile)
        for line in reader:
            item_id = line[0]
            name = line[1]
            items.append({'id': item_id, 'name': name})
    return items


def _get_items_prices(items_input: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    This method queries the guild wars 2 commerce API to get item prices for each item in the list provided, and
    returns a similar list of dictionaries of item id, name, and price triplets.
    :param items_input: A List of dictionaries of item name and id pairs.
    :return: List[Dict[str,str]] of item id, name, and price triplets
    """
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


def get_best_item_per_vendor(items_with_prices: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    This method checks vendor offerings against their current prices, and selects the lowest-price item from each
    vendor's 6-item offering.
    :param items_with_prices: A List of Dicts of item id, name, and price triplets.
    :return: List[Dict[str, str]] of the best item id, name, price triplets for each vendor.
    """
    best_items = []
    with open("resources/provisioner_token_items.json", 'r') as infile:
        json_items_list: Dict = json.load(infile)
        for vendor, tabs in json_items_list.items():
            for tab in tabs:
                for tab_name, items in tab.items():
                    six_items = _create_group_of_6(items, items_with_prices)
                    best_item = _choose_best_of_6(six_items)
                    best_items.append(best_item)
    return best_items


def _create_group_of_6(items_json: List[Dict[str, str]], items_with_prices: List[Dict[str, str]]) -> List[
    Dict[str, str]]:
    """
    Creates a 6-item liss of dicts of item id, name and price based on a vendor's offerings.
    :param items_json: List[Dict[str, str]] of a vendor's item name and id pairs
    :param items_with_prices: List[Dict[str, str]] of all item name, id and price triplets
    :return: List[Dict[str, str]] of the 6 item id, name, price triplets for this vendor
    """
    output_items = []
    for item in items_json:
        for item_with_price in items_with_prices:
            if item['id'] == item_with_price['id']:
                output_item = {'id': item['id'], 'name': item['name'], 'price': item_with_price['price']}
                output_items.append(output_item)
    return output_items


def _choose_best_of_6(items: List[Dict[str, str]]) -> Dict[str, str]:
    """
    Takes a list of 6 items from a vendor, and ouputs the cheapest option.
    :param items: List[Dict[str, str]] of a vendor's item id, name, price triplets
    :return: Dict[str, str] a dictionary of the cheapest item id, name and price triplet
    """
    best = 9999999999
    best_item = None
    for item in items:
        price = int(item['price'])
        if int(item['price']) < best:
            best = price
            best_item = item
    return best_item


def get_items_within_price_threshold(threshold: int, items: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Takes a threshold value, and removes any of the items in the list that exceed this price limit.
    :param threshold: int value above which items are removed from consideration
    :param items: List[Dict[str, str]] of the best item id, name, price triplets for each vendor
    :return: List[Dict[str, str]] of the valid item id, name, price triplets for each vendor
    """
    output_items = []
    for item in items:
        if int(item['price']) <= threshold:
            output_items.append(item)
    return output_items
