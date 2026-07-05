from mods.linked_list import LinkedList


RED = "red"
BLACK = "black"


class RBNode:
    def __init__(self, key=None, record=None):
        self.key = key
        self.records = LinkedList()

        if record is not None:
            self.records.append(record)

        self.parent = None
        self.left = None
        self.right = None
        self.color = RED


class RedBlackTree:
    def __init__(self):
        self.nil = RBNode()
        self.nil.color = BLACK

        self.root = self.nil
        self.size = 0

    def search(self, key):
        current = self.root
        steps = 0

        while current != self.nil:
            steps += 1

            if key == current.key:
                return current.records, steps

            if key < current.key:
                current = current.left
            else:
                current = current.right

        return LinkedList(), steps

    def insert(self, key, record):
        node = self._find_node(key)

        if node != self.nil:
            node.records.append(record)
            return

        new_node = RBNode(key, record)
        new_node.left = self.nil
        new_node.right = self.nil
        new_node.color = RED

        parent = None
        current = self.root

        while current != self.nil:
            parent = current

            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self.size += 1

        if new_node.parent is None:
            new_node.color = BLACK
            return

        if new_node.parent.parent is None:
            return

        self._fix_insert(new_node)

    def delete_record(self, key, record):
        node = self._find_node(key)

        if node == self.nil:
            return False

        deleted = node.records.remove_by_reference(record)

        if not deleted:
            return False

        if node.records.is_empty():
            self._delete_node(node)

        return True

    def _find_node(self, key):
        current = self.root

        while current != self.nil:
            if key == current.key:
                return current

            if key < current.key:
                current = current.left
            else:
                current = current.right

        return self.nil

    def _fix_insert(self, node):
        while node.parent is not None and node.parent.color == RED:
            if node.parent == node.parent.parent.right:
                uncle = node.parent.parent.left

                if uncle.color == RED:
                    uncle.color = BLACK
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)

                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self._left_rotate(node.parent.parent)

            else:
                uncle = node.parent.parent.right

                if uncle.color == RED:
                    uncle.color = BLACK
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)

                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self._right_rotate(node.parent.parent)

            if node == self.root:
                break

        self.root.color = BLACK

    def _delete_node(self, node):
        original_color = node.color

        if node.left == self.nil:
            x = node.right
            self._transplant(node, node.right)

        elif node.right == self.nil:
            x = node.left
            self._transplant(node, node.left)

        else:
            replacement = self._maximum(node.left)

            original_color = replacement.color
            x = replacement.left

            if replacement.parent == node:
                x.parent = replacement
            else:
                self._transplant(replacement, replacement.left)
                replacement.left = node.left
                replacement.left.parent = replacement

            self._transplant(node, replacement)

            replacement.right = node.right
            replacement.right.parent = replacement
            replacement.color = node.color

        if original_color == BLACK:
            self._fix_delete(x)

        self.size -= 1

    def _fix_delete(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                sibling = x.parent.right

                if sibling.color == RED:
                    sibling.color = BLACK
                    x.parent.color = RED
                    self._left_rotate(x.parent)
                    sibling = x.parent.right

                if sibling.left.color == BLACK and sibling.right.color == BLACK:
                    sibling.color = RED
                    x = x.parent
                else:
                    if sibling.right.color == BLACK:
                        sibling.left.color = BLACK
                        sibling.color = RED
                        self._right_rotate(sibling)
                        sibling = x.parent.right

                    sibling.color = x.parent.color
                    x.parent.color = BLACK
                    sibling.right.color = BLACK
                    self._left_rotate(x.parent)
                    x = self.root

            else:
                sibling = x.parent.left

                if sibling.color == RED:
                    sibling.color = BLACK
                    x.parent.color = RED
                    self._right_rotate(x.parent)
                    sibling = x.parent.left

                if sibling.right.color == BLACK and sibling.left.color == BLACK:
                    sibling.color = RED
                    x = x.parent
                else:
                    if sibling.left.color == BLACK:
                        sibling.right.color = BLACK
                        sibling.color = RED
                        self._left_rotate(sibling)
                        sibling = x.parent.left

                    sibling.color = x.parent.color
                    x.parent.color = BLACK
                    sibling.left.color = BLACK
                    self._right_rotate(x.parent)
                    x = self.root

        x.color = BLACK

    def _transplant(self, old_node, new_node):
        if old_node.parent is None:
            self.root = new_node
        elif old_node == old_node.parent.left:
            old_node.parent.left = new_node
        else:
            old_node.parent.right = new_node

        new_node.parent = old_node.parent

    def _maximum(self, node):
        while node.right != self.nil:
            node = node.right

        return node

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left

        if y.left != self.nil:
            y.left.parent = x

        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right

        if y.right != self.nil:
            y.right.parent = x

        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def clear(self):
        self.root = self.nil
        self.size = 0

    def debug_print(self, index_lookup=None):
        result = []
        self._debug_print_helper(self.root, "", True, result, index_lookup)
        return "\n".join(result)

    def _debug_print_helper(self, node, indent, last, result, index_lookup):
        if node == self.nil:
            return

        prefix = "R---- " if last else "L---- "
        color = "BLACK" if node.color == BLACK else "RED"

        indexes_text = ""
        if index_lookup is not None:
            indexes = [
                str(index_lookup[id(record)])
                for record in node.records
                if id(record) in index_lookup
            ]
            if indexes:
                indexes_text = f", номера в массиве: {', '.join(indexes)}"

        result.append(
            f"{indent}{prefix}{node.key} ({color}) [записей: {len(node.records)}{indexes_text}]"
        )

        new_indent = indent + ("     " if last else "|    ")

        self._debug_print_helper(node.left, new_indent, False, result, index_lookup)
        self._debug_print_helper(node.right, new_indent, True, result, index_lookup)