from flask import Flask, render_template, request

from solver import Grid

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        sudoku_dict = {}
        for i in range(81):
            square = request.form[str(i)]
            if square.isalpha():
                # raise error
                pass
            if square == "":
                square = 0
            else:
                square = int(square)
            row, col = i // 9, i % 9
            sudoku_dict[(row, col)] = [square, square != 0]
        sudoku_grid = Grid(sudoku_dict)
        sudoku_grid.solve()
        # run algorithm
        return render_template("index.html")
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run()
