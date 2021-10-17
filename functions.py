def clean_name(recipe_name):
    recipe_name = recipe_name.replace('\n', '')
    # replacements = [('\n', ''), ('!', ''), ("'", "")]
    recipe_name = recipe_name.replace('\n', '')
    recipe_name = recipe_name.replace('!', '')
    recipe_name = recipe_name.replace("'", "")
    # recipe_name = [recipe_name.replace(a, b) for a, b in replacements]
    recipe_name = recipe_name.rstrip()
    recipe_name = recipe_name.lstrip()

clean_name('        עוגות    ')
