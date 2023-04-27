from ezgraphics import GraphicsImage, GraphicsWindow
from recipe import Recipe

class RecipeUI:
    """ Creates and displays recipes in user interface.
    
    Contains functions for creating graphical user interface (popup window) and displaying pertinent recipe
    information including image, name, prep, and cook times. Displays information in a 4 * 4 grid.
    
    Utilizes the EzGraphics module to create graphical UI. Note EzGraphics requires PIL module as well as
    requiring displayed images to be in GIF format.

    Attributes:
        gap: an integer representing the desired space between recipe data in pixels.
        width: an integer representing the width of the UI window in pixels.
        height: an integer representing the height of the UI window in pixels.
        window: an GraphicsWindow object user to display content.
        canvas: a GraphicsWinow.Canvas object used to add contained content.
    """

    def __init__(self): 
        self._gap = 60
        self._width = 1100
        self._height = 1000
        self._window = None
        self._canvas = None

        self.setup_window()

    def setup_window(self) :
        """Creates UI window, sets window title, and prep window for content addition. 
    
        """
        self._window = GraphicsWindow(self._width, self._height)
        self._window.setTitle("Recipe Viewer")
        self._canvas = self._window.canvas()


    def layout_ui(self, recipes: list):
        """Adds 16 recipes and pertinent information to UI.

        Args: 
            recipes: A list of Recipe objects to display from.
        """
        x = y = self._gap

        images_folder = "./images/"

        for recipe in recipes[:16]:

            # get image then, draw
            img = GraphicsImage(images_folder+recipe.get_image())
            img_width = img.width()
            img_height = img.height()

            self._canvas.drawImage(x , y, img)
            self.show_recipe_desc(recipe, x, (y + img_height))

            x, y = self._update_coords(x, y, img_width, img_height)
            
        self._window.wait()
            
    def show_recipe_desc(self, recipe: Recipe , x: int , y: int):
        """Adds name, prep time, and cook time to supplied coordinates.

        Args: 
            recipe: A Recipe object to get information from.
            x: an integer representing the x-coordinate to start displaying information at.
            y: an integer representing the y-coordinate to start displaying information at.
        """
        separation = self._gap // 6
        self._canvas.drawText(x, y, f"Name: {recipe.get_name()}")
        self._canvas.drawText(x, (y + separation), f"Prep Time: {recipe.get_prep_time()}")
        self._canvas.drawText(x, (y + (separation*2)), f"Cook Time: {recipe.get_cook_time()}")

    def _update_coords(self, x: int, y : int, width: int, height: int):
        """Updates x and y coordinates to display next recipe.

        Args: 
            x: an integer representing the current x-coordinate.
            y: an integer representing the current y-coordinate.
            width: an integer representing the width of the last image added.
            height: an integer representing the height of the last image added.

        Returns:
            Two integers containing the updated x and y coordinates.
        """
        # update x
        x += width + self._gap

        # ensure next image can fit in window. Vertical scrolling is fine
        if( (x + width + self._gap) > self._width ):
            x = self._gap
            y += height + self._gap
        
        return x, y
            
    
