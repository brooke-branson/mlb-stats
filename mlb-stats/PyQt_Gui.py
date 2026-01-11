import sys
import utilities
import PySide6.QtCore
from PySide6 import QtWidgets, QtCore
import statsapi
from team import Team
from datetime import datetime


class StatsWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_width = 1000
        window_height = 700
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2

        self.setWindowTitle("MLB Stats Application")
        self.setGeometry(x, y, window_width, window_height)

        self.user_team = None
        self.team_name = None
        self.id = None
        self.city = None
        self.current_season = datetime.now().year - 1
        self.dark_mode = False

        """
        User input frame. Will contain subframes for all the different menus
        """
        # ************* The Master Widget *************
        self.user_interface = QtWidgets.QWidget()
        self.setCentralWidget(self.user_interface)
        main_box = QtWidgets.QVBoxLayout(self.user_interface)

        # ========== Text Box Widget ==========
        self.output_text_area = QtWidgets.QTextEdit(self)
        self.output_text_area.setReadOnly(True)
        self.show_welcome_message()
        main_box.addWidget(self.output_text_area)

        # ========== Team Selection Widget ==========
        team_selection = QtWidgets.QHBoxLayout()  # Creates the 2nd Horizontal widget container
        self.team_button = QtWidgets.QPushButton("Enter", self)  # Creates the entry button for text input
        self.user_input_box = QtWidgets.QLineEdit(self)  # The actual Text entry box
        self.user_input_box.setPlaceholderText("Enter Team Name: ex... SD, San Diego, Padres (Not Case Sensitive).")
        
        self.user_input_box.returnPressed.connect(self.team_info)

        team_selection.addWidget(self.user_input_box)
        team_selection.addWidget(self.team_button)
        main_box.addLayout(team_selection)

        self.team_button.clicked.connect(self.team_info)
        
        # ========== Season Selection Widget ==========
        season_layout = QtWidgets.QHBoxLayout()
        season_label = QtWidgets.QLabel("Season:")
        self.season_spinbox = QtWidgets.QSpinBox()
        self.season_spinbox.setMinimum(1900)
        self.season_spinbox.setMaximum(2100)
        self.season_spinbox.setValue(self.current_season)
        self.season_spinbox.valueChanged.connect(self.update_season)
        season_layout.addWidget(season_label)
        season_layout.addWidget(self.season_spinbox)
        season_layout.addStretch()
        main_box.addLayout(season_layout)



        # ========== Buttons/Stats/Options Widget container ==========
        input_layout = QtWidgets.QHBoxLayout()
        self.stats_widget = StatsDropDown()
        
        limit_layout = QtWidgets.QVBoxLayout()
        limit_label = QtWidgets.QLabel("Leaders:")
        self.limit_spinbox = QtWidgets.QSpinBox()
        self.limit_spinbox.setMinimum(1)
        self.limit_spinbox.setMaximum(50)
        self.limit_spinbox.setValue(10)
        limit_layout.addWidget(limit_label)
        limit_layout.addWidget(self.limit_spinbox)
        limit_widget = QtWidgets.QWidget()
        limit_widget.setLayout(limit_layout)
        
        self.options_widget = Options(name="Clear")
        self.help_button = Options(name="Help")
        self.change_team_button = Options(name="Change Team")
        self.theme_button = Options(name="🌙 Dark Mode")

        input_layout.addWidget(self.stats_widget)
        input_layout.addWidget(limit_widget)
        input_layout.addWidget(self.options_widget)
        input_layout.addWidget(self.help_button)
        input_layout.addWidget(self.change_team_button)
        input_layout.addWidget(self.theme_button)


        main_box.addLayout(input_layout)

        self.stats_widget.hide()
        self.options_widget.hide()
        self.help_button.hide()
        self.change_team_button.hide()
        limit_widget.hide()
        self.limit_widget = limit_widget
        
        # Theme button is always visible
        self.apply_theme()

        self.user_interface.setLayout(main_box)
        
        self.statusBar = self.statusBar()
        self.statusBar.showMessage("Ready - Enter a team name to begin")

        self.stats_widget.stat_selected.connect(self.handle_stat_selection)
        self.options_widget.button_clicked_signal.connect(self.handle_clear)
        self.help_button.button_clicked_signal.connect(self.handle_help)
        self.change_team_button.button_clicked_signal.connect(self.handle_change_team)
        self.theme_button.button_clicked_signal.connect(self.toggle_theme)

    def update_season(self, year):
        """Update the current season"""
        self.current_season = year
        if self.user_team:
            self.statusBar.showMessage(f"{self.team_name} - Season {self.current_season}")

    def team_info(self):
        """Look up team information with error handling"""
        try:
            team_input = self.user_input_box.text().strip()
            if not team_input:
                self.output_text_area.append("Please enter a team name.\n")
                return
                
            choice = statsapi.lookup_team(lookup_value=team_input)
            self.output_text_area.clear()
            
            if not choice:
                self.output_text_area.append(f"No teams found for '{team_input}'. Please try again.\n")
                return
                
            if len(choice) == 1:
                self.id = choice[0]['id']
                self.team_name = choice[0]['name']
                self.city = choice[0]['locationName']
                self.user_team = Team(self.team_name, self.id, self.city)
                self.output_text_area.append(f"Selected: {self.team_name} ({self.city})\n")
                self.statusBar.showMessage(f"{self.team_name} - Season {self.current_season}")
                self.enable_buttons()
            else:
                self.show_team_selection_dialog(choice)
        except Exception as e:
            self.output_text_area.append(f"Error: {str(e)}\n")
            self.statusBar.showMessage("Error occurred")

    def show_team_selection_dialog(self, teams):
        """Show a dialog to select from multiple teams"""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Select Team")
        dialog.setModal(True)
        layout = QtWidgets.QVBoxLayout()
        
        label = QtWidgets.QLabel("Multiple teams found. Please select one:")
        layout.addWidget(label)
        
        list_widget = QtWidgets.QListWidget()
        for team in teams:
            item_text = f"{team['name']} ({team['locationName']})"
            list_widget.addItem(item_text)
        list_widget.setCurrentRow(0)
        layout.addWidget(list_widget)
        
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            selected_index = list_widget.currentRow()
            if selected_index >= 0:
                selected_team = teams[selected_index]
                self.id = selected_team['id']
                self.team_name = selected_team['name']
                self.city = selected_team['locationName']
                self.user_team = Team(self.team_name, self.id, self.city)
                self.output_text_area.append(f"Selected: {self.team_name} ({self.city})\n")
                self.statusBar.showMessage(f"{self.team_name} - Season {self.current_season}")
                self.enable_buttons()

    def handle_stat_selection(self, stat):
        """Handle stat selection with error handling and table formatting"""
        if not self.user_team:
            self.output_text_area.append("Please select a team first.\n")
            return
            
        try:
            limit = self.limit_spinbox.value()
            result = self.user_team.leader_lookup(limit=limit, plot=False, stat=stat, df_return=True, season=self.current_season)
            
            self.output_text_area.append(f"\n{'='*60}\n")
            self.output_text_area.append(f"Top {limit} Leaders - {stat}\n")
            self.output_text_area.append(f"{'='*60}\n")
            
            table_text = f"{'Rank':<8}{'Name':<30}{'Value':<15}\n"
            table_text += "-" * 60 + "\n"
            for _, row in result.iterrows():
                table_text += f"{str(row['Rank']):<8}{str(row['Name']):<30}{str(row['Value']):<15}\n"
            
            self.output_text_area.append(table_text)
            self.output_text_area.append(f"{'='*60}\n\n")
            
        except Exception as e:
            self.output_text_area.append(f"Error retrieving stats: {str(e)}\n")
            self.statusBar.showMessage("Error retrieving stats")

    def handle_help(self):
        """Display help information about available stats"""
        try:
            self.output_text_area.append("\n" + "="*60 + "\n")
            self.output_text_area.append("Available Leader Types:\n")
            self.output_text_area.append("="*60 + "\n")
            meta_types = statsapi.meta(type="leagueLeaderTypes")
            for i in meta_types:
                self.output_text_area.append(f"  • {i['displayName']}\n")
            self.output_text_area.append("\n" + "="*60 + "\n\n")
        except Exception as e:
            self.output_text_area.append(f"Error loading help: {str(e)}\n")
    
    def show_welcome_message(self):
        """Display welcome message in the text area"""
        text_color = "#ccc" if self.dark_mode else "#666"
        sub_color = "#999" if self.dark_mode else "#999"
        welcome_text = f"""
        <div style='text-align: center; padding-top: 200px; font-size: 24px; color: {text_color};'>
            <b>Welcome to MLB Stats!</b>
            <br><br>
            <span style='font-size: 18px;'>Enter a team name below to get started</span>
            <br>
            <span style='font-size: 14px; color: {sub_color};'>Examples: SD, San Diego, Padres</span>
        </div>
        """
        self.output_text_area.setHtml(welcome_text)
    
    def toggle_theme(self):
        """Toggle between dark and light mode"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        # Update welcome message if it's showing
        if not self.user_team:
            self.show_welcome_message()
    
    def apply_theme(self):
        """Apply the current theme (dark or light)"""
        if self.dark_mode:
            # Dark theme stylesheet
            dark_stylesheet = """
            QMainWindow {
                background-color: #2b2b2b;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #444;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555;
                padding: 5px;
            }
            QPushButton {
                background-color: #404040;
                color: #ffffff;
                border: 1px solid #555;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #303030;
            }
            QComboBox {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555;
                padding: 5px;
            }
            QComboBox:hover {
                background-color: #454545;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #3c3c3c;
                color: #ffffff;
                selection-background-color: #505050;
            }
            QSpinBox {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555;
                padding: 5px;
            }
            QLabel {
                color: #ffffff;
            }
            QStatusBar {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            """
            self.setStyleSheet(dark_stylesheet)
            self.theme_button.button.setText("☀️ Light Mode")
        else:
            # Light theme stylesheet
            light_stylesheet = """
            QMainWindow {
                background-color: #f5f5f5;
            }
            QWidget {
                background-color: #f5f5f5;
                color: #000000;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #ccc;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #ccc;
                padding: 5px;
            }
            QPushButton {
                background-color: #e0e0e0;
                color: #000000;
                border: 1px solid #ccc;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
            QComboBox {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #ccc;
                padding: 5px;
            }
            QComboBox:hover {
                background-color: #f0f0f0;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #000000;
                selection-background-color: #e0e0e0;
            }
            QSpinBox {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #ccc;
                padding: 5px;
            }
            QLabel {
                color: #000000;
            }
            QStatusBar {
                background-color: #f5f5f5;
                color: #000000;
            }
            """
            self.setStyleSheet(light_stylesheet)
            self.theme_button.button.setText("🌙 Dark Mode")
    
    def handle_change_team(self):
        """Reset to allow changing teams"""
        self.user_input_box.clear()
        self.user_input_box.setFocus()
        self.show_welcome_message()
        self.statusBar.showMessage("Ready - Enter a team name to begin")

    def handle_clear(self):
        self.output_text_area.clear()

    def enable_buttons(self):
        """Show all UI elements after team is selected"""
        self.stats_widget.show()
        self.options_widget.show()
        self.help_button.show()
        self.change_team_button.show()
        self.limit_widget.show()


class Options(QtWidgets.QWidget):
    button_clicked_signal = PySide6.QtCore.Signal(str)

    def __init__(self, name="placeholder"):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()

        self.name = name
        self.label = QtWidgets.QLabel(f"{self.name}:")
        self.button = QtWidgets.QPushButton(self.name)
        self.button.clicked.connect(self.button_clicked)

        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def button_clicked(self):
        """ Perform the search based on the button clicked"""

        self.button_clicked_signal.emit(self.name)


class StatsDropDown(QtWidgets.QWidget):
    stat_selected = PySide6.QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.options = utilities.SELECTION_DICT

        layout = QtWidgets.QVBoxLayout()

        self.dropDown = QtWidgets.QComboBox()
        self.all_stats = utilities.FORMATTED_STATS.copy()
        self.dropDown.addItems(self.all_stats)
        self.dropDown.setEditable(True)
        self.dropDown.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        completer = QtWidgets.QCompleter(self.all_stats)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchContains)
        self.dropDown.setCompleter(completer)
        self.dropDown.lineEdit().setPlaceholderText("Select or type to search...")
        layout.addWidget(self.dropDown)

        self.entryButton = QtWidgets.QPushButton("Select Stat")
        layout.addWidget(self.entryButton)

        self.setLayout(layout)

        self.entryButton.clicked.connect(self.on_button_clicked)
        self.dropDown.lineEdit().returnPressed.connect(self.on_button_clicked)

    def on_button_clicked(self):
        """
        Takes the selected option from the stats menu, converts that to a usable string for the mlb stats api,
        then prints that message to the apps window text area.
        :return:
        """
        selected_text = self.dropDown.currentText().strip().lower()
        if not selected_text:
            return
        
        try:
            selection = self.options[selected_text]
            self.stat_selected.emit(selection)
        except KeyError:
            for key in self.options.keys():
                if selected_text in key or key in selected_text:
                    self.stat_selected.emit(self.options[key])
                    return



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = StatsWindow()
    window.show()
    sys.exit(app.exec())