import kivy
import json
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

kivy.require('1.11.1')  # specify your Kivy version

# Function to load the win data from a JSON file
def load_win_data():
    try:
        with open('wins.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, start with 0 wins for both players
        return {'X': 0, 'O': 0}

# Function to save the win data to a JSON file
def save_win_data(win_data):
    with open('wins.json', 'w') as file:
        json.dump(win_data, file)

class TicTacToeApp(App):
    def build(self):
        self.win_data = load_win_data()  # Load win data from the file
        self.board = [['' for _ in range(3)] for _ in range(3)]  # 3x3 board initialized to empty strings
        self.current_player = 'X'
        
        self.layout = BoxLayout(orientation='vertical')
        
        self.board_layout = GridLayout(cols=3)
        
        for row in range(3):
            for col in range(3):
                button = Button(font_size=40)
                button.row, button.col = row, col  # Assign row and col to each button
                button.bind(on_press=self.on_button_click)
                self.board_layout.add_widget(button)
        
        self.status_label = Label(text="Player X's turn", font_size=30, size_hint=(1, 0.1))
        self.win_label = Label(text=f"X: {self.win_data['X']} O: {self.win_data['O']}", font_size=20, size_hint=(1, 0.1))
        
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.win_label)
        self.layout.add_widget(self.board_layout)
        
        # Add "End Game" and "Restart Game" buttons
        button_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        
        self.end_game_button = Button(text="End Game", font_size=20)
        self.end_game_button.bind(on_press=self.end_game)
        button_layout.add_widget(self.end_game_button)
        
        self.restart_game_button = Button(text="Restart Game", font_size=20)
        self.restart_game_button.bind(on_press=self.restart_game)
        button_layout.add_widget(self.restart_game_button)
        
        self.layout.add_widget(button_layout)
        
        return self.layout

    def on_button_click(self, instance):
        row, col = instance.row, instance.col
        if self.board[row][col] == '':
            self.board[row][col] = self.current_player
            instance.text = self.current_player  # Update button text to the current player symbol
            if self.check_winner():
                self.status_label.text = f"Player {self.current_player} wins!"
                self.win_data[self.current_player] += 1  # Increment the winner's win count
                self.win_label.text = f"X: {self.win_data['X']} O: {self.win_data['O']}"
                save_win_data(self.win_data)  # Save win data to file
                self.end_game()  # End the game after a win
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.status_label.text = f"Player {self.current_player}'s turn"
    
    def check_winner(self):
        # Check rows, columns, and diagonals
        for i in range(3):
            # Check rows
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return True
            # Check columns
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return True
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return True
        
        return False

    def end_game(self, instance=None):
        # Disable all buttons after the game ends
        for button in self.board_layout.children:
            button.disabled = True

    def restart_game(self, instance=None):
        # Reset the board and UI for a new game
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.status_label.text = "Player X's turn"
        self.board_layout.clear_widgets()

        for row in range(3):
            for col in range(3):
                button = Button(font_size=40)
                button.row, button.col = row, col
                button.bind(on_press=self.on_button_click)
                self.board_layout.add_widget(button)
        
        # Re-enable all buttons
        for button in self.board_layout.children:
            button.disabled = False

    def update_board(self):
        # This function can be used to update the board from server-side data or external updates
        pass

if __name__ == '__main__':
    TicTacToeApp().run()
