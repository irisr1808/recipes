import requests
from bs4 import BeautifulSoup
import sqlite3
# from functions import clean_name

# get initial id_num
conn = sqlite3.connect('Recipes_data.db')
cursor = conn.cursor()
id_num = cursor.execute("SELECT MAX(id) FROM Address").fetchall()[0][0] + 1
# Reading all cakes in carine


url_start_list = ['https://www.carine.co.il/category/%D7%A2%D7%95%D7%92%D7%95%D7%AA/?page=27', 'https://www.carine.co.il/category/%D7%A2%D7%95%D7%92%D7%99%D7%95%D7%AA-%D7%95%D7%9E%D7%90%D7%A4%D7%99%D7%9D-%D7%90%D7%99%D7%A9%D7%99%D7%99%D7%9D/%D7%A2%D7%95%D7%92%D7%99%D7%95%D7%AA/?page=10']
site_name = 'carine'
recipe_owner = 'קרין גורן'
headers = {
  'User-Agent': 'Chrome/92.0.4515.159'
}

for url_start in url_start_list:
    f = requests.get(url_start, headers=headers)
    recipes_lst = []
    soup = BeautifulSoup(f.content, 'lxml')
    # recipe_names = soup.find('div', {'class': 'line-clamp'}).find_all('h5')
    recipe_names = soup.find_all('h2')
    # recipe_names_len = recipe_names.__len__

    for recipe in recipe_names:

        recipe_name = recipe.text
        recipe_name = recipe_name.replace('\n', '')
        recipe_name = recipe_name.replace('\n', '')
        recipe_name = recipe_name.replace('!', '')
        recipe_name = recipe_name.replace("'", "")
        recipe_name = recipe_name.rstrip()
        recipe_name = recipe_name.lstrip()

        # recipe_name = clean_name(recipe_name)
        recipe_add_address = recipe_name.replace(" ", "-")
        print(recipe_add_address)
        recipe_full_address = 'https://www.carine.co.il/foody_recipe/' + recipe_add_address
        print(str(id_num) + 'is ' + recipe_full_address)
        # Connecting to sqlite
        # conn = sqlite3.connect('Recipes_data.db')

        # Creating a cursor object using the cursor() method
        # cursor = conn.cursor()
        # Insert address and recipe name into DB
        # id_num = cursor.execute("SELECT MAX(id) FROM Address").fetchall()[0][0] + 1
        cursor.execute("INSERT OR IGNORE INTO Address(id, site_name, recipe_address, recipe_name, recipe_owner) VALUES(?,?,?,?,?)", (id_num, site_name, recipe_full_address, recipe_name, recipe_owner) )
        # Commit your changes in the database
        conn.commit()
        # print('data inserted')
        id_num += 1
        # Closing the connection
conn.close()


