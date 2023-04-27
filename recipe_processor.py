import json, os

from recipe import Recipe

class RecipeProcessor:
    """ Loads, validates, and stores recipes for later use.
    
    Contains functions for loading recipes from a JSON file, conversion of raw JSON to Recipe object, storage of Recipe 
    objects, and styling of data for UI display.
    
    Utilizes the JSON(standard) and Requests(non-standard) modules to read/convert raw JSON data to standard data
    types. Os module is used for displaying progress bar properly and creating images folder.

    Attributes:
        recipes: a list of Recipe objects created after validating recipe data from JSON file.
    """
    
    def __init__(self):
        """Initializes the instance and creates empty recipe list"""

        self._recipes = []

    def load_recipes (self, json_file: str, n: int = 16):
        """Fills recipe list up to n objects.

        Args:
            json_file : a string containing a path to JSON file containing recipe data.
            n : an integer specifying the desired recipe objects to be created.
        """

        # open file in read mode and get data.
        with open(json_file, mode='r') as file:
            data = json.load(file)
        
        # get n recipes and save for later use
        index = 0
        while (len(self._recipes) != n):
            recipe = data[index]

            # validate recipe image before adding to list
            if( Recipe.valid_recipe(recipe) ):
                self._recipes.append( Recipe(recipe))

            # continue through list.
            index += 1

        self._download_images()

    def get_recipes (self) :
        """Returns object's recipe list.

        Returns:
            A list of Recipe objects. Recipe list is of size n : specified during "self.load_recipes()" call
        """
        return self._recipes

    def tabulate_recipes(self):
        """Prints all recipe names, prep times, cook times, and yields in table format.

        """
        # useful strings
        divider = "- " * 80 
        
        # table heading
        print(divider)
        print(self._formatted_string("Name", "Prep Time", "Cook Time", "Yield"))
        print(divider)

        for recipe in self._recipes:
            print(self._formatted_string( recipe.get_name(), recipe.get_prep_time(), recipe.get_cook_time(), recipe.get_recipe_yield()))

        print(divider)

    def _clear(self):
        """ Clears standard output.

        """
        # windows
        if os.name == 'nt':
            _ = os.system('cls')
        #  mac and linux
        else:
            _ = os.system('clear')

    def _print_progress(self, completed, total):
        """Creates progress bar with text-based graphics .

        Args:
            completed : an integer representing the amount of images downloaded and converted.
            total : an integer representing the total amount of images to be downloaded and converted.

        Returns:
            A string containing information on the progress of image downloading based on passed params.
        """
        colored_bar = "\u001b[32;1m\u2588"
        reset_color = "\u001b[0m"

        return f"Downloading and converting image {completed} of {total}   {colored_bar*(completed//3) + reset_color}"

    def _download_images(self) :
        """Dowloads all images in recipe list.

        Note:
            Downloads all images and stores them under images folder in GIF format.
        """

        # create images folder
        self._create_images_folder()

        self._print_progress(0, len(self._recipes))
        for index, recipe in enumerate(self._recipes):
            # limit progress bar updates to reasonable amount.
            if (index % 3 == 0):
                self._clear()
                print(self._print_progress(index, len(self._recipes)))
            # download every image. Store under images folder.
            recipe.set_image()

    def _formatted_string(self, name: str, prep_time: str, cook_time: str, recipe_yield: str):
        """Prints all recipe names, prep times, cook times, and yields in table format.
        
        Args:
            name: a string containing the recipe's name.
            prep_time: a string containing the recipe's prep time.
            cook_time: a string containing the recipe's cook time.
            recipe_yield: a string containing the recipe's yield.

        Returns:
            A string properly formatted in the following order: name, prep time , cook time, recipe yield.
        """
        # tabulation sizes
        name_space = 75
        prep_time_space = cook_time_space = 15
        recipe_yield_space = 25

        return '{:{name_space}}{:<{prep_time_space}}{:<{cook_time_space}}{:<{recipe_yield_space}}'.format(
            name, '|  ' + prep_time, '|  ' + cook_time, '|  ' + recipe_yield, 
            name_space=name_space, prep_time_space=prep_time_space, 
            cook_time_space=cook_time_space, recipe_yield_space=recipe_yield_space)

    def _create_images_folder(self):
        """Creates images folder
        
        Note:
            Creates folder if it does not alreadt exist.
        """
        if (not os.path.exists("./images") ):
            os.mkdir("./images")





