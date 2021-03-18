class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def printTreeLeftRight(node):
    if node.left == None and node.left == None:
        print(node.data, end=" ")
    else:
        printTreeLeftRight(node.left)
        print(node.data, end=" ")
        printTreeLeftRight(node.right)


if __name__ == "__main__":
    root = Node(12)
    root.left = Node(10)
    root.right = Node(20)
    root.right.left = Node(25)
    root.right.right = Node(40)

    printTreeLeftRight(root)