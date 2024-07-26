import tkinter as tk
import random
from tkinter import messagebox

class WumpusWorld:
    def __init__(self, master, size=4):
        self.master = master
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.agent_location = (0, 0)
        self.wumpus_location = self.generate_random_location(exclude=[self.agent_location, (0,1), (1,0)])
        self.gold_location = self.generate_random_location(exclude=[self.agent_location, self.wumpus_location])
        self.pit_locations = [self.generate_random_location(exclude=[self.agent_location, self.wumpus_location, self.gold_location, (0,1), (1,0)]) for _ in range(3)]
        self.percept = ''
        self.game_over = False
        self.create_widgets()
        self.bind_keys()
        self.show_instructions()

    def generate_random_location(self, exclude=[]):
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if (x, y) not in exclude:
                return (x, y)

    def get_adjacent_locations(self, location):
        x, y = location
        adjacent_locations = []
        if x > 0:
            adjacent_locations.append((x - 1, y))
        if x < self.size - 1:
            adjacent_locations.append((x + 1, y))
        if y > 0:
            adjacent_locations.append((x, y - 1))
        if y < self.size - 1:
            adjacent_locations.append((x, y + 1))
        return adjacent_locations

    def get_percept(self):
        self.percept = ''
        x, y = self.agent_location
        if (x, y) in self.get_adjacent_locations(self.wumpus_location):
            self.percept += 'You smell a wumpus nearby!\n'
        for pit_location in self.pit_locations:
            if (x, y) in self.get_adjacent_locations(pit_location):
                self.percept += 'You feel a breeze!\n'
                break
        for pit_location in self.pit_locations:
            if (0, 0) in self.get_adjacent_locations(pit_location):
                self.percept += 'You feel a breeze near the starting position!\n'
                break
        if (x, y) == self.gold_location:
            self.percept += 'You see a glimmer! Press "g" to grab the gold.\n'

    def move(self, direction):
        x, y = self.agent_location
        if direction == 'up' and x > 0:
            self.agent_location = (x - 1, y)
        elif direction == 'down' and x < self.size - 1:
            self.agent_location = (x + 1, y)
        elif direction == 'left' and y > 0:
            self.agent_location = (x, y - 1)
        elif direction == 'right' and y < self.size - 1:
            self.agent_location = (x, y + 1)
        self.get_percept()
        self.update_grid()
        if self.agent_location in self.pit_locations:
            self.game_over = True
            self.percept = "You fell into a pit! Game Over!"
            self.update_grid()
        if self.agent_location in self.wumpus_location:
            self.percept = "You are with Wumpus! Kill him using the space bar"
            self.update_grid()
        if self.agent_location == (0, 0) and self.gold_location is None:
            self.game_over = True
            self.percept = "You've reached the starting position with the gold. You win! Game Over!"
            self.update_grid()

    def shoot(self, event=None):
        self.percept = ''
        if self.agent_location[0] == self.wumpus_location[0] or self.agent_location[1] == self.wumpus_location[1]:
            self.percept += 'You hear a scream!\n'
            self.wumpus_location = None
        else:
            self.percept += 'You hear nothing but your own echo.\n'
        self.update_grid()

    def grab(self, event=None):
        self.percept = ''
        if self.agent_location == self.gold_location:
            self.percept += 'You grab the gold!\n'
            self.gold_location = None
        else:
            self.percept += 'There is no gold here.\n'
        self.update_grid()

    def bind_keys(self):
        self.master.bind('<Up>', lambda event: self.move('up'))
        self.master.bind('<Down>', lambda event: self.move('down'))
        self.master.bind('<Left>', lambda event: self.move('left'))
        self.master.bind('<Right>', lambda event: self.move('right'))
        self.master.bind('<space>', self.shoot)
        self.master.bind('g', self.grab)

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()
        self.update_grid()

    def show_instructions(self):
        messagebox.showinfo("Instructions", "Welcome to Wumpus World!\n\n"
                            "Instructions:\n"
                            "- Use arrow keys to move the agent.\n"
                            "- Press the space bar to shoot an arrow.\n"
                            "- Press 'g' to grab the gold.\n"
                            "- Avoid pits and the wumpus.\n"
                            "- Find the gold and return to the starting position to win.")

    def update_grid(self):
        self.canvas.delete("all")
        cell_width = 100
        cell_height = 100
        for row in range(self.size):
            for col in range(self.size):
                x0 = col * cell_width
                y0 = row * cell_height
                x1 = x0 + cell_width
                y1 = y0 + cell_height
                if (row, col) == self.agent_location:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
                elif (row, col) == self.wumpus_location:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                elif (row, col) == self.gold_location:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                elif (row, col) in self.pit_locations:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
        self.canvas.create_text(200, 20, text=self.percept, font=("Arial", 12))
        if self.game_over:
            self.canvas.create_text(200, 200, text="Game Over!", font=("Arial", 24))
            exit()

def main():
    root = tk.Tk()
    root.title("Wumpus World")
    game = WumpusWorld(root)
    root.mainloop()

if __name__ == "__main__":
    main()