import requests
from bs4 import BeautifulSoup
import lxml
import shutil
import sqlite3

# requests_session = requests.session()


# Reading first page in mako
url1 = 'https://www.mako.co.il/food-recipes/recipes_column-cakes?Partner=blockscomp'

headers = {
  'User-Agent': 'Chrome/92.0.4515.159'
}
f = requests.get(url1, headers=headers)
recipes_lst = []
soup = BeautifulSoup(f.content, 'lxml')
# recipe_names = soup.find('div', {'class': 'line-clamp'}).find_all('h5')
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

    cursor.execute("INSERT OR IGNORE INTO Address(recipe_address, recipe_name) VALUES(?,?)", (recipe_full_address, recipe_name) )
# Commit your changes in the database
    conn.commit()
    # print('data inserted')

# Closing the connection
    conn.close()




"""
num = 0
for anchor in recipe_names:
    # urls = 'https://www.10dakot.co.il/category/%D7%9E%D7%AA%D7%9B%D7%95%D7%A0%D7%99%D7%9D-%D7%9C%D7%A2%D7%95%D7%92%D7%95%D7%AA/' + anchor['href']
    urls = 'https://www.mako.co.il' + anchor.text

    recipes_lst.append(url)

    num += 1
    recipe_url = urls
    recipe_f = requests.get(recipe_url, headers=headers)
    recipe_soup = BeautifulSoup(recipe_f.content, 'lxml')
    recipe_content = recipe_soup.find('div', {
       'class': 'recipe_synopsis clamp clamp-6 js-clamp'
    })
    print(num, url, '\n', 'recipe:' + anchor.string.strip())
    print('recipe info:' + recipe_content.string.strip())

"""
