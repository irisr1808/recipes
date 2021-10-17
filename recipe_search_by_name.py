import sqlite3
import requests
from bs4 import BeautifulSoup


sqliteConnection = sqlite3.connect('Recipes_data.db')
cursor = sqliteConnection.cursor()
autocommit = True

# sqlite_select_query = """SELECT * from Address WHERE site_name = 'carine'"""
# cursor.execute(sqlite_select_query)
# records = cursor.fetchall()
# headers = {
#       'User-Agent': 'Chrome/92.0.4515.159'
#     }


def blogs_choose():
    blogs = input('''Please choose the blogs you want to search\n
                        For MAKO choose 1\n
                        For 10 Dakot choose 2\n
                        For Liza Panelim choose 3\n
                        For Carine Goren choose 4\n
                        For all sites press enter\n
                        insert the desired blog(s) number(s)\n
                        ''')
    blogs_list = []
    if '1' in blogs:
        blogs_list.append('mako')
    if '2' in blogs:
        blogs_list.append('10dakot')
    if '3' in blogs:
        blogs_list.append('liza')
    if '4' in blogs:
        blogs_list.append('carine')
    if blogs == '':
        blogs_list = ['mako', '10dakot', 'liza', 'carine']
    print(str(blogs_list))
    # with sqlite3.connect('Recipes_data.db') as conn_d:
    #     cursor = conn_d.cursor()
    #     cursor.execute(f"""INSERT  INTO ingredients
    #                     VALUES ('{row_id}', '{url}', '{ingredient}')
    #                      """)


def search_by_name():
    search_name = input('Please enter the desired ingredient')
    #  recipes = cursor.execute('SELECT recipe_address , recipe_short_name FROM Address WHERE recipe_short_name like ?', ("'%'" + search_name + "'%'",))
    search_name = '%' + search_name + '%'

    sqlite_select_recipes = "SELECT recipe_address , recipe_short_name FROM Address WHERE recipe_short_name like ?"
    all_rows = cursor.execute(sqlite_select_recipes, [search_name]).fetchall()
    print('The recipes links and names that include ' + search_name[1:-1] + ' are:')
    for row in all_rows:
        print(row[0] + ' , ' + row[1])





# blogs_choose()
search_by_name()
