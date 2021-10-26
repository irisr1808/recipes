import requests
from bs4 import BeautifulSoup
import sqlite3


# Reading first page in mako
url1 = 'https://www.mako.co.il/food-recipes/recipes_column-cakes?Partner=blockscomp'
site_name = 'mako'
id_num = 1000001
headers = {
  'User-Agent': 'Chrome/92.0.4515.159'
}
f = requests.get(url1, headers=headers)
recipes_lst = []
soup = BeautifulSoup(f.content, 'lxml')

recipe_names = soup.find_all('h5')

for addresses in recipe_names:
    recipe_name = addresses.text
    recipe_data = addresses.contents
    recipe_add_address = recipe_data[0].attrs['href']
    recipe_full_address = "'" + 'https://www.mako.co.il' + recipe_add_address + "'"
    # print(recipe_name)
    # print(recipe_add_address)
    # print(recipe_full_address)
# Connecting to sqlite
    conn = sqlite3.connect('Recipes_data.db')

# Creating a cursor object using the cursor() method
    cursor = conn.cursor()
# Insert address and recipe name into DB

    cursor.execute("INSERT OR IGNORE INTO Address(id, site_name, recipe_address, recipe_name) VALUES(?,?,?,?)", (id_num, site_name, recipe_full_address[1:-1], recipe_name) )
# Commit your changes in the database
    conn.commit()
    # print('data inserted')
    id_num += 1
# Closing the connection
    conn.close()
