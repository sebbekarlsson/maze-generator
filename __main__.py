from maze_generator import Canvas


if __name__ == '__main__':
    canvas = Canvas()
    canvas.render()
    canvas.image.save('maze.png')
    canvas.show()
