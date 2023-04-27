from recipe_processor import RecipeProcessor
from recipe_ui import RecipeUI
from PyQt6.QtWidgets import QApplication
import sys

def main():

    app = QApplication(sys.argv)

    # instantiate classes and load recipes
    rp = RecipeProcessor()
    rp.load_recipes("./recipes.json")
    
    # create UI and display recipes
    ui = RecipeUI()
    ui.layout_ui(rp.get_recipes())
    ui.show()
    sys.exit(app.exec())




if __name__ == "__main__":
    main()