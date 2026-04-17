import random
import tkinter as tk

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 30
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
UPDATE_DELAY = 120  # milliseconds between frames

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
        self.canvas.pack()

        self.score = 0
        self.small_eggs_eaten = 0
        self.grow_amount = 0
        self.direction = "Right"
        self.game_over = False

        self.snake = [(GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
                      (GRID_WIDTH // 2, GRID_HEIGHT // 2),
                      (GRID_WIDTH // 2 + 1, GRID_HEIGHT // 2)]
        self.place_egg()

        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))
        self.root.bind("<space>", self.restart)

        self.draw_text("Press arrow keys to start. Space to restart.")
        self.root.after(UPDATE_DELAY, self.game_loop)

    def draw_text(self, message):
        self.canvas.delete("message")
        self.canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                                text=message,
                                fill="white",
                                font=("Arial", 18, "bold"),
                                tags="message")

    def change_direction(self, new_direction):
        if self.game_over:
            return
        opposite = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if new_direction != opposite.get(self.direction):
            self.direction = new_direction
            self.canvas.delete("message")

    def place_egg(self):
        self.is_big_egg = self.small_eggs_eaten >= 5
        self.egg_position = self.random_empty_position()
        self.canvas.delete("egg")
        if self.is_big_egg:
            self.canvas.create_oval(
                self.egg_position[0] * CELL_SIZE + 2,
                self.egg_position[1] * CELL_SIZE + 2,
                (self.egg_position[0] + 1) * CELL_SIZE - 2,
                (self.egg_position[1] + 1) * CELL_SIZE - 2,
                fill="gold", tags="egg")
            self.canvas.create_oval(
                self.egg_position[0] * CELL_SIZE + 6,
                self.egg_position[1] * CELL_SIZE + 6,
                (self.egg_position[0] + 1) * CELL_SIZE - 6,
                (self.egg_position[1] + 1) * CELL_SIZE - 6,
                fill="orange", tags="egg")
        else:
            self.canvas.create_oval(
                self.egg_position[0] * CELL_SIZE + 4,
                self.egg_position[1] * CELL_SIZE + 4,
                (self.egg_position[0] + 1) * CELL_SIZE - 4,
                (self.egg_position[1] + 1) * CELL_SIZE - 4,
                fill="red", tags="egg")

    def random_empty_position(self):
        while True:
            x = random.randrange(GRID_WIDTH)
            y = random.randrange(GRID_HEIGHT)
            if (x, y) not in self.snake:
                return x, y

    def move_snake(self):
        head_x, head_y = self.snake[-1]
        if self.direction == "Up":
            head_y -= 1
        elif self.direction == "Down":
            head_y += 1
        elif self.direction == "Left":
            head_x -= 1
        elif self.direction == "Right":
            head_x += 1

        head_x %= GRID_WIDTH
        head_y %= GRID_HEIGHT
        new_head = (head_x, head_y)

        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.append(new_head)
        if self.grow_amount > 0:
            self.grow_amount -= 1
        else:
            self.snake.pop(0)

        if new_head == self.egg_position:
            self.consume_egg()

    def consume_egg(self):
        if self.is_big_egg:
            self.score += 5
            self.grow_amount += 2
            self.small_eggs_eaten = 0
        else:
            self.score += 1
            self.grow_amount += 1
            self.small_eggs_eaten += 1
        self.place_egg()

    def draw(self):
        self.canvas.delete("snake")
        for index, segment in enumerate(self.snake):
            x, y = segment
            color = "green" if index < len(self.snake) - 1 else "lime"
            self.canvas.create_rectangle(
                x * CELL_SIZE, y * CELL_SIZE,
                (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                fill=color, outline="black", tags="snake")
        self.canvas.delete("hud")
        self.canvas.create_text(10, 10,
                                text=f"Score: {self.score}",
                                anchor="nw",
                                fill="white",
                                font=("Arial", 12, "bold"),
                                tags="hud")
        if self.is_big_egg:
            self.canvas.create_text(WINDOW_WIDTH - 10, 10,
                                    text="Big egg active!",
                                    anchor="ne",
                                    fill="yellow",
                                    font=("Arial", 12, "bold"),
                                    tags="hud")

    def game_loop(self):
        if not self.game_over and self.direction:
            self.move_snake()
            self.draw()
            if self.game_over:
                self.draw_text(f"Game Over! Score: {self.score}. Press Space to restart.")
        self.root.after(UPDATE_DELAY, self.game_loop)

    def restart(self, event=None):
        self.score = 0
        self.small_eggs_eaten = 0
        self.grow_amount = 0
        self.direction = "Right"
        self.game_over = False
        self.snake = [(GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
                      (GRID_WIDTH // 2, GRID_HEIGHT // 2),
                      (GRID_WIDTH // 2 + 1, GRID_HEIGHT // 2)]
        self.place_egg()
        self.canvas.delete("message")
        self.draw()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
