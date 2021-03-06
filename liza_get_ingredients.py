import sqlite3
import requests
from bs4 import BeautifulSoup


sqliteConnection = sqlite3.connect('Recipes_data.db')
cursor = sqliteConnection.cursor()
autocommit = True

sqlite_select_query = """SELECT * from Address WHERE site_name = 'liza'"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
headers = {
      'User-Agent': 'Chrome/92.0.4515.159'
    }
for row in records:
    url = (row[2])
    row_id = row[0]
    print(str(row_id))
    try:

        f = requests.get(url, headers=headers)
        soup = BeautifulSoup(f.content, 'lxml')
        recipe_short_name = soup.find_all('h1')[0].text
        recipe_short_name = recipe_short_name.replace("'", "")
        recipe_short_name = recipe_short_name.replace('"', '')
        recipe_short_name = recipe_short_name.replace("!", "")
        recipe_short_name = recipe_short_name.strip('\n')
        recipe_short_name = recipe_short_name.strip('\t')
        print(recipe_short_name)

        # Insert the recipe short name
        with sqlite3.connect('Recipes_data.db') as conn_d:
            cursor = conn_d.cursor()
            cursor.execute(f"""UPDATE Address
                            SET recipe_short_name = '{recipe_short_name}'
                                WHERE Address.id = '{row_id}'
                                """)
        recipe_ingredients = soup.find_all('br')
        tag_type = 'None'
        step_no = 1
        counter = 0

        # Check if the ingredient line has data and clean it
        try:
            for tag in recipe_ingredients:
                text_in = tag.next
                text_in = text_in.replace('\n', '')
                text_in = text_in.replace("'", '')
                text_in = text_in.strip()
                text_in = text_in.replace('&nbsp', '')
                counter += 1
                if text_in == 'מה צריכים:' or text_in == 'לעוגה:':
                    ingredients_start = counter + 1
                if text_in == 'איך מכינים?':
                    instruction_start = counter + 1
                if text_in[0:3] == '1. ':
                    instruction_start = counter
        except TypeError:
            pass
        counter = 0

        # Check if the ingredient line has data and clean it
        try:
            for tag in recipe_ingredients:
                text_in = tag.next
                text_in = text_in.replace('\n', '')
                text_in = text_in.replace("'", '')
                text_in = text_in.strip()
                counter += 1
                try:
                    if ingredients_start < counter < instruction_start:
                        print('ingredients ' + text_in)
                        if counter < 10:
                            middle = '-00'
                        else:
                            middle = '-0'
                        ingredient_no = str(row_id) + middle + str(counter)
                        with sqlite3.connect('Recipes_data.db') as conn_d:
                            cursor = conn_d.cursor()
                            cursor.execute(f"""INSERT OR IGNORE INTO ingredients
                                            VALUES ('{row_id}', '{ingredient_no}', '{text_in}')
                                             """)

                except NameError:
                    pass
        except TypeError:
            pass

    except IndexError:
        pass
# cursor.close()
