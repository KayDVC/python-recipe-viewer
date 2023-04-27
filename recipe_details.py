from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QVBoxLayout, QWidget, \
                            QLabel, QTableWidget

class RecipeDetails(QWidget):
    """ Creates and displays a selected recipe with more details in user interface.
    
    Contains functions for creating graphical user interface (popup window) and displaying pertinent recipe
    information including image, name, description, ingredients, prep, and cook times.
    
    Utilizes the PyQt6 library to create, format, and display GUI. 

    Attributes:
        main_layout: a QtWidget.QVBoxLayout object to house children elements.
        img: a QLabel object that contains an image of the recipe.
        details: a QTableWidgetObject that contains the recipe's name, description, 
                 ingredients, prep, and cook times.
    """

    def __init__(self, img: QLabel, details: QTableWidget, *args):
        """Initializes object with passed image and details.

        Args:
            img: a QLabel object that contains an image of the recipe.
            details: a QTableWidgetObject that contains the recipe's name, description, 
                        ingredients, prep, and cook times.
        """
        super(RecipeDetails, self).__init__(*args)
        self._main_layout = None
        self._img = img
        self._details = details

        self._layout_ui()

    def _layout_ui(self):
        """Creates UI window containing img and details of recipe.

        Note: 
            Window is 400px*800px and should open on the top left corner of display when 
            thisObject.show() is called.
        """

        # set geometry
        self.setGeometry(QRect(100, 100, 400, 800))
        # create layout parent.
        self._main_layout = QVBoxLayout()
        self._main_layout.setContentsMargins(40, 20, 40, 20)
        self._main_layout.setSpacing(0)

        # add passed UI elements to main layout. 
        self._main_layout.addWidget(self._img)
        self._main_layout.addWidget(self._details)

        self.setLayout(self._main_layout)

        

