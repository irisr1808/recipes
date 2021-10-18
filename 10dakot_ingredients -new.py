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
    # print(str(row_id))
    lines_list = []
    ingredients_start = 0
    instruction_start = 0

    try:

        f = requests.get(url, headers=headers)
        soup = BeautifulSoup(f.content, 'lxml')
        recipe_short_name = soup.find_all(class_="banner_resipe__title")[0].text
        recipe_short_name = recipe_short_name.replace("'", "")
        recipe_short_name = recipe_short_name.replace('"', '')
        recipe_short_name = recipe_short_name.replace("!", "")
        recipe_short_name = recipe_short_name.strip('\n')
        recipe_short_name = recipe_short_name.strip('\t')
        # print(recipe_short_name)
        with sqlite3.connect('Recipes_data.db') as conn_d:
            cursor = conn_d.cursor()
            cursor.execute(f"""UPDATE Address
                            SET recipe_short_name = '{recipe_short_name}'
                                WHERE Address.id = '{row_id}'
                                """)
        recipe_ingredients = soup.find_all(class_="resipes__content")[0]
        recipe_ingredients = recipe_ingredients.contents



        # try:
        for tag in recipe_ingredients:
            if tag != '\n':
                text_in = tag.text
                print(text_in)
                text_in = text_in.replace('\n', '')
                text_in = text_in.replace("'", '')
                text_in = text_in.replace('"', '')
                text_in = text_in.strip()
                lines_list.append(text_in)
                if text_in == 'מצרכים:':
                    ingredients_start = lines_list.index('מצרכים:') + 1
                if text_in == 'רכיבים':
                    ingredients_start = lines_list.index('רכיבים') + 1
                if 'הכנה' in text_in:
                    instruction_start = lines_list.index(text_in) + 1
        ingredient_count = 0
        instruction_count = 0
        # if ingredients_start < instruction_start:
        lines = len(lines_list)
        for line_no in range(1, lines):
            line_text = lines_list[line_no]
            if ingredients_start < line_no < instruction_start:
                ingredient_count += 1
                if ingredient_count < 10:
                    middle = '-00'
                else:
                    middle = '-0'
                ingredient_no = str(row_id) + middle + str(ingredient_count)

                if line_text.find('ראו הערות בתחתית המתכון') < 0 and \
                        line_text.find('מבצע לחגים') < 0 and \
                        line_text.find('לא בטוחים') < 0 and \
                        line_text.find('תבנית') < 0 and\
                        line_text.find('הכנה') < 0 and\
                        line_text.list != '' :
                    # print(str(line_no), line_text)
                    with sqlite3.connect('Recipes_data.db') as conn_d:
                        cursor = conn_d.cursor()
                        cursor.execute(f"""INSERT OR IGNORE INTO ingredients
                                        VALUES ('{row_id}', '{ingredient_no}', '{line_text}')
                                         """)
                        # print('Ingredient Data inserted')
            elif line_no > instruction_start:
                instruction_count += 1
                if instruction_count < 10:
                    middle = '-00'
                else:
                    middle = '-0'
                instruction_no = str(row_id) + middle + str(instruction_count)
                if line_text.find('טיימר') < 0 and \
                        line_text != '+' and\
                        line_text != '':
                    # print('instructions ' + line_text)
                    step_instruction = line_text
                    with sqlite3.connect('Recipes_data.db') as conn_d:
                        cursor = conn_d.cursor()
                        cursor.execute(f"""INSERT  INTO instructions
                                    VALUES ('{row_id}', '{instruction_no}' , '{step_instruction}')
                                     """)

        # except TypeError:
        #     pass

    except AttributeError:
        pass
