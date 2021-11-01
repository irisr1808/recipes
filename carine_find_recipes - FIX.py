import requests
from bs4 import BeautifulSoup
import sqlite3
# from functions import clean_name

# get initial id_num
conn = sqlite3.connect('Recipes_data.db')
cursor = conn.cursor()
id_num = cursor.execute("SELECT MAX(id) FROM Address").fetchall()[0][0] + 1

# Reading all cakes recipes in carine


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
    recipe_names = soup.find_all('h2')


    # Clean the recipe name to minimize it
    for recipe in recipe_names:
        try:
            try:
                recipe_name = recipe.text
                recipe_name = recipe_name.replace('\n', '')
                recipe_name = recipe_name.replace('\n', '')
                recipe_name = recipe_name.replace('!', '')
                recipe_name = recipe_name.replace("'", "")
                recipe_name = recipe_name.rstrip()
                recipe_name_n = recipe_name.lstrip()
                recipe_new_address = recipe.contents[1].attrs['href']
                # recipe_1 = recipe_address[1].attrs['href']
                print(recipe_new_address + ' - ' + recipe_name)
                # sql_update_address = "UPDATE Address SET recipe_address = ? WHERE recipe_name = ?"

                # cursor.execute(f"""UPDATE Address
                #                 SET recipe_address = '{recipe_new_address}'
                #                     WHERE recipe_name = '{recipe_name_n}'
                #                     """)
                # # Commit your changes in the database
                # conn.commit()
            except sqlite3.IntegrityError:
                pass
        except IndexError:
            pass


        # Insert id, site_name, recipe_address, recipe_name, recipe_owner into database
        # cursor.execute("INSERT OR IGNORE INTO Address(id, site_name, recipe_address, recipe_name, recipe_owner) VALUES(?,?,?,?,?)", (id_num, site_name, recipe_full_address, recipe_name, recipe_owner) )
        # cursor.execute("UPDATE Address SET recipe_address = recipe_new_address WHERE recipe_name = recipe_name_n")
        # Commit your changes in the database
        # conn.commit()
        # Increment the id counter
        id_num += 1
# Closing the connection
conn.close()


