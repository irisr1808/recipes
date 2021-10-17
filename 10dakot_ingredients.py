import sqlite3
import requests
from bs4 import BeautifulSoup


sqliteConnection = sqlite3.connect('Recipes_data.db')
cursor = sqliteConnection.cursor()
autocommit = True

sqlite_select_query = """SELECT * from Address WHERE site_name = '10dakot'"""
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
        try:

            f = requests.get(url, headers=headers)
            soup = BeautifulSoup(f.content, 'lxml')
            # recipe_short_name = soup.find_all(class_="banner_resipe__title")[0].text
            # recipe_short_name = recipe_short_name.replace("'", "")
            # recipe_short_name = recipe_short_name.replace('"', '')
            # recipe_short_name = recipe_short_name.replace("!", "")
            # recipe_short_name = recipe_short_name.strip('\n')
            # recipe_short_name = recipe_short_name.strip('\t')
            # print(recipe_short_name)
            # with sqlite3.connect('Recipes_data.db') as conn_d:
            #     cursor = conn_d.cursor()
            #     cursor.execute(f"""UPDATE Address
            #                     SET recipe_short_name = '{recipe_short_name}'
            #                         WHERE Address.id = '{row_id}'
            #                         """)
            recipe_ingredients = soup.find_all(class_="resipes__content")[0]
            recipe_ingredients = recipe_ingredients.contents

            tag_type = 'None'
            step_no = 1
            counter = 0
            # try:
            for tag in recipe_ingredients:
                if tag != '\n':
                    text_in = tag.text
                    print(text_in)
                    text_in = text_in.replace('\n', '')
                    text_in = text_in.replace("'", '')
                    text_in = text_in.replace('"', '')
                    text_in = text_in.strip()
                    counter += 1
                    if text_in == 'מצרכים:' or text_in == 'רכיבים':
                        ingredients_start = counter + 1
                    if 'הכנה' in text_in:
                        instruction_start = counter + 1
        # except TypeError:
        #     pass
            counter = 0
            for tag in recipe_ingredients:
                text_in = tag.next
                text_in = text_in.replace('\n', '')
                text_in = text_in.replace("'", '')
                text_in = text_in.strip()
                counter += 1
                # try:
                if ingredients_start < counter < instruction_start:
                    print('ingredients ' + text_in)
                    if 'ראו הערות בתחתית המתכון' in text_in == False and 'מבצע לחגים' == False and 'לא בטוחים' in text_in == False:
                        with sqlite3.connect('Recipes_data.db') as conn_d:
                            cursor = conn_d.cursor()
                            cursor.execute(f"""INSERT  INTO ingredients
                                            VALUES ('{row_id}', '{url}', '{text_in}')
                                             """)
                            print('Ingredient Data inserted')

                if counter >= instruction_start:
                    if 'טיימר' in text_in is False and text_in != '+':
                        print('instructions ' + text_in)
                        step_instruction = text_in
                        with sqlite3.connect('Recipes_data.db') as conn_d:
                            cursor = conn_d.cursor()
                            cursor.execute(f"""INSERT  INTO instructions
                                        VALUES ('{row_id}', '{url}', '{step_no}' , '{step_instruction}')
                                         """)
                            print('instruction data inserted')
                        step_no += 1
        except TypeError:
            pass

    except AttributeError:
        pass
