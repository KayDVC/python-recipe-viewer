import json

from recipe import Recipe
from waiting_window import WaitingWindow

class RecipeProcessor:
    """ Loads, validates, and stores recipes for later use.
    
    Contains functions for loading recipes from a JSON file, conversion of raw JSON to Recipe object, and storage of Recipe 
    objects.

    Utilizes the JSON(standard) and Requests(non-standard) modules to read/convert raw JSON data to standard data
    types.

    Attributes:
        recipes: a list of Recipe objects created after validating recipe data from JSON file.
    """
    
    def __init__(self):
        """Initializes the instance and creates empty recipe list"""

        self._recipes = []

    def load_recipes (self, json_file: str):
        """Fills recipe list up to n objects.

        Args:
            json_file : a string containing a path to JSON file containing recipe data.
            n : an integer specifying the desired recipe objects to be created.
        """

        # open file in read mode and get data.
        with open(json_file, mode='r') as file:
            data = json.load(file)

        # instantiate and display waiting window.
        waiting_window = WaitingWindow("Please wait, validating & creating recipe objects", data)
        waiting_window.exec()
        
        self._recipes = waiting_window.return_recipes()


    def get_recipes (self) :
        """Returns object's recipe list.

        Returns:
            A list of Recipe objects. Recipe list is of size n : specified during "self.load_recipes()" call
        """
        return self._recipes





