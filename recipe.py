from isoduration import parse_duration
import requests

class Recipe: 
    """Stores recipe attributes for easy access.
    
    Contains functions for retrieving recipe inforamtion, validating the existence of an image for each image,
    Utilizes the JSON(standard) and Requests(non-standard) modules to read/convert raw JSON data to standard data
    types and then ensure "image" property of recipes are valid urls. 

    Utilizes Requests module to ensure "image" property of recipes are valid urls and capture content from a given url
    and Isoduration to convert recipe cook and prep times from ISO-8601 format to HH:MM format.

    Attributes:
        name: a string containing the recipe's name.
        cook_time: a string containing the recipe's cook time.
        prep_time: a string containing the recipe's prep time.
        recipe_yield: a string containing the recipe's yield.
        image_url: a string containing a web address that opens to finished recipe's image.
        desc: a string containing the recipe's description.
        ingredients: a list of strings containing the recipe's ingredients.
    """

    def __init__(self, recipe):
        """Initializes a recipe object and stores basic recipe information.

        Args: 
            recipe: A dictionary containing recipe information. 

        Returns:
            A string containing the name of the finished recipe's image.
        """
        self._name = recipe["name"]
        self._cook_time = self._convert_time(recipe["cookTime"])
        self._prep_time = self._convert_time(recipe["prepTime"])
        self._recipe_yield = recipe["recipeYield"]
        self._image_url = recipe["image"]
        self._desc = recipe["description"]
        self._ingredients = recipe["ingredients"]

    def get_name(self):
        """Returns object's name, if available.

        Returns:
            A string containing recipe's name.
        """
        return self._name

    def get_cook_time(self):
        """Returns object's cook time, if available.

        Returns:
            A string containing recipe's cook time in HH:MM format.
        """
        return self._cook_time

    def get_prep_time(self) -> str :
        """Returns object's prep time, if available.

        Returns:
            A string containing recipe's prep time in HH:MM format.
        """
        return self._prep_time

    def get_recipe_yield(self):
        """Returns object's yield, if available.

        Returns:
            A string containing recipe's yield.
        """
        return self._recipe_yield
    
    def get_description(self):
        """Returns object's description, if available.

        Returns:
            A string containing recipe's description.
        """
        return self._desc

    def get_ingredients(self):
        """Returns object's ingredients, if available.

        Returns:
            A list containing recipe's ingredients.
        """
        return self._ingredients

    def set_image(self) :
        """Downloads the image associated with the recipe.

        Note:
            Stores image in jpg format under images folder.
        """

        img_name = "./images/" + self.get_image()

        # get image data in JPG format
        img_data = requests.get(self._image_url).content
        
        with open(img_name, 'wb') as file:
            file.write(img_data)


    def get_image(self) -> str :
        """Returns the name of image linked to recipe.

        Returns:
            A string containing the name of the finished recipe's image with .gif extension.
        """
        # find last "/" of the url.
        for index in range(len(self._image_url), 0, -1):
            c = self._image_url[index -1 ]
            if ( c == "/" ):
                break
        # return string after last "/" without image extension
        return self._image_url[index:-4]+'.jpg'
    
    @staticmethod
    def valid_recipe(recipe: dict):
        """Determines if recipe valid to add. Image must be in JPG format and url to image must be valid.

        Args:
            recipe: a dictionary containing various properties including "image".

        Returns:
            True if image validation conditions met.
        """
        url = recipe["image"]
        return _valid_format(url) and _valid_image(url)

    def _convert_time(self, iso_time: str):
        """Converts a string from ISO-8601 format to HH:MM format

        Args:
            iso_time: a string containing the a time duration in ISO-8601 format.

        Returns:
            A string containing the passed time duration in HH:MM format.

        Note:
            Hours are not capped, but minutes are (60 >= mins equal to +1 hour).
        """
        
        # handle case: time empty
        if (len(iso_time) < 1):
            return "00:00"
        
        # convert to integer based object
        duration = parse_duration(iso_time).time
        hours = duration.hours
        minutes = duration.minutes

        # convert minutes to hours if necessary
        if (minutes >= 60):
            hours += minutes // 60
            minutes = minutes % 60

        # return in HH:MM format
        return f"{hours:02}:{minutes:02}"
        

def _valid_format(url: str):
    """Determines if image is in JPG format.

    Args:
        url: a web address link to image.

    Returns:
        True if image in JPG format.
    """
    return url[-3:] == "jpg"

def _valid_image(url: str):
    """Fetches response from given url.

    Args:
        url: a web address link to image.

    Returns:
        True if url can be opened and contains a file.
    """

    valid = True
    
    # try to open url. Ensure response is okay.
    response = requests.get(url)
    if (response.status_code != 200) :
        valid = False

    return valid
