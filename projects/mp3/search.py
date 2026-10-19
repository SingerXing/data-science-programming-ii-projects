class Node:
    def __init__(self, key):
        self.key = key
        self.values = []
        self.left = None
        self.right = None

    def __len__(self):
        # TODO: implement recursive size calculation
        size = len(self.values)
        if self.left != None:
            size += len(self.left)
        if self.right != None:
            size += len(self.right)
        return size

    def lookup(self, key):
        # TODO: implement recursive search
        if self.key == key:
            return self.values
        if self.left != None:
            if self.key > key:
                return self.left.lookup(key)
        if self.right != None:
            if self.key < key:
                return self.right.lookup(key)
        return []


class BST:
    def __init__(self):
        self.root = None

    def add(self, key, val):
        # TODO: implement iterative insert
        if self.root == None:
            self.root = Node(key)
        curr = self.root
        while True:
            if key < curr.key:
                if curr.left == None:
                    curr.left = Node(key)
                curr = curr.left
            elif key > curr.key:
                if curr.right == None:
                    curr.right = Node(key)
                curr = curr.right
            else:
                assert curr.key == key
                break
        curr.values.append(val)

    def __dump(self, node):
        if node == None:
            return
        self.__dump(node.left)            # 1
        print(node.key, ":", node.values)  # 2
        self.__dump(node.right)             # 3


    def dump(self):
        # TODO: call __dump on the root
        self.__dump(self.root)

    def __getitem__(self, key):
        # TODO: return values for key
        if self.root is None:
            return []
        return self.root.lookup(key)
    
    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))
    
    def leaf_count(self):
        return self._leaf_count(self.root)
    def _leaf_count(self, node):
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return 1
        return self._leaf_count(node.left) + self._leaf_count(node.right)

    def top_n(self, n):
        result = []

        def helper(node):
            if node is None or len(result) >= n:
                return

            helper(node.right)

            if len(result) < n:
                result.append(node.key)

            helper(node.left)

        helper(self.root)
        return result
