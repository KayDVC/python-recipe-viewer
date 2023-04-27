from recipe_processor import RecipeProcessor
from recipe_ui import RecipeUI

def main():
    
    # instantiate classes and load recipes
    rp = RecipeProcessor();
    rp.load_recipes("./recipes.json", 50)

    # create UI and display recipes
    ui = RecipeUI()
    ui.layout_ui(rp.get_recipes())

    # display recipe data in table format.
    rp.tabulate_recipes()


if __name__ == "__main__":
    main()