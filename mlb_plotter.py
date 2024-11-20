import tkinter as tk
import statsapi
from team import Team


# Stats window for UI Prototype
class StatsWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Player Stats")

        # Dictionary for converting the options to something the API can use.
        self.SELECTION_DICT = {
            "home runs": "homeRuns",
            "batting average": "battingAverage",
            "total bases": "totalBases",
                          }
        
        # Options for the Drop-Down Menu.
        self.options = ["Home Runs", "Batting Average", "Total Bases"]


        # This will contain the Team object one the .team_info function is called.
        self.user_team = None

        self.team_name = None
        self.id = None
        self.city = None

        # Create a text area to display output
        self.text_area = tk.Text(self.window)
        self.text_area.pack(expand=True, fill="both")

        """

        User input frame. Will contain subframes for all the different menus

        """
        # ************* The Master Frame *************
        self.user_interface = tk.Frame(self.window)
        self.user_interface.pack(pady=5)

        # ============= Team Choice Frame =============
        self.team_frame = tk.Frame(self.user_interface)
        self.team_frame.pack(padx=5)

        # Add an entry field for team input
        self.team_label = tk.Label(self.team_frame, text="Enter Team Name:")
        self.team_label.pack(pady=5)
        self.team_entry = tk.Entry(self.team_frame)
        self.team_entry.pack(pady=5)

        # Add an "Enter" button for the team name input
        self.enter_team_button = tk.Button(self.team_frame, text="Enter", command=self.team_info)
        self.enter_team_button.pack(pady=5)

        # Entry field and button for team ID
        self.team_id_entry = tk.Entry(self.team_frame)
        self.team_id_button = tk.Button(self.team_frame, text="Submit ID", command=self.process_team_id)

        # ============= Creates the Frame to hold the Stats options =============
        self.stats_frame = tk.Frame(self.user_interface)
        # Create buttons for user actions
        self.hr_button = tk.Button(self.stats_frame, text="HR Leader Stats", command=self.show_hr_leader_stats)
        self.batting_avg_button = tk.Button(self.stats_frame, text="Batting Average", command=self.show_batting_average)

        # Drop down menu for stat choices
        self.selected_option = tk.StringVar(self.stats_frame)
        self.menu_entry = tk.Button(self.stats_frame, text="Enter", command=self.on_select)
        self.selected_option.set("Home Runs")  # Default value
        self.dropdown = tk.OptionMenu(self.stats_frame, self.selected_option, *self.options)

        self.number_of_leaders = tk.Scale(self.stats_frame, from_=1, to=15, orient="horizontal")

        # ============= Options menu Frame =============
        self.options_frame = tk.Frame(self.user_interface)
        self.help_button = tk.Button(self.options_frame, text="Help", command=self.on_help)


    def team_info(self):
        """
        Creates the Team object to be used by the UI from this point on.
        This function must be run before any other function will operate correctly.
        Queries the stats api to find the teams related to the user input:
            This input can be the full team name, the city, the city initials, or the direct ID if known.
            For example, inputing NY will return two teams, the Mets and the Yankees, and will present their ID.
            From that point, the user is requested to input the ID of the team they want to see.
        """
        # self.team_name = self.team_entry.get()
        choice = statsapi.lookup_team(lookup_value=self.team_entry.get())

        if len(choice) == 1:
            self.display_text(f"The {choice[0]['name']} with the ID {choice[0]['id']}.\n")
            self.id = choice[0]['id']
            self.team_name = choice[0]['name']
            self.city = choice[0]['locationName']

            self.user_team = Team(self.team_name, self.id, self.city)
            self.enable_buttons()

        else:

            # Multiple teams found, ask user to select an ID
            self.display_text("Teams from that city are:\n")
            for team in choice:
                self.display_text(f"The {team['name']} with the ID {team['id']}.\n")
            self.display_text("Please enter the ID of the team you want to select:\n")

            # Show the entry field and button for team ID input in the event of multiple teams in the search.
            self.team_id_entry.pack(pady=5)
            self.team_id_button.pack(pady=5)

    def process_team_id(self):
        """
        This function only gets called if there are multiple teams related to user input.
        Retrieves the selected team ID and finalizes team information.
        """
        # Get the team ID from user input
        selected_id = self.team_id_entry.get()

        # Use the selected ID to look up and set the team information
        choice = statsapi.lookup_team(lookup_value=selected_id)

        if choice:
            self.team_name = choice[0]['name']
            self.id = choice[0]['id']
            self.city = choice[0]['locationName']
            self.user_team = Team(self.team_name, self.id, self.city)

            # Clear and display final selection
            self.text_area.delete("1.0", tk.END)
            self.display_text(f"Team selected: {self.team_name} (ID: {self.id})\n")

        else:
            self.display_text("Invalid team ID. Please try again.\n")

        # Hide the entry field and button for team ID input after processing
        self.team_id_entry.pack_forget()
        self.team_id_button.pack_forget()

        self.enable_buttons()

    def show_hr_leader_stats(self):
        self.display_text(self.user_team.leader_lookup(limit=10, plot=False, stat="homeRuns"))

    def show_batting_average(self):
        self.display_text(self.user_team.leader_lookup(limit=10, plot=False, stat="battingAverage"))

    def enable_buttons(self):
        """
        To be called once the user team Object is instantiated. Will toggle the visibility of the various stat buttons.

        :return: Nothing
        """
        self.stats_frame.pack(side="left")

        # Show Options drop down menu and Entry button.
        self.dropdown.grid(row=0, column=0)
        self.menu_entry.grid(row=0, column=1)

        # Shows the Numerical slider
        self.number_of_leaders.grid(row=1, column=0)

        # Enables Help menu
        self.options_frame.pack(side="right")
        self.help_button.pack()


    def on_select(self, *args):
        """
        Runs the correct function for the selection in the drop down menu.

        """
        self.display_text(f"{self.selected_option.get()} Leaders:")
        selection = self.selected_option.get().lower()
        self.display_text(self.user_team.leader_lookup(limit=self.number_of_leaders.get(), plot=False, stat=self.SELECTION_DICT[f"{selection}"]))

    def on_help(self):
        # TODO Actually set this button to work, currently its just for reference to see meta data
        print(self.user_team.help(type="leagueLeaderTypes"))




    def display_text(self, text):
        self.text_area.insert(tk.END, text + "\n")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    stats_window = StatsWindow()
    stats_window.run()


