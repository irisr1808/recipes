import sqlite3
import requests
from bs4 import BeautifulSoup

# insert recipe_short name and recipe_owner in table Address
# insert ingredient_no and ingredient in table ingredients
# ingredient_no is unique and includes recipe_id and ingredient counter
sqliteConnection = sqlite3.connect('Recipes_data.db')
cursor = sqliteConnection.cursor()
autocommit = True

# Select a list of the recipes from mako site
sqlite_select_query = """SELECT * from Address WHERE site_name = 'mako'"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
headers = {
      'User-Agent': 'Chrome/92.0.4515.159'
    }
for row in records:
    url = (row[2])
    row_id = row[0]
    # print(str(row_id))

    # if row_id > 1002191:

    f = requests.get(url, headers=headers)
    soup = BeautifulSoup(f.content, 'lxml')
    if soup.find('div', {'class': 'writerData'}):
        recipe_data_owner = soup.find('div', {'class': 'writerData'}).find_all('span')
        # Check there is a recipe owner in the url page
        # If there is no owner insert None
        try:
            recipe_owner = str(recipe_data_owner[0].contents[0])
            recipe_owner = recipe_owner.replace("'", "")
        except IndexError:
            recipe_owner = 'None'

    else:
        recipe_owner = 'None'
    if soup.find('div', {'class': 'articleHeaderWrap'}):
        # Check there is a recipe short name in the url page
        # If there is no short name insert None
        try:
            recipe_data_name = soup.find('div', {'class': 'articleHeaderWrap'}).find_all('h1')
            recipe_short_name = str(recipe_data_name[0].contents[0])
            recipe_short_name = recipe_short_name.replace("'", "")
        except IndexError:
            recipe_short_name = 'None'
    else:
        recipe_short_name = 'None'

    # Insert the short name and the owner into the database
    with sqlite3.connect('Recipes_data.db') as conn_d:
        cursor = conn_d.cursor()
        cursor.execute(f"""UPDATE Address
                        SET recipe_short_name = '{recipe_short_name}' ,
                            recipe_owner = '{recipe_owner}'
                            WHERE id = '{row_id}'
                            """)

    if soup.find('div', {'class': 'ingredients'}):
        recipe_ingredients = soup.find('div', {'class': 'ingredients'}).find_all('span')
        ingredient_counter = 0
        ingredient_seperator = '-00'
        for Tag in recipe_ingredients:
            ingredient = Tag.text
            ingredient = ingredient.replace('\n','')
            ingredient = ingredient.replace("'", "")

            if ingredient != '' and ingredient != ' ':
                ingredient_counter += 1
                if ingredient_counter > 9:
                    ingredient_seperator = '-0'

                ingredient_no = str(row_id) + ingredient_seperator + str(ingredient_counter)

                # Insert the  ingredient_id , ingredient number and ingredient into the database
                with sqlite3.connect('Recipes_data.db') as conn_d:
                    cursor = conn_d.cursor()
                    cursor.execute(f"""INSERT  OR IGNORE INTO ingredients
                                    VALUES ('{row_id}', '{ingredient_no}', '{ingredient}')
                                     """)

    else:
        recipe_ingredients = 'None'

cursor.close()
