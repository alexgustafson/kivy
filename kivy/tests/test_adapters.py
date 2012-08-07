'''
Adapter tests
=============
'''

import unittest

from kivy.uix.listview import ListItemButton
from kivy.adapters.listadapter import ListAdapter


class DataStore(object):

    def __init__(self, name, db_dict):
        self.name = name
        self.db_dict = db_dict

    def set(self, key, prop, val):
        if key in self.db_dict:
            if prop in self.db_dict[key]:
                self.db_dict[key][prop] = val
                return
            msg = "DataStore {0} set: no property {1} in record[{2}]".format(
                    self.name, prop, key)
            raise Exception(msg)
        msg = "DataStore {0} set: unknown record for key: {1}".format(
                self.name, key)
        raise Exception(msg)

    def get(self, key, prop):
        if key in self.db_dict:
            if prop in self.db_dict[key]:
                return self.db_dict[key][prop]
            msg = "DataStore {0} get: no property {1} in record[{2}]".format(
                    self.name, prop, key)
            raise Exception(msg)
        msg = "DataStore {0} get: unknown record for key: {1}".format(
                self.name, key)
        raise Exception(msg)
        return None

    def reset_to_defaults(self):
        for key in self.db_dict:
            self.set(key, 'is_selected', False)


# Data from http://www.fda.gov/Food/LabelingNutrition/\
#                FoodLabelingGuidanceRegulatoryInformation/\
#                InformationforRestaurantsRetailEstablishments/\
#                ucm063482.htm
fruit_categories = \
        {'Melons': {'fruits': ['Cantaloupe', 'Honeydew', 'Watermelon'],
                    'is_selected': False},
         'Tree Fruits': {'fruits': ['Apple', 'Avocado', 'Banana', 'Nectarine',
                                    'Peach', 'Pear', 'Pineapple', 'Plum',
                                    'Cherry'],
                         'is_selected': False},
         'Citrus Fruits': {'fruits': ['Grapefruit', 'Lemon', 'Lime', 'Orange',
                                      'Tangerine'],
                           'is_selected': False},
         'Miscellaneous Fruits': {'fruits': ['Grape', 'Kiwifruit',
                                             'Strawberry'],
                                  'is_selected': False}}

descriptors = """(gram weight/ ounce weight)	Calories	Calories from Fa
t	Total Fat	Sodium	Potassium	Total Carbo-hydrate	Dietary Fiber	Suga
rs	Protein	Vitamin A	Vitamin C	Calcium	Iron""".replace('\n', '')

descriptors = [item.strip() for item in descriptors.split('\t')]

units = """(g) 	(%DV)	(mg) 	(%DV)	(mg) 	(%DV)	 (g) 	(%DV)	 (g)
(%DV)	 (g) 	 (g) 	(%DV)	(%DV)	(%DV)	(%DV)""".replace('\n', '')

units = [item.strip() for item in units.split('\t')]

raw_fruit_data = [
{'name':'Apple',
 'Serving Size': '1 large (242 g/8 oz)',
 'data': [130, 0, 0, 0, 0, 0, 260, 7, 34, 11, 5, 20, 25, 1, 2, 8, 2, 2],
 'is_selected': False},
{'name':'Avocado',
 'Serving Size': '1/5 medium (30 g/1.1 oz)',
 'data': [50, 35, 4.5, 7, 0, 0, 140, 4, 3, 1, 1, 4, 0, 1, 0, 4, 0, 2],
 'is_selected': False},
{'name':'Banana',
 'Serving Size': '1 medium (126 g/4.5 oz)',
 'data': [110, 0, 0, 0, 0, 0, 450, 13, 30, 10, 3, 12, 19, 1, 2, 15, 0, 2],
 'is_selected': False},
{'name':'Cantaloupe',
 'Serving Size': '1/4 medium (134 g/4.8 oz)',
 'data': [50, 0, 0, 0, 20, 1, 240, 7, 12, 4, 1, 4, 11, 1, 120, 80, 2, 2],
 'is_selected': False},
{'name':'Grapefruit',
 'Serving Size': '1/2 medium (154 g/5.5 oz)',
 'data': [60, 0, 0, 0, 0, 0, 160, 5, 15, 5, 2, 8, 11, 1, 35, 100, 4, 0],
 'is_selected': False},
{'name':'Grape',
 'Serving Size': '3/4 cup (126 g/4.5 oz)',
 'data': [90, 0, 0, 0, 15, 1, 240, 7, 23, 8, 1, 4, 20, 0, 0, 2, 2, 0],
 'is_selected': False},
{'name':'Honeydew',
 'Serving Size': '1/10 medium melon (134 g/4.8 oz)',
 'data': [50, 0, 0, 0, 30, 1, 210, 6, 12, 4, 1, 4, 11, 1, 2, 45, 2, 2],
 'is_selected': False},
{'name':'Kiwifruit',
 'Serving Size': '2 medium (148 g/5.3 oz)',
 'data': [90, 10, 1, 2, 0, 0, 450, 13, 20, 7, 4, 16, 13, 1, 2, 240, 4, 2],
 'is_selected': False},
{'name':'Lemon',
 'Serving Size': '1 medium (58 g/2.1 oz)',
 'data': [15, 0, 0, 0, 0, 0, 75, 2, 5, 2, 2, 8, 2, 0, 0, 40, 2, 0],
 'is_selected': False},
{'name':'Lime',
 'Serving Size': '1 medium (67 g/2.4 oz)',
 'data': [20, 0, 0, 0, 0, 0, 75, 2, 7, 2, 2, 8, 0, 0, 0, 35, 0, 0],
 'is_selected': False},
{'name':'Nectarine',
 'Serving Size': '1 medium (140 g/5.0 oz)',
 'data': [60, 5, 0.5, 1, 0, 0, 250, 7, 15, 5, 2, 8, 11, 1, 8, 15, 0, 2],
 'is_selected': False},
{'name':'Orange',
 'Serving Size': '1 medium (154 g/5.5 oz)',
 'data': [80, 0, 0, 0, 0, 0, 250, 7, 19, 6, 3, 12, 14, 1, 2, 130, 6, 0],
 'is_selected': False},
{'name':'Peach',
 'Serving Size': '1 medium (147 g/5.3 oz)',
 'data': [60, 0, 0.5, 1, 0, 0, 230, 7, 15, 5, 2, 8, 13, 1, 6, 15, 0, 2],
 'is_selected': False},
{'name':'Pear',
 'Serving Size': '1 medium (166 g/5.9 oz)',
 'data': [100, 0, 0, 0, 0, 0, 190, 5, 26, 9, 6, 24, 16, 1, 0, 10, 2, 0],
 'is_selected': False},
{'name':'Pineapple',
 'Serving Size': '2 slices, 3" diameter, 3/4" thick (112 g/4 oz)',
 'data': [50, 0, 0, 0, 10, 0, 120, 3, 13, 4, 1, 4, 10, 1, 2, 50, 2, 2],
 'is_selected': False},
{'name':'Plum',
 'Serving Size': '2 medium (151 g/5.4 oz)',
 'data': [70, 0, 0, 0, 0, 0, 230, 7, 19, 6, 2, 8, 16, 1, 8, 10, 0, 2],
 'is_selected': False},
{'name':'Strawberry',
 'Serving Size': '8 medium (147 g/5.3 oz)',
 'data': [50, 0, 0, 0, 0, 0, 170, 5, 11, 4, 2, 8, 8, 1, 0, 160, 2, 2],
 'is_selected': False},
{'name':'Cherry',
 'Serving Size': '21 cherries; 1 cup (140 g/5.0 oz)',
 'data': [100, 0, 0, 0, 0, 0, 350, 10, 26, 9, 1, 4, 16, 1, 2, 15, 2, 2],
 'is_selected': False},
{'name':'Tangerine',
 'Serving Size': '1 medium (109 g/3.9 oz)',
 'data': [50, 0, 0, 0, 0, 0, 160, 5, 13, 4, 2, 8, 9, 1, 6, 45, 4, 0],
 'is_selected': False},
{'name':'Watermelon',
 'Serving Size': '1/18 medium melon; 2 cups diced pieces (280 g/10.0 oz)',
 'data': [80, 0, 0, 0, 0, 0, 270, 8, 21, 7, 1, 4, 20, 1, 30, 25, 2, 4],
 'is_selected': False}]

fruit_data = {}
descriptors_and_units = dict(zip(descriptors, units))
for row in raw_fruit_data:
    fruit_data[row['name']] = {}
    fruit_data[row['name']] = dict({'Serving Size': row['Serving Size'],
                                    'is_selected': row['is_selected']},
            **dict(zip(descriptors_and_units.keys(), row['data'])))

# See the dictionary definitions above for fruit category and raw data
# creation. From those dictionaries, we define two datastores that will be
# used in the examples:

datastore_categories = DataStore(name='categories', db_dict=fruit_categories)
datastore_fruits = DataStore(name='fruits', db_dict=fruit_data)


class AdaptersTestCase(unittest.TestCase):

    def setUp(self):
        self.args_converter = lambda x: {'text': x,
                                         'size_hint_y': None,
                                         'height': 25}
        self.fruits = sorted(fruit_data.keys())

        datastore_categories.reset_to_defaults()
        datastore_fruits.reset_to_defaults()

    def test_list_adapter_selection_mode_none(self):
        list_adapter = ListAdapter(data=self.fruits,
                                   datastore=datastore_fruits,
                                   args_converter=self.args_converter,
                                   selection_mode='none',
                                   allow_empty_selection=True,
                                   cls=ListItemButton)

        self.assertEqual(list_adapter.data, ['Apple', 'Avocado', 'Banana',
            'Cantaloupe', 'Cherry', 'Grape', 'Grapefruit', 'Honeydew',
            'Kiwifruit', 'Lemon', 'Lime', 'Nectarine', 'Orange', 'Peach',
            'Pear', 'Pineapple', 'Plum', 'Strawberry', 'Tangerine',
            'Watermelon'])

        self.assertEqual(list_adapter.cls, ListItemButton)
        self.assertEqual(list_adapter.args_converter, self.args_converter)
        self.assertEqual(list_adapter.template, None)

        apple_data_item = list_adapter.get_item(0)
        self.assertTrue(isinstance(apple_data_item, str))
