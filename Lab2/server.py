import math
from flask import Flask, request, jsonify, send_file

import helpers as helper   # your game file (helpers.py)

app = Flask(__name__)


def num(x):
    """JSON can't hold infinity, so send it as text."""
    if isinstance(x, float) and math.isinf(x):
        return "inf" if x > 0 else "-inf"
    return x


def print_tree():
    """Full tree to the console (assignment requirement). Root first."""
    K = helper.MAXDEPTH
    lines = []
    for level, col, value, alpha, beta, pruned in reversed(helper.Nodes):
        pad = "    " * level
        if level == 0:
            lines.append(f"ROOT value={value} alpha={alpha} beta={beta}")
        elif level == K:
            lines.append(f"{pad}col {col}  LEAF heuristizc={value}")
        else:
            lines.append(f"{pad}col {col}  value={value} alpha={alpha} beta={beta}")
        if pruned:
            lines.append(f"{pad}    PRUNED x {pruned}")
    return "\n".join(lines)


@app.route("/")
def home():
    return send_file("index.html")


@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    K = int(data["depth"])

    helper.MAXDEPTH = K          # so levels are computed correctly
    helper.Nodes.clear()         # new tree for this turn

    value, col = helper.minMax(data["board"], data["index"],
                               -math.inf, math.inf, K, True, None)

    text = print_tree()
    print("\n===== Minimax tree, K =", K, "=====")
    print(text)
    print("Chosen column:", col, " Nodes:", len(helper.Nodes))
    with open("tree_log.txt", "a") as f:
        f.write(f"\n===== K = {K}, chosen column {col} =====\n{text}\n")

    # every node goes to the page as [level, col, value, alpha, beta, pruned]
    nodes = [[l, c, num(v), num(a), num(b), p] for l, c, v, a, b, p in helper.Nodes]
    return jsonify({"col": col, "value": num(value), "K": K, "nodes": nodes})


if __name__ == "__main__":
    app.run(debug=True)
