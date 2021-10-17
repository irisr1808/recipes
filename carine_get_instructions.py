import sqlite3
import requests
from bs4 import BeautifulSoup


sqliteConnection = sqlite3.connect('Recipes_data.db')
cursor = sqliteConnection.cursor()
autocommit = True

sqlite_select_query = """SELECT * from Address WHERE site_name = 'carine'"""
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
        step_no = 1
        try:
            recipe_instructions = soup.find_all(class_='foody-content')
            inst = recipe_instructions[1].contents[2].text
            inst_step = inst.split('.')
            # inst_step = inst_step.replace('\n', '')
            steps_count = len(inst_step)
            for step_num in range(steps_count):
                print(str(step_no ) + ' - ' + inst_step[step_num])
                step_instruction = inst_step[step_num]
                step_instruction = step_instruction.replace('\n', '')
                step_instruction = step_instruction.replace("'", '')
                if steps_count > 0 and step_instruction != '':
                    if step_no <10:
                        middle = '-00'
                    else:
                        middle = '-0'
                    step_no_combo = str(row_id) + middle + str(step_no)
                    with sqlite3.connect('Recipes_data.db') as conn_d:
                        cursor = conn_d.cursor()
                        cursor.execute(f"""INSERT  OR IGNORE INTO instructions
                                    VALUES ('{row_id}', '{step_no_combo}' , '{step_instruction}')
                                     """)
                # insert into sql
                    step_no += 1
        except IndexError:
            pass
    except IndexError:
        pass
# cursor.close()
