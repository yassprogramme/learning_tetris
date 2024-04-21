import tkinter as tk
import tetris
import game_simulation
import numpy as np


colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]


def draw_game(canvas, game):
    canvas.delete("all")
    for i in range(game.height):
        for j in range(game.width):
            color_index = game.field[i][j]
            color = "#%02x%02x%02x" % colors[color_index]
            canvas.create_rectangle(j * game.zoom, i * game.zoom,
                                    (j + 1) * game.zoom, (i + 1) * game.zoom,
                                    fill=color)
    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    color_index = np.random.randint(0, len(colors))
                    color = "#%02x%02x%02x" % colors[color_index]
                    canvas.create_rectangle((j + game.figure.x) * game.zoom,
                                            (i + game.figure.y) * game.zoom,
                                            (j + game.figure.x + 1) * game.zoom,
                                            (i + game.figure.y + 1) * game.zoom,
                                            fill=color)
                    


def simulate_game(canvas, game, W):
    if game.state != "gameover":
        type = np.random.randint(0,6)
        game.new_figure(type)
        col, rot = game_simulation.evaluate_best_move(W, game.field, type)
        game.rotate(rot)
        game.go_side(col)
        game.go_space()
        draw_game(canvas, game)
        canvas.after(20, lambda: simulate_game(canvas, game, W))

# Create the Tkinter window
window = tk.Tk()
window.title("Tetris Simulation")

# Create a canvas for drawing the Tetris game
canvas_width = 200  # Adjust as needed
canvas_height = 400  # Adjust as needed
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Create a Tetris game instance
game = tetris.Tetris(20, 10)
W = np.ones(21)

# Run the game simulation and update the canvas
simulate_game(canvas, game, W)

# Start the Tkinter event loop
window.mainloop()