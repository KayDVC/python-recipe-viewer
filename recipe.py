from PIL import Image
from isoduration import parse_duration
import requests, io

class Recipe: 
    """Stores recipe attributes for easy access.
    
    Contains functions for retrieving recipe inforamtion, validating the existence of an image for each image,
    Utilizes the JSON(standard) and Requests(non-standard) modules to read/convert raw JSON data to standard data
    types and then ensure "image" property of recipes are valid urls. 

    Utilizes PIL and IO modules to convert image format (JPG -> GIF), Requests module to ensure "image" property 
    of recipes are valid urls and capture content from a given url, and Isoduration to convert recipe cook and 
    prep times from ISO-8601 format to HH:MM format.

    Attributes:
        name: a string containing the recipe's name.
        cook_time: a string containing the recipe's cook time.
        prep_time: a string containing the recipe's prep time.
        recipe_yield: a string containing the recipe's yield.
        image_url: a string containing a webb address that opens to finished recipe's image.
    """

    def __init__(self, recipe):
        """Initializes a recipe object and stores basic recipe information.

        Args: 
            recipe: A dictionary containing recipe information. 

        Returns:
            A string containing the name of the finished recipe's image.
        """
        self.name = recipe["name"]
        self.cook_time = self._convert_time(recipe["cookTime"])
        self.prep_time = self._convert_time(recipe["prepTime"])
        self.recipe_yield = recipe["recipeYield"]
        self.image_url = recipe["image"]

    def get_name(self):
        """Returns object's name, if available.

        Returns:
            A string containing recipe's name.
        """
        return self.name

    def get_cook_time(self):
        """Returns object's cook time, if available.

        Returns:
            A string containing recipe's cook time in HH:MM format.
        """
        return self.cook_time

    def get_prep_time(self) -> str :
        """Returns object's prep time, if available.

        Returns:
            A string containing recipe's prep time in HH:MM format.
        """
        return self.prep_time

    def get_recipe_yield(self):
        """Returns object's yield, if available.

        Returns:
            A string containing recipe's yield.
        """
        return self.recipe_yield

    def set_image(self) :
        """Downloads the image associated with the recipe.

        Note:
            Stores image in GIF format under images folder.
        """

        img_name = self.get_image()

        # get image data in JPG format
        img_data = requests.get(self.image_url).content
        
        # convert JPG to GIF
        self._convert_to_gif(img_data, img_name)


    def get_image(self) -> str :
        """Returns the name of image linked to recipe.

        Returns:
            A string containing the name of the finished recipe's image with .gif extension.
        """
        # find last "/" of the url.
        for index in range(len(self.image_url), 0, -1):
            c = self.image_url[index -1 ]
            if ( c == "/" ):
                break
        # return string after last "/" without image extension
        return self.image_url[index:-4]+'.gif'
    
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

    def _convert_to_gif(self, img_data: bytes, img_name: str ):
        """Converts image data in JPG format to GIF format and stores under images folder.

        Args:
            img_data: a bytes object containing the raw data of the image.
            img_name: a string containing the desired name for the image.

        Note:
            Stores GIF image in images folder.
        """
        img_folder_path = "./images/"
        scaled_width = 200

        img = Image.open(io.BytesIO(img_data))
        percent_width = (scaled_width / float(img.size[0]))
        h_size = int(( float(img.size[1]) * float(percent_width) ))
        img = img.resize((scaled_width, h_size), Image.ANTIALIAS)
        img.save(img_folder_path + img_name)

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
