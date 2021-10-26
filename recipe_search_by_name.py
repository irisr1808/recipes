import sqlite3
import requests
from bs4 import BeautifulSoup


sqliteConnection = sqlite3.connect('Recipes_data.db')
conn = sqlite3.connect(':memory:')
sqliteConnection.backup(conn)
cursor = conn.cursor()
# cursor = conn.cursor()
autocommit = True


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


def search_by_name():
    # a function that search recipes from db by name
    search_name = input(
        '''Please enter what you are looking for
            For example type שוקולד if you want
            a chocolate cake or cookies 
            ''')

    search_name = '%' + search_name + '%'

    sqlite_select_recipes = "SELECT recipe_address , recipe_short_name FROM Address WHERE recipe_short_name like ?"
    all_rows = cursor.execute(sqlite_select_recipes, [search_name]).fetchall()
    print('The recipes links and names that include ' + search_name[1:-1] + ' are:')
    for row in all_rows:
        print(row[0] + ' , ' + row[1])


def search_with_ingredient():
    # a function that search recipes from db by ingredient
    search_ingredient = input('''
    Please type the desired ingredient
    For example type חמאת בוטנים
    ''')
    search_ingredient = '%' + search_ingredient + '%'

    sql_select_recipe_by_ingredient = '''SELECT   MIN(Address.id) 
                                        ,MIN(ingredients.ingredient)
                                        ,MIN(Address.recipe_address)
                                        ,MIN(Address.recipe_short_name)
                                        FROM ingredients
                                        INNER JOIN Address
                                        ON ingredients.recipe_id = Address.id
                                        WHERE ingredients.ingredient like ?
                                        GROUP BY Address.id
                                        '''

    all_rows = cursor.execute(sql_select_recipe_by_ingredient, [search_ingredient]).fetchall()
    # print('The recipes links and names that include ' + search_ingredient[1:-1] + ' are:')
    for row in all_rows:
        print('Link is ' + str(row[2]) + ' and recipe name is  ' + row[3])


def search_with_without_ingredient():
    # a function that search recipes from db by included ingredient and excluded ingredient
    search_with = input(
        '''Please enter the desired ingredient
            For example type שוקולד              
            ''')
    search_without = input(
        '''Please enter the un desired ingredient
            For example type חמאה              
            ''')
    list_id_with_ingredient = []
    list_id_without_ingredient = []
    sql_select_address = '''SELECT * FROM Address'''
    sql_select_ingredients = '''SELECT * FROM ingredients'''
    address_list = cursor.execute(sql_select_address).fetchall()
    ingredients_list = cursor.execute(sql_select_ingredients).fetchall()

    # find all address id with an ingredient
    # and put them in a list
    for recipe in ingredients_list:
        try:
            a = recipe[2]
            if search_with in recipe[2]:
                # recipe has the ingredient save recipe_id
                list_id_with_ingredient.append(recipe[0])
        except ValueError:
            pass
    # remove duplicates from list
    list_id_with_ingredient = list(dict.fromkeys(list_id_with_ingredient))
    # print('list with - ' + search_with + str(list_id_with_ingredient) + 'len = ' + str(len(list_id_with_ingredient)))

    # find all address id without an ingredient
    # and put them in a list
    for recipe in ingredients_list:
        try:
            a = recipe[2]
            if search_without in recipe[2]:
                # recipe has the ingredient save recipe_id
                list_id_without_ingredient.append(recipe[0])
        except ValueError:
            pass
    # remove duplicates from list
    list_id_without_ingredient = list(dict.fromkeys(list_id_without_ingredient))
    # print('list without - ' + search_without + str(list_id_without_ingredient))
    list_id_with_without_ingredient = list_id_with_ingredient.copy()
    for with_id in list_id_with_ingredient:
        for without_id in list_id_without_ingredient:
            if without_id == with_id:
                list_id_with_without_ingredient.remove(without_id)

    print('list with without is ' + str(list_id_with_without_ingredient) + 'len = ' + str(len(list_id_with_without_ingredient)))

    # print all the desired recipes
    for recipe in address_list:
        for id_with_without in list_id_with_without_ingredient:
            if recipe[0] == id_with_without:
                print(recipe[4] + ' - ' + recipe[2])


def main():
    # a function to choose thr desired search
    option = input('''
                    To search recipes  by recipe name type 1
                    To search recipes by specific ingredient type 2
                    To search recipes by specific ingredient included 
                        and specific ingredient excluded type 3  
                    ''')
    answers = ['1', '2', '3']
    if option in answers:

        if option == '1':
            search_by_name()
        elif option == '2':
            search_with_ingredient()
        elif option == '3':
            search_with_without_ingredient()
    else:
        print('Please select 1 2 or 3')


if __name__ == "__main__":
    main()
