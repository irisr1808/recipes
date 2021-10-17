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
    lines_list = []
    ingredients_start = 0
    instruction_start = 0

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

        try:
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
                        ingredients_start = lines_list.index('מצרכים:')
                    if text_in == 'רכיבים':
                        ingredients_start = lines_list.index('רכיבים')
                    if 'הכנה' in text_in:
                        instruction_start = lines_list.index(text_in)

            if ingredients_start < instruction_start:
                lines = len(lines_list)
                for line_no in range(lines):
                    line_text = lines_list[line_no]
                    if ingredients_start < line_no < instruction_start:
                        print('ingredients ' + line_text)
                        if line_text.find('ראו הערות בתחתית המתכון') < 0 and line_text.find('מבצע לחגים') < 0 and line_text.find('לא בטוחים') < 0:
                            with sqlite3.connect('Recipes_data.db') as conn_d:
                                cursor = conn_d.cursor()
                                cursor.execute(f"""INSERT  INTO ingredients
                                                VALUES ('{row_id}', '{url}', '{line_text}')
                                                 """)
                                print('Ingredient Data inserted')
                    elif line_no > instruction_start:
                        if line_text.find('טיימר') < 0 and line_text != '+':
                            print('instructions ' + line_text)
                            step_instruction = line_text
                            with sqlite3.connect('Recipes_data.db') as conn_d:
                                cursor = conn_d.cursor()
                                cursor.execute(f"""INSERT  INTO instructions
                                            VALUES ('{row_id}', '{url}', '{step_no}' , '{step_instruction}')
                                             """)
                                step_no += 1
                                print('instruction data inserted')






                    # counter += 1
                    # if text_in == 'מצרכים:' or text_in == 'רכיבים':
                    #     ingredients_start = counter + 1
                    # if 'הכנה' in text_in:
                    #     instruction_start = counter + 1
        # except TypeError:
        #     pass
    # try:
    #         counter = 0
    #         for tag in recipe_ingredients:
    #             print('step2')
    #             if tag.text != '\n':
    #                 text_in = tag.text
    #                 text_in = text_in.replace('\n', '')
    #                 text_in = text_in.replace("'", '')
    #                 text_in = text_in.strip()
    #                 print('counter = ' + str(counter) + 'text_in = ' + text_in)
    #                 counter += 1
    #                 # try:
    #                 if ingredients_start < counter < instruction_start:
    #                     print('ingredients ' + text_in)
    #                     #if 'ראו הערות בתחתית המתכון' in text_in is False and 'מבצע לחגים' is False and 'לא בטוחים' in text_in is False:
    #                     if text_in.find('ראו הערות בתחתית המתכון') < 0 and text_in.find('מבצע לחגים') < 0 and text_in.find('לא בטוחים') < 0:
    #                         with sqlite3.connect('Recipes_data.db') as conn_d:
    #                             cursor = conn_d.cursor()
    #                             cursor.execute(f"""INSERT  INTO ingredients
    #                                             VALUES ('{row_id}', '{url}', '{text_in}')
    #                                              """)
    #                             print('Ingredient Data inserted')
    #
    #                 if counter > instruction_start:
    #                     # if 'טיימר' in text_in is False and text_in != '+':
    #                     if text_in.find('טיימר') < 0 and text_in != '+':
    #                         print('instructions ' + text_in)
    #                         step_instruction = text_in
    #                         with sqlite3.connect('Recipes_data.db') as conn_d:
    #                             cursor = conn_d.cursor()
    #                             cursor.execute(f"""INSERT  INTO instructions
    #                                         VALUES ('{row_id}', '{url}', '{step_no}' , '{step_instruction}')
    #                                          """)
    #                             print('instruction data inserted')
    #                         step_no += 1
        except TypeError:
            pass

    except AttributeError:
        pass
