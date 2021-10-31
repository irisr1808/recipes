import sqlite3
import requests
from bs4 import BeautifulSoup


sqliteConnection = sqlite3.connect('Recipes_data.db')
cursor = sqliteConnection.cursor()
autocommit = True

# Find a list of all the recipes from carine site
sqlite_select_query = """SELECT * from Address WHERE site_name = 'carine'"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
headers = {
      'User-Agent': 'Chrome/92.0.4515.159'
    }
for row in records:
    url = (row[2])
    row_id = row[0]

    ingredient_no = 0

    # Check there is a short recipe name
    try:

        f = requests.get(url, headers=headers)
        soup = BeautifulSoup(f.content, 'lxml')
        recipe_short_name = soup.find_all('h1')[0].text
        recipe_short_name = recipe_short_name.replace("'", "")
        recipe_short_name = recipe_short_name.replace('"', '')
        recipe_short_name = recipe_short_name.replace("!", "")
        recipe_short_name = recipe_short_name.strip('\n')
        recipe_short_name = recipe_short_name.strip('\t')
        # print(recipe_short_name)

        # Update the recipe short name into the database
        with sqlite3.connect('Recipes_data.db') as conn_d:
            cursor = conn_d.cursor()
            cursor.execute(f"""UPDATE Address
                            SET recipe_short_name = '{recipe_short_name}'
                                WHERE Address.id = '{row_id}'
                                """)

        # Insert all the ingredients into the database
        recipe_ingredients = soup.find_all(class_='ingredient-container')
        for Tag in recipe_ingredients:
            ingredient = Tag.text
            ingredient = ingredient.replace('\n', '')
            ingredient = ingredient.replace("'", "")
            ingredient = ingredient.strip()
            ingredient = ' '.join(ingredient.split())
            ingredient_no += 1
            if ingredient_no < 10:
                ingredient_middle = '-00'
            else:
                ingredient_middle = '-0'

            ingredient_combine_no = str(row_id) + ingredient_middle + str(ingredient_no)

            # Insert the ingredients with ingredient number
            with sqlite3.connect('Recipes_data.db') as conn_d:
                cursor = conn_d.cursor()
                cursor.execute(f"""INSERT OR IGNORE INTO ingredients
                                VALUES ('{row_id}', '{ingredient_combine_no}', '{ingredient}')
                                 """)
    except IndexError:
        pass
cursor.close()
