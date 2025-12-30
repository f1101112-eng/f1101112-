import tkinter as tk
import random

# ===== 基本設定 =====
CELL_SIZE = 20
WIDTH = 30
HEIGHT = 20
SPEED = 120

BG_COLOR = "#1e1e2e"
SNAKE_COLOR = "#4ade80"
HEAD_COLOR = "#22c55e"
FOOD_COLOR = "#f87171"

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("精緻版貪食蛇")

        self.canvas = tk.Canvas(
            root,
            width=WIDTH * CELL_SIZE,
            height=HEIGHT * CELL_SIZE,
            bg=BG_COLOR,
            highlightthickness=0
        )
        self.canvas.pack()

        self.score = 0
        self.direction = "Right"
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.food = self.create_food()

        self.root.bind("<Key>", self.change_direction)
        self.update()

    def create_food(self):
        while True:
            pos = (random.randint(0, WIDTH - 1),
                   random.randint(0, HEIGHT - 1))
            if pos not in self.snake:
                return pos

    def draw_round_cell(self, x, y, color):
        px = x * CELL_SIZE
        py = y * CELL_SIZE
        r = 6
        self.canvas.create_oval(
            px + r, py + r,
            px + CELL_SIZE - r, py + CELL_SIZE - r,
            fill=color,
            outline=""
        )

    def draw(self):
        self.canvas.delete("all")

        # 食物
        self.draw_round_cell(self.food[0], self.food[1], FOOD_COLOR)

        # 蛇
        for i, (x, y) in enumerate(self.snake):
            color = HEAD_COLOR if i == 0 else SNAKE_COLOR
            self.draw_round_cell(x, y, color)

        # 分數
        self.canvas.create_text(
            60, 10,
            text=f"Score: {self.score}",
            fill="white",
            font=("Consolas", 12),
            anchor="nw"
        )

    def change_direction(self, event):
        key = event.keysym
        opposites = {
            "Up": "Down", "Down": "Up",
            "Left": "Right", "Right": "Left"
        }
        if key in opposites and opposites[key] != self.direction:
            self.direction = key

    def move_snake(self):
        x, y = self.snake[0]

        if self.direction == "Up":
            y -= 1
        elif self.direction == "Down":
            y += 1
        elif self.direction == "Left":
            x -= 1
        elif self.direction == "Right":
            x += 1

        new_head = (x, y)

        # 撞牆或自己
        if (x < 0 or x >= WIDTH or
            y < 0 or y >= HEIGHT or
            new_head in self.snake):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.create_food()
        else:
            self.snake.pop()

    def game_over(self):
        self.canvas.create_text(
            WIDTH * CELL_SIZE // 2,
            HEIGHT * CELL_SIZE // 2,
            text="GAME OVER",
            fill="white",
            font=("Consolas", 32)
        )

    def update(self):
        self.move_snake()
        self.draw()
        self.root.after(SPEED, self.update)

# ===== 主程式 =====
root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
