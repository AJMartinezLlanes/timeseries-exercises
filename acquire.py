
import os
import requests
import pandas as pd

# fresh stores data from website
def get_store_data_from_api():
    response = requests.get('https://api.data.codeup.com/api/v1/stores')
    data = response.json()
    stores = pd.DataFrame(data['payload']['stores'])
    stores = pd.DataFrame(stores)
    return stores

# fresh items data from website
def get_items_data_from_api():
    domain = 'https://api.data.codeup.com'
    endpoint = '/api/v1/items'
    items = []
    while endpoint != None:
        url = domain + endpoint
        response = requests.get(url)
        data = response.json()
        print(f'\rGetting page {data["payload"]["page"]} of {data["payload"]["max_page"]}: {url}', end='')
        items.extend(data['payload']['items'])
        endpoint = data['payload']['next_page']
    items = pd.DataFrame(items)
    return items

# fresh sales data from website
def get_sales_data_from_api():
    base_url = 'https://api.data.codeup.com/api/v1/sales?page='
    sales = []
    url = base_url + str(1)
    response = requests.get(url)
    data = response.json()
    max_page = data['payload']['max_page']
    sales.extend(data['payload']['sales'])
    page_range = range(2, max_page + 1)

    for page in page_range:
        url = base_url + str(page)
        print(f'\rFetching page {page}/{max_page} {url}', end='')
        response = requests.get(url)
        data = response.json()
        sales.extend(data['payload']['sales'])
    sales = pd.DataFrame(sales)
    return sales

# get stores data function
def get_stores_data():
    if os.path.exists('stores.csv'):
        return pd.read_csv('stores.csv')
    df = get_store_data_from_api()
    df.to_csv('stores.csv', index=False)
    return df

# get items data function
def get_items_data():
    if os.path.exists('items.csv'):
        return pd.read_csv('items.csv')
    df = get_items_data_from_api()
    df.to_csv('items.csv', index=False)
    return df

# get sales data function
def get_sales_data():
    if os.path.exists('sales.csv'):
        return pd.read_csv('sales.csv')
    df = get_sales_data_from_api()
    df.to_csv('sales.csv', index=False)
    return df

# all data merged into one
def get_all_store_data():
    sales = get_sales_data()
    stores = get_stores_data()
    items = get_items_data()

    sales = sales.rename(columns={'store': 'store_id', 'item': 'item_id'})
    df = pd.merge(sales, stores, how='left', on='store_id')
    df = pd.merge(df, items, how='left', on='item_id')

    return df

# opsd data
def get_opsd_data():
    if os.path.exists('opsd.csv'):
        return pd.read_csv('opsd.csv')
    df = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
    df.to_csv('opsd.csv', index=False)
    return df
