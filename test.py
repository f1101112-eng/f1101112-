import tkinter as tk
import random

# 視窗與畫布設定
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
CELL_SIZE = 20

# 方向
UP = "Up"
DOWN = "Down"
LEFT = "Left"
RIGHT = "Right"

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("貪食蛇 Snake Game")

        self.canvas = tk.Canvas(
            root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg="black"
        )
        self.canvas.pack()

        # 初始化
        self.direction = RIGHT
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = None
        self.running = True

        # 鍵盤事件
        self.root.bind("<Key>", self.change_direction)

        self.create_food()
        self.game_loop()

    def create_food(self):
        while True:
            x = random.randrange(0, WINDOW_WIDTH, CELL_SIZE)
            y = random.randrange(0, WINDOW_HEIGHT, CELL_SIZE)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def change_direction(self, event):
        key = event.keysym
        if key == UP and self.direction != DOWN:
            self.direction = UP
        elif key == DOWN and self.direction != UP:
            self.direction = DOWN
        elif key == LEFT and self.direction != RIGHT:
            self.direction = LEFT
        elif key == RIGHT and self.direction != LEFT:
            self.direction = RIGHT

    def move_snake(self):
        head_x, head_y = self.snake[0]

        if self.direction == UP:
            head_y -= CELL_SIZE
        elif self.direction == DOWN:
            head_y += CELL_SIZE
        elif self.direction == LEFT:
            head_x -= CELL_SIZE
        elif self.direction == RIGHT:
            head_x += CELL_SIZE

        new_head = (head_x, head_y)

        # 撞牆或撞到自己
        if (
            head_x < 0 or head_x >= WINDOW_WIDTH or
            head_y < 0 or head_y >= WINDOW_HEIGHT or
            new_head in self.snake
        ):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        # 吃到食物
        if new_head == self.food:
            self.create_food()
        else:
            self.snake.pop()

    def draw(self):
        self.canvas.delete("all")

        # 畫蛇
        for x, y in self.snake:
            self.canvas.create_rectangle(
                x, y,
                x + CELL_SIZE, y + CELL_SIZE,
                fill="green"
            )

        # 畫食物
        fx, fy = self.food
        self.canvas.create_oval(
            fx, fy,
            fx + CELL_SIZE, fy + CELL_SIZE,
            fill="red"
        )

    def game_loop(self):
        if self.running:
            self.move_snake()
            self.draw()
            self.root.after(150, self.game_loop)

    def game_over(self):
        self.running = False
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            fill="white",
            font=("Arial", 24),
            text="Game Over"
        )

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
