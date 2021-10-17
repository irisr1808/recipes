import requests
from bs4 import BeautifulSoup
import sqlite3

# requests_session = requests.session()


# Reading other  pages in 10 dakot
# url_start = 'https://www.10dakot.co.il/category/%D7%9E%D7%AA%D7%9B%D7%95%D7%A0%D7%99%D7%9D-%D7%9C%D7%A2%D7%95%D7%92%D7%95%D7%AA/'
site_name = '10dakot'
recipe_owner = 'efrat_10dakot'
headers = {
  'User-Agent': 'Chrome/92.0.4515.159'
}
# get initial id_num
conn = sqlite3.connect('Recipes_data.db')
cursor = conn.cursor()
id_num = cursor.execute("SELECT MAX(id) FROM Address").fetchall()[0][0] + 1

url_cakes = 'https://www.10dakot.co.il/category/%D7%9E%D7%AA%D7%9B%D7%95%D7%A0%D7%99%D7%9D-%D7%9C%D7%A2%D7%95%D7%92%D7%95%D7%AA/?page='
url_cookies = 'https://www.10dakot.co.il/category/%D7%9E%D7%AA%D7%9B%D7%95%D7%A0%D7%99%D7%9D-%D7%9C%D7%A2%D7%95%D7%92%D7%99%D7%95%D7%AA/?page='
url_start_list = [url_cakes, url_cookies]
for url_start in url_start_list:
    if url_start == url_cakes:
        no_of_pages = 17
    else:
        no_of_pages = 10
    for page_no in range(1, no_of_pages):
        url = url_start + str(page_no)
        if page_no == 1:
            if url_start == url_cakes:
                url = 'https://www.10dakot.co.il/category/%d7%9e%d7%aa%d7%9b%d7%95%d7%a0%d7%99%d7%9d-%d7%9c%d7%a2%d7%95%d7%92%d7%95%d7%aa/'
            elif url_start == url_cookies:
                url = 'https://www.10dakot.co.il/category/%d7%9e%d7%aa%d7%9b%d7%95%d7%a0%d7%99%d7%9d-%d7%9c%d7%a2%d7%95%d7%92%d7%99%d7%95%d7%aa/'

        f = requests.get(url, headers=headers)
        soup = BeautifulSoup(f.content, 'lxml')
        recipe_data = soup.find_all(class_="categories__item")
        print('page no is ' + str(page_no))
        for recipe in recipe_data:
            try:
                try:
                    recipe_address = recipe.attrs['href']
                    recipe_name = recipe.text
                    recipe_name = recipe_name.replace('\n', '')
                    recipe_name = recipe_name.replace('!', '')
                    recipe_name = recipe_name.replace("'", "")
                    recipe_name = recipe_name.rstrip()
                    recipe_name = recipe_name.lstrip()
                    print(str(id_num) + ' is ' + recipe_address)
                    # Connecting to sqlite
                    conn = sqlite3.connect('Recipes_data.db')

                    # Creating a cursor object using the cursor() method
                    cursor = conn.cursor()
                    # Insert address and recipe name into DB
                    if recipe_name not in {'מתכונים לעוגות', \
                                            'לחצו לסינון', 'סנן לפי:', '…', \
                                            'הראו שאתם לא רובוט', 'הגדל טקסט   זכוכית מגדלת', 'הדגשת קישורים', \
                                            'פונט נגיש', 'טוען...', 'כתוב הערה אישית למתכון', \
                                           }:
                        cursor.execute("INSERT OR IGNORE INTO Address(id, site_name, recipe_address, recipe_name, recipe_owner) VALUES(?,?,?,?,?)", (id_num, site_name, recipe_address, recipe_name, recipe_owner) )
                    # Commit your changes in the database
                        conn.commit()
                        print('data inserted')
                    id_num += 1


                    # Closing the connection
                    conn.close()
                except TypeError:
                    pass
            except IndexError:
                pass

