from recipe import Recipe
from recipe_details import RecipeDetails
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, \
                            QLabel, QSpacerItem, QLineEdit, QPushButton, QTableWidget, \
                            QTableWidgetItem, QHeaderView, QSizePolicy, QAbstractItemView
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

import os

class RecipeUI(QMainWindow):
    """ Creates and displays recipes in user interface.
    
    Contains functions for creating graphical user interface (popup window) and displaying pertinent recipe
    information including image, name, prep, and cook times with the option to view additional detials.
    Displays information in a 4 * 2 grid. 
    
    Utilizes the PyQt6 library to create, format, and display GUI.

    Attributes:
        main_widget: QtWidget.QWidget object to house all other objects displayed. 
        main_layout: a QtWidget.QVBoxLayout object to house children elements.
        search_bar: a QtWidget.QHBoxLayout object to house search bar & accompanying buttons.
        recipe_table: a ditcionary containing a QtWidget.QGridLayout object to all recipe image & descriptions, 
                    list of widget objects inside Layout object.
        navigation: a ditcionary containing a QtWidget.QHBoxLayout object to navigation buttons, 
                    list of widget objects inside Layout object.
        navigation: a QtWidget.QProgressBar object to display the progress of recipe images downloading.
        page: an integer representing the current page of recipes being displayed.
        original_recipe_data : an unmodified list of Recipe objects to get data from.
        working_recipe_data: a potentially modified list of Recipe objects taken from original.
        popup : A QWidget object that serves as a secondary pop-up window for additional
                recipe details.
    """

    def __init__(self, *args): 
        super(RecipeUI, self).__init__(*args)
        self._main_widget = None
        self._main_layout = None
        self._search_bar = None
        self._recipe_table = {}
        self._navigation = {}
        self._progress_bar = None
        self._page = 0
        self._original_recipe_data = None
        self._working_recipe_data = None
        self._popup = None

        self._create_images_folder()
        self.setup_window()
        

    def setup_window(self) :
        """Creates UI window and sets window title. 
        """
        width = 1200
        height = 900

        # set window dimensions & title.
        self.setWindowTitle("Recipe Viewer V2")
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.setContentsMargins(0,0,0,0)
        self.menuBar().hide()
        self.statusBar().hide()

    def layout_ui(self, recipes: list[Recipe]):
        """Creates UI structure and adds content.

        Args: 
            recipes: A list of Recipe objects to get data from.
        """
        self._original_recipe_data = self._working_recipe_data = recipes

        # set main widget.
        self._main_widget = QWidget(self)
        self._main_widget.setContentsMargins(0,0,0,0)
        self.setCentralWidget(self._main_widget)

        # create layout parent.
        self._main_layout = QGridLayout()
        self._main_layout.setContentsMargins(40, 0, 40, 0)
        self._main_layout.setVerticalSpacing(0)

        # create UI elements to layout.
        self._search_bar = self._create_search_bar()

        self._recipe_table["components"] = []
        self._recipe_table["layout"] = self._create_recipe_table()

        self._navigation["components"] = []
        self._navigation["layout"] = self._create_navigation()

        # add created UI elements to main layout. 
        self._main_layout.addLayout(self._search_bar, 0,0)
        self._main_layout.addLayout(self._recipe_table["layout"], 1,0)
        self._main_layout.addLayout(self._navigation["layout"],2,0)

        self._main_widget.setLayout(self._main_layout)

    def _create_images_folder(self):
        """Creates images folder
        
        Note:
            Creates folder if it does not alreadt exist.
        """
        if (not os.path.exists("./images") ):
            os.mkdir("./images")

    ## --------------------------------------------
    ## Search Functions 
    ## --------------------------------------------
    def _create_search_bar(self) -> QHBoxLayout:
        """Creates search bar layout containing widgets used to search list.
        
        Returns:
            A QHBoxLayout object filled with the configured widgets necessary for 
            assigned search functionality.

        Note:
            Creates folder if it does not alreadt exist.
        """
        # create input line.
        input_box = QLineEdit()
        input_box.setPlaceholderText("Search for a recipe")
        

        # create search/reset button and assign functions on click.
        search_button = QPushButton("Search")
        search_button.clicked.connect(lambda: self._search_recipes(input_box.text()))
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(lambda: self._search_reset(input_box))

        # add setup input box and buttons to parent layout and return.
        element = QHBoxLayout()
        element.addWidget(input_box, 6)
        element.addWidget(search_button, 1)
        element.addWidget(reset_button, 1)
        element.setContentsMargins(-10, 0, 0, 0)
        
        return element
    
    def _search_recipes(self, search_str: str):
        """Updates the working recipe set to only include recipe names/description matching search query.
        
        Args:
            search_str : a string containing the user specified query.
        """

        # gather all recipes that contain desired words.
        matched_recipes = []
        for recipe in self._original_recipe_data:
            if ( (search_str in recipe.get_name()) or
                (search_str in recipe.get_description())
                ):
                matched_recipes.append(recipe)

        # display only matched recipes.
        self._working_recipe_data = matched_recipes
        self._refresh_recipes("first")

    def _search_reset(self, input_box: QLineEdit):
        """Adds all recipes back to working recipe set and clears search box.
        
        Note:
            Creates folder if it does not alreadt exist.
        """
        # clear input line.
        input_box.clear()
        # add all available recipes back to GUI.
        self._working_recipe_data = self._original_recipe_data
        self._refresh_recipes("first")

    ## --------------------------------------------
    ## Recipe Table Functions 
    ## --------------------------------------------
    def _create_configure_recipe_layout(self) -> QGridLayout:
        """Instantiates and configures a recipe table layout for later use.
        
        Returns:
            An empty, but configured QGridLayout object.
        """
        recipe_table = QGridLayout()
        recipe_table.setHorizontalSpacing(40)
        recipe_table.setVerticalSpacing(30)
        recipe_table.setContentsMargins(0, 0, 0, 0)

        return recipe_table

    def _make_recipe_table_spacer(self) -> QSpacerItem:
        """Instantiates a blank placeholder item to cover the space a regular recipeItem would.
        
        Returns:
            A QSpacerItem object of similar size to a normal recipe item.
        """
        return QSpacerItem(500, 350, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum )

    def _create_recipe_table(self) -> QGridLayout:
        """Creates recipe table layout fills it with recipe items.
        
        Returns:
            A QGridLayout object filled with the recipe images and details formatted to match 
            assigned display requirements.
        """
        # create and configure layout
        recipe_table = self._create_configure_recipe_layout()
        
        # create recipe items to display in 4*2 grid.
        start = self._page * 8
        for index in range(start, (start + 8)):

            # prevent out-of-bounds list access
            if (index >= len(self._working_recipe_data)):
                while index < start+ 8:
                    spacer = self._make_recipe_table_spacer()
                     # add to parent layout and dict of contained items.
                    recipe_table.addItem(spacer, ((index%8)//4), (index % 4))
                    self._recipe_table["components"].append(spacer)
                    index+= 1
                break

            recipe_data = self._working_recipe_data[index]

            # create container layout, setup component storage, and save raw recipe data for search functionality.
            recipe_item = { "layout": QVBoxLayout(), "components": {},"recipe_data": recipe_data}
            recipe_item["layout"].setSpacing(0)

            # create image, desc, and pop up with additional details.
            recipe_item["components"]["image"] = self._make_recipe_image(recipe_data)
            recipe_item["components"]["desc"] = self._make_recipe_description(recipe_data, index)
            recipe_item["components"]["more"] = self._make_more_recipe_details(recipe_data, index)

            for component in recipe_item["components"]:
                    if (component == "more"):
                        recipe_item["layout"].addWidget(recipe_item["components"][component])
                        recipe_item["layout"].setAlignment(recipe_item["components"][component],Qt.AlignmentFlag.AlignRight)
                    else:
                        recipe_item["layout"].addWidget(recipe_item["components"][component])

            # add to parent layout and dict of contained items.
            recipe_table.addLayout(recipe_item["layout"], ((index%8)//4), (index % 4))
            self._recipe_table["components"].append(recipe_item)
            
        return recipe_table

    def _make_recipe_image(self, recipe:Recipe, full_size: bool = False) -> QLabel:
        """Creates image widget for a given recipe.

        Args:
            recipe : a Recipe object with desired information.
            full_size : a Boolean that represents if an image should be made larger than normal.
                        False by default.

        Returns:
            A QLabel object containing the passed recipe's image scaled to an appropriate size.

        Note:
            Will download image and store in images folder if necessary.
        """
        img_location = "./images/" + recipe.get_image()
        scaled_size_height = 200 if not full_size else 300
        scaled_size_width = 300 if not full_size else 600

        # download image if necessary
        if(not os.path.exists(img_location)):
            recipe.set_image()

        # create Image widget, load data, and scale.
        element = QLabel()
        img = QPixmap(img_location)
        img = img.scaled(scaled_size_width, scaled_size_height, Qt.AspectRatioMode.KeepAspectRatio)
        element.setPixmap(img)
        element.setMaximumHeight(scaled_size_height)
        element.setMaximumWidth(scaled_size_width)
    
        return element
    
    def _make_recipe_description(self, recipe: Recipe, recipe_numb: int, full_details: bool = False)-> QTableWidget:
        """Creates table containing recipe info at specied level.

        Args:
            recipe : a Recipe object with desired information.
            recipe_numb : an Integer specifying the overall placement that the recipe will be when displayed.
                          Should be passed based on zero-index. Display will be in one-based index.
            full_details : a Boolean that represents if the table should contain all of the recipe's details or 
                           an abbreviated version. False by default.    
        Returns:
            A QTableWidget object containing the passed recipe's description at the specified level.
        """

        # create and configure widget.
        recipe_desc = QTableWidget()
        row_cnt = 4 if not full_details else 10
        col_cnt = 2
        
        if (not full_details):
            recipe_desc.setMaximumHeight(row_cnt * 40)

        recipe_desc.setRowCount(row_cnt)
        recipe_desc.setColumnCount(col_cnt)
        recipe_desc.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # hide headers
        recipe_desc.horizontalHeader().hide()  
        recipe_desc.verticalHeader().hide()

        for row in range(row_cnt):  # set height of individual rows
            recipe_desc.verticalHeader().setSectionResizeMode(row, QHeaderView.ResizeMode.Stretch)
        for col in range(col_cnt):  # set height of individual rows
            recipe_desc.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

        # add recipe data to table
        recipe_desc.setItem(0, 0, QTableWidgetItem("Recipe #:") )
        recipe_desc.setItem(0, 1, QTableWidgetItem(f"{recipe_numb+1}") )

        recipe_desc.setItem(1, 0, QTableWidgetItem("Recipe Name:") )
        recipe_desc.setItem(1, 1, QTableWidgetItem(recipe.get_name()) )

        recipe_desc.setItem(2, 0, QTableWidgetItem("Prep Time:") )
        recipe_desc.setItem(2, 1, QTableWidgetItem(recipe.get_prep_time()) )

        recipe_desc.setItem(3, 0, QTableWidgetItem("Cook Time:") )
        recipe_desc.setItem(3, 1, QTableWidgetItem(recipe.get_cook_time()) )

        # add in all details, if specified. Give these extra space in table.
        if (full_details):
            recipe_desc.setItem(4, 0, QTableWidgetItem("Description:") )
            recipe_desc.setItem(4, 1, QTableWidgetItem(recipe.get_description()) )
            recipe_desc.setSpan(4, 0, 3, 1)
            recipe_desc.setSpan(4, 1, 3, 1)

            recipe_desc.setItem(7, 0, QTableWidgetItem("Ingredients:") )
            recipe_desc.setItem(7, 1, QTableWidgetItem("\n".join(recipe.get_ingredients())) )
            recipe_desc.setSpan(7, 0, 3, 1)
            recipe_desc.setSpan(7, 1, 3, 1)

        return recipe_desc
    
    def _make_more_recipe_details(self, recipe: Recipe, recipe_numb: int) -> QPushButton:
        """Creates a button that will trigger recipe popup functionality when pressed.

        Args:
            recipe : a Recipe object with desired information.
            recipe_numb : an Integer specifying the overall placement that the recipe will be when displayed.
                          Should be passed based on zero-index. Display will be in one-based index.   
        Returns:
            A configured QPushButton object that displays the passed recipe in greater details when pressed.
        """

        # create button widgets & style.
        details_button = QPushButton("View Details")
        details_button.setStyleSheet(details_button.styleSheet() + " max-width: 100%;")

        # set button function
        details_button.clicked.connect(lambda: self._make_complete_recipe_popup(
            self._make_recipe_image(recipe, full_size=True), 
            self._make_recipe_description(recipe, recipe_numb, full_details=True)  ))
        
        return details_button


    def _make_complete_recipe_popup(self, img: QLabel, details: QTableWidget):
        """Creates and displays popup window with recipe details.

        Args:
            img : a QLabel object containing recipe's image.
            details : a QTableWidget containing the recipe's details.

        Note:
            Will open another small window.
        """
        self._popup = RecipeDetails(img, details)
        self._popup.show()

    ## --------------------------------------------
    ## Navigation Functions 
    ## --------------------------------------------
    def _create_navigation(self) -> QHBoxLayout:
        """Creates layout containing navigation widgets.
        
        Returns:
            A QHBoxLayout object filled with the widgets necessary to fulfill assigned navigation 
            functionality.
        """
        
        # create layout and button widgets.
        layout = QHBoxLayout()
        layout.setDirection(QHBoxLayout.Direction.RightToLeft)
        next_button = QPushButton("Next >")
        prev_button = QPushButton("< Prev")
        first_button = QPushButton("First")
        last_button = QPushButton("Last")

        # set button functions
        next_button.clicked.connect(lambda: self._refresh_recipes("next"))
        prev_button.clicked.connect(lambda: self._refresh_recipes("prev"))
        first_button.clicked.connect(lambda: self._refresh_recipes("first"))
        last_button.clicked.connect(lambda: self._refresh_recipes("last"))

        spacing = 12
        # ensure next/last buttons aren't avaiable when displaying last set of recipes.
        if (self._page < len(self._working_recipe_data)// 8 ):
            self._navigation["components"].append(next_button)
            self._navigation["components"].append(last_button)
        
        # ensure prev/first buttons aren't avaiable when displaying first set of recipes.
        if(self._page > 0):
            self._navigation["components"].append(first_button)
            self._navigation["components"].append(prev_button)
        
        # add widgets to layout.
        for widget in self._navigation["components"]:
            layout.addWidget(widget, 1)
        
        # add spacer to ensure consistent button sizing.
        layout.addStretch(spacing - len(self._navigation["components"]))
        self._navigation["components"].append(layout.itemAt(len(self._navigation["components"])))

        return layout

    ## --------------------------------------------
    ## "Reload" & "Remove" Functions 
    ## --------------------------------------------
    def _refresh_recipes(self, page: str):
        """Wipes displayed recipe table, gets another 8 recipes and displays them.

        Args:
            page: a string that contains the desired operation. 
            Expected values are :
                "next", "prev", "first", "last"

        Returns:
            A QGridLayout object filled with the recipe images and details formatted to match 
            assigned display requirements.

        Note:
            If page is not an expected value, the current recipes are regenerated and displayed.
        """
        # set page. 
        if(page == "next"):
            self._page += 1
        elif(page == "prev"):
            self._page -= 1
        elif(page == "first"):
            self._page = 0
        elif(page == "last"):
            self._page = len(self._working_recipe_data) // 8

        # clear and fetch recipes.
        self._remove_recipes()
        self._recipe_table["components"] = []
        self._recipe_table["layout"] = self._create_recipe_table()
        self._main_layout.addLayout(self._recipe_table["layout"], 1,0)

        # clear and display applicable navigation buttons.
        self._remove_navigation()
        # clear recipe items stored.
        self._navigation["components"] = []
        self._navigation["layout"] = self._create_navigation()
        self._main_layout.addLayout(self._navigation["layout"],2,0)

    def _remove_recipes(self):
        """Wipes displayed recipe table, gets another 8 recipes and displays them.

        Args:
            page: a string that contains the desired operation. 
            Expected values are :
                "next", "prev", "first", "last"

        Returns:
            A QGridLayout object filled with the recipe images and details formatted to match 
            assigned display requirements.

        Note:
            If page is not an expected value, the current recipes are regenerated and displayed.
        """
        # clear all recipe item widgets.
        for recipe_item in self._recipe_table["components"]:
            if (type(recipe_item) == QSpacerItem):
                self._recipe_table["layout"].removeItem(recipe_item)
            else:
                for component in recipe_item["components"]:
                        recipe_item["layout"].removeWidget(recipe_item["components"][component])
        
    def _remove_navigation(self):
        # clear all navigation buttons and spacing widgets.
        for item in self._navigation["components"]:
            if (type(item) == QSpacerItem):
                self._navigation["layout"].removeItem(item)
            else:
                self._navigation["layout"].removeWidget(item)

        


