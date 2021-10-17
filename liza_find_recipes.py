import requests
from bs4 import BeautifulSoup
import sqlite3

# get initial id_num
conn = sqlite3.connect('Recipes_data.db')
cursor = conn.cursor()
id_num = cursor.execute("SELECT MAX(id) FROM Address").fetchall()[0][0] + 1

# Reading all cakes and cookies recipes  in liza panelim
url_start = 'https://lizapanelim.com/category/%d7%9e%d7%a9%d7%95-%d7%9c%d7%a7%d7%99%d7%a0%d7%95%d7%97/'
site_name = 'liza'
recipe_owner = 'ליזה'
headers = {
  'User-Agent': 'Chrome/92.0.4515.159'
}


f = requests.get(url_start, headers=headers)
# recipes_lst = []
soup = BeautifulSoup(f.content, 'lxml')
# recipe_names = soup.find('div', {'class': 'line-clamp'}).find_all('h5')
recipe_names = soup.find_all(class_="elementor-post__title")
# recipe_names_len = recipe_names.__len__

for recipe in recipe_names:

    recipe_name = recipe.text
    recipe_name = recipe_name.replace('\n', '')
    recipe_name = recipe_name.replace('\t', '')
    recipe_name = recipe_name.replace('!', '')
    recipe_name = recipe_name.replace("'", "")
    recipe_name = recipe_name.rstrip()
    recipe_name = recipe_name.lstrip()
    recipe_full_address = recipe.contents[1].attrs
    recipe_full_address = recipe_full_address.get('href')
    print(str(id_num) + recipe_name)
    print(recipe_full_address)
    # Connecting to sqlite
    conn = sqlite3.connect('Recipes_data.db')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    # Insert address and recipe name into DB

    cursor.execute("INSERT OR IGNORE INTO Address(id, site_name, recipe_address, recipe_name, recipe_owner) VALUES(?,?,?,?,?)", (id_num, site_name, recipe_full_address, recipe_name, recipe_owner))
    # Commit your changes in the database
    conn.commit()
    # print('data inserted')
    id_num += 1
    # Closing the connection
    # conn.close()
