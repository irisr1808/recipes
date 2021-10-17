import requests
from bs4 import BeautifulSoup
import sqlite3


def get_ingredients_mako():

    # Connecting to sqlite
    conn = sqlite3.connect('Recipes_data.db')
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    # Insert address and recipe name into DB

    # id_num = cursor.execute("SELECT MAX(id) FROM Address").fetchall()[0][0] + 1
    # conn.commit()
    # url = 'https://www.mako.co.il/food-recipes/recipes_column-cakes/Recipe-584d6c1a46fdb71026.htm?sCh=131539cdf3178110&pId=25483675'
    headers = {
      'User-Agent': 'Chrome/92.0.4515.159'
    }
    for url in
    f = requests.get(url, headers=headers)
    soup = BeautifulSoup(f.content, 'lxml')
    recipe_data_owner = soup.find('div', {'class': 'writerData'}).find_all('span')
    # recipe_names = soup.find_all('h5')
    recipe_owner = str(recipe_data_owner[0].contents[0])
    recipe_data_name = soup.find('div', {'class': 'articleHeaderWrap'}).find_all('h1')
    recipe_short_name = str(recipe_data_name[0].contents[0])
    recipe_ingredients = soup.find('div', {'class': 'recipeContent'}).find_all('span')
    for Tag in recipe_ingredients:
        ingredient = str(Tag.contents[0])
    print('1')


get_ingredients_mako()
