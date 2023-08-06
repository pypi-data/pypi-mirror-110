# get_chefkoch
[![Downloads](https://pepy.tech/badge/get-chefkoch)](https://pepy.tech/project/get-chefkoch)
[![PyPI version](https://badge.fury.io/py/get-chefkoch.svg)](https://badge.fury.io/py/get-chefkoch)
[![GitHub](https://img.shields.io/github/license/olzeug/get_chefkoch)](https://github.com/olzeug/get_chefkoch/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/get-chefkoch/badge/?version=latest)](https://get-chefkoch.readthedocs.io/en/latest/?badge=latest)

Python library to interact with Chefkoch.

## Examples:

```python
from get_chefkoch import Recipe, Search

s = Search("Apfelstrudel")
recipe = s.recipes(limit=1)
print(recipe.name)
print(recipe.description)
```

```python
from get_chefkoch import Recipe, Search

recipe = Search().recipeOfTheDay()

print(recipe.name)
print(recipe.description)
```

## Recipe-Class Parameters:
     name              Name of the recipe
     id                Unique identification of the recipe
     description       Description of the recipe
     image             Url of a beautiful picture of the recipe
     ingredients       Recipe ingredients
     category          Recipe category
     prepTime          Preparation time
     totalTime         Total Time
     cooktime          Cooking time
     
     Many more parameters are available after calling Recipe().data_dump()

## Features:

- Query the recipe of the day
- Search for specific recipe
- Querying information about a recipe(cooking time, description, ingredients, ...)
- Use the automatic suggestions from Chefkoch

## Get it now:

```
pip install get-chefkoch
```
