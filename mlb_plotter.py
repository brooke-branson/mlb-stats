import tkinter as tk
import statsapi
from team import Team


# Stats window for UI Prototype
class StatsWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Player Stats")

        self.SELECTION_DICT = {
            "home runs": "homeRuns",
            "batting average": "battingAverage",
            "total bases": "totalBases",
                          }

        # This will contain the Team object one the .team_info function is called.
        self.user_team = None

        self.team_name = None
        self.id = None
        self.city = None

        # Create a text area to display output
        self.text_area = tk.Text(self.window)
        self.text_area.pack(expand=True, fill="both")

        # Add an entry field for team input
        self.team_label = tk.Label(self.window, text="Enter Team Name:")
        self.team_label.pack(pady=5)

        self.team_entry = tk.Entry(self.window)
        self.team_entry.pack(pady=5)

        # Add an "Enter" button for the team name input
        self.enter_team_button = tk.Button(self.window, text="Enter", command=self.team_info)
        self.enter_team_button.pack(pady=5)

        # Entry field and button for team ID
        self.team_id_entry = tk.Entry(self.window)
        self.team_id_button = tk.Button(self.window, text="Submit ID", command=self.process_team_id)

        # Create buttons for user actions
        self.hr_button = tk.Button(self.window, text="HR Leader Stats", command=self.show_hr_leader_stats)
        self.batting_avg_button = tk.Button(self.window, text="Batting Average", command=self.show_batting_average)

        self.selected_option = tk.StringVar(self.window)

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

        self.selected_option.set("Home Runs")  # Default value

        # Create OptionMenu
        options = ["Home Runs", "Batting Average", "Total Bases"]
        dropdown = tk.OptionMenu(self.window, self.selected_option, *options)
        dropdown.pack(side="left", pady=10)

        self.selected_option.trace("w", self.on_select)
        # self.hr_button.pack(side="left", padx=10, pady=5)
        # self.batting_avg_button.pack(side="left", padx=10, pady=5)

    def on_select(self, *args):
        """
        Runs the correct function for the selection in the drop down menu.

        """
        self.display_text(f"{self.selected_option.get()} Leaders:")
        selection = self.selected_option.get().lower()
        self.display_text(self.user_team.leader_lookup(limit=10, plot=False, stat=self.SELECTION_DICT[f"{selection}"]))




    def display_text(self, text):
        self.text_area.insert(tk.END, text + "\n")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    stats_window = StatsWindow()
    stats_window.run()


