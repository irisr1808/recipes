import sqlite3
import requests
from bs4 import BeautifulSoup


sqliteConnection = sqlite3.connect('Recipes_data.db')
cursor = sqliteConnection.cursor()
autocommit = True

sqlite_select_query = """SELECT * from Address WHERE site_name = 'mako'"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
headers = {
      'User-Agent': 'Chrome/92.0.4515.159'
    }
for row in records:
    url = (row[2])
    if url[0] == "'":
        url = url[1:-1]
    row_id = row[0]
    print(str(row_id))

    if row_id > 1001411:

        f = requests.get(url, headers=headers)
        soup = BeautifulSoup(f.content, 'lxml')
        try:
            recipe_instructions = soup.find('div', {'class': 'recipeInstructions ArticleText fontSize'}).find_all('p')
            for inst in recipe_instructions:
                try:
                    if inst.contents[0].next != '\n' and 'strong' not in inst.contents[0].next and 'href' not in inst.contents[0].next and 'script type' not in inst.contents[0].next:
                        try:
                            recipe_instructions_no = inst.contents[0].next
                        except IndexError:
                            recipe_instructions_no = recipe_instructions_no
                        try:
                            recipe_instructions_no = recipe_instructions_no.replace("'", "")
                        except TypeError:
                            pass
                        try:
                            recipe_step = str(inst.contents[1])
                            recipe_step = recipe_step.replace("'", "")
                        except IndexError:
                            recipe_step = ''
                        # remove error step_no s
                        try:
                            recipe_instructions_no = recipe_instructions_no.replace("<small>", "")
                            recipe_instructions_no = recipe_instructions_no.replace("</small>", "")
                        except TypeError:
                            pass
                        instruction_step = str(row_id) + '-' + str(recipe_instructions_no)
                        print(str(recipe_instructions_no) + " - " + recipe_step)
                        # if recipe_instructions_no.find('strong') or recipe_instructions_no.find('href') or recipe_instructions_no.find('script'):
                        #     pass
                        # else:
                        if len(recipe_step) > 1 :
                            with sqlite3.connect('Recipes_data.db') as conn_d:
                                cursor = conn_d.cursor()
                                cursor.execute(f"""INSERT OR IGNORE  INTO instructions
                                            VALUES ('{row_id}', '{instruction_step}' , '{recipe_step}')
                                             """)
                except IndexError:
                    pass
        except AttributeError:
            pass
cursor.close()
