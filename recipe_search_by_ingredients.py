import sqlite3
import regex as re

sqliteConnection = sqlite3.connect('Recipes_data.db')
cursor = sqliteConnection.cursor()
autocommit = True

search_ingredient = input('Please insert the name of the ingredient you want to search ')
search_ingredient = '%' + search_ingredient + '%'
quantity_search = input('Do you want specific quantity? \n'
                        'Please reply Y or N  ')
if quantity_search == 'Y':

    ingredient_unit = input('Please insert measure unit\n'
                            'For tea spoon insert 1\n'
                            'For spoon insert 2\n'
                            'For cup insert 3\n'
                            'for weight in grams insert 4\n'
                            '')
    ingredient_quantity = input('Please insert the quantity of the unit you chose ')
sql_search_by_ingredient_only = '''SELECT Address.recipe_short_name
                            , ingredients.recipe_address
                            ,ingredients.ingredient
                            FROM ingredients
                            LEFT JOIN Address
                            ON ingredients.id = Address.id
                            WHERE ingredients.ingredient like ?'''

all_rows = cursor.execute(sql_search_by_ingredient_only, [search_ingredient]).fetchall()
print('The recipes links and names that include ' + search_ingredient + ' are:')
for row in all_rows:
    print(row[0] + ' , ' + row[1])
