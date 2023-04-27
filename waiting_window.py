from recipe import Recipe
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QVBoxLayout, QDialog, QWidget, \
                            QLabel, QProgressBar, QApplication

import json
class WaitingWindow(QDialog):
    """ Creates and displays a "loading" window with a progress bar.
    
    Contains functions for creating graphical user interface (popup window) and displaying operation progress.

    Utilizes the PyQt6 library to create, format, and display GUI.

    Attributes:
        main_layout : a QtWidget.QVBoxLayout object to house children elements.
        progress_bar_label : a QLabel object containing label passed to object.
        progress_bar : a QProgressBar that represents the overall completion for a certain task.
        label : a String containing the text to display along with progress bar.
        recipes : a list of Recipe objects to be returned.
        current_task : an Integer representing the progress of tasks.
    """

    def __init__(self, label: str, data: list , *args):
        """Initializes object with passed tasks to complete.

        Args:
            label : a String containing the text to display along with progress bar.
            data : a list containing recipe data data.
        """
        super(WaitingWindow, self).__init__(*args)
        self._main_layout = None
        self._progress_bar_label = None
        self._progress_bar = None
        self._label = label
        self._todo = len(data)
        self._current_task = 1
        self._recipes = []
        self._layout_ui()
        QTimer.singleShot(1, lambda: self._load_recipes(data))
        

    def _layout_ui(self):
        self.setWindowTitle("Please Wait")
        # create layout parent.
        self._main_layout = QVBoxLayout()
        self._main_layout.setContentsMargins(40, 20, 40, 20)
        self._main_layout.setSpacing(0)

        # create label and progress bar.
        self._progress_bar = QProgressBar()
        self._progress_bar_label = QLabel()

        # configure widgets.
        self._progress_bar.setRange(self._current_task, self._todo)
        self._progress_bar_label.setText(f"{self._label} ({self._current_task}/{self._todo})" )
        

        self._main_layout.addWidget(self._progress_bar_label)
        self._main_layout.addWidget(self._progress_bar)

        self.setLayout(self._main_layout)

    def _completed_task(self):

        # increment current task.
        self._current_task += 1
        self._progress_bar_label.setText(f"{self._label} ({self._current_task}/{self._todo})" )

        # close window if all tasks complete or update progress bar.
        if (self._current_task >= self._todo):
            self.close()
        else:
            self._progress_bar.setValue(self._current_task)


    def _load_recipes(self, data: list ):
        # save all recipes
        for recipe in data:
            QApplication.processEvents()

            if( Recipe.valid_recipe(recipe)):
                # Add all valid recipes to list
                self._recipes.append( Recipe(recipe))

            # update progress bar in waiting window.
            self._completed_task()

    def return_recipes(self):
        return self._recipes
    