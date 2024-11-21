import sys
from PySide6 import QtWidgets, QtCore
import statsapi
from team import Team


class StatsWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MLB Stats Application")
        self.setGeometry(100, 100, 600, 400)

        # This will contain the Team object one the .team_info function is called.
        self.user_team = None

        self.team_name = None
        self.id = None
        self.city = None

        # Create a text area to display output

        """
        User input frame. Will contain subframes for all the different menus
        """
        # ************* The Master Widget *************
        self.user_interface = QtWidgets.QWidget()
        self.setCentralWidget(self.user_interface)
        main_box = QtWidgets.QVBoxLayout(self.user_interface)

        # ========== Text Box Widget ==========
        self.output_text_area = QtWidgets.QTextEdit(self)
        self.output_text_area.setReadOnly(True)  # Makes it read-only
        main_box.addWidget(self.output_text_area)

        # ========== Team Selection Widget ==========
        team_selection = QtWidgets.QHBoxLayout()  # Creates the 2nd Horizontal widget container
        self.team_button = QtWidgets.QPushButton("Enter", self)  # Creates the entry button for text input
        self.user_input_box = QtWidgets.QLineEdit(self)  # The actual Text entry box
        self.user_input_box.setPlaceholderText("Enter Team Name: ex... SD, San Diego, Padres (Not Case Sensitive).")

        team_selection.addWidget(self.user_input_box)
        team_selection.addWidget(self.team_button)
        # Add Layout to main box
        main_box.addLayout(team_selection)

        self.team_button.clicked.connect(self.team_info)

        # ========== Buttons/Stats/Options Widget container ==========
        # TODO: Connect button to a function
        input_layout = QtWidgets.QHBoxLayout()
        self.stats_widget = StatsDropDown()
        self.options_widget = TeamInput(name="Options")
        input_layout.addWidget(self.stats_widget)
        input_layout.addWidget(self.options_widget)

        # Add Layout to main box
        main_box.addLayout(input_layout)

        # Hides the UI widgets until a team is chosen.
        self.stats_widget.hide()
        self.options_widget.hide()
        self.user_interface.setLayout(main_box)

    # Function to handle button click
    def team_info(self):
        choice = statsapi.lookup_team(lookup_value=self.user_input_box.text())
        self.output_text_area.clear()
        if len(choice) == 1:
            self.output_text_area.append(f"The {choice[0]['name']} with the ID {choice[0]['id']}.\n")
            self.id = choice[0]['id']
            self.team_name = choice[0]['name']
            self.city = choice[0]['locationName']

            self.user_team = Team(self.team_name, self.id, self.city)

        else:

            # Multiple teams found, ask user to select an ID
            self.output_text_area.append("Teams from that city are:\n")
            for team in choice:
                self.output_text_area.append(f"The {team['name']} with the ID {team['id']}.\n")
            self.output_text_area.append("Please enter the ID of the team you want to select:\n")

        self.enable_buttons()

    def enable_buttons(self):

        self.stats_widget.show()
        self.options_widget.show()


class TeamInput(QtWidgets.QWidget):
    def __init__(self, name="placeholder"):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()

        # Add a label and button
        self.label = QtWidgets.QLabel(f"{name}:")
        self.button = QtWidgets.QPushButton("Click Me - Widget One")
        self.button.clicked.connect(self.button_clicked)

        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def button_clicked(self):
        """ Perform the search based on the button clicked"""
        window.output_text_area.append("Button clicked! Output updated.")


class StatsDropDown(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Dictionary for converting the options to something the API can use.
        self.SELECTION_DICT = {
            "home runs": "homeRuns",
            "batting average": "battingAverage",
            "total bases": "totalBases",
                          }

        layout = QtWidgets.QVBoxLayout()  # Internal layout, keeps things vertical within this space

        # Define the dropdown box options, mostly stats
        self.dropDown = QtWidgets.QComboBox()
        self.dropDown.addItems(["Home Runs", "Batting Average", "Total Bases"])
        layout.addWidget(self.dropDown)

        # TODO:1 Add the stats calls depending on the option selected
        self.entryButton = QtWidgets.QPushButton("Select Stat")
        layout.addWidget(self.entryButton)

        # Set the vertical layout for the widget
        self.setLayout(layout)

        # Connect button to a placeholder function
        self.entryButton.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        # TODO:1
        selection = self.SELECTION_DICT[self.dropDown.currentText().lower()]
        window.output_text_area.append(window.user_team.leader_lookup(limit=10, plot=False, stat=selection))
        pass



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = StatsWindow()
    window.show()
    sys.exit(app.exec_())