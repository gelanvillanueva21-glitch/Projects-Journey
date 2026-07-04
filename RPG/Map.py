
class Map:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def printMap(node, prefix="", isLeft=True):
        if node is None:
            return
        print(prefix + ("├── " if isLeft else "└── ") + node.data)
        printMap(node.left, prefix + ("│   " if isLeft else "    "), True)
        printMap(node.right, prefix + ("│   " if isLeft else "    "), False)