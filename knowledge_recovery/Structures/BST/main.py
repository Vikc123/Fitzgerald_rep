from mods import generator as gt
class Tree:
    def __init__(self):
        self.root = None

    def insert(self, current_root, data):
        if self.root is None:
            self.root = Node(data)
            return
        else:
            if data <= current_root.data:
                if current_root.left is None:
                    current_root.left = Node(data)
                    current_root.left.parent = current_root
                    return
                else:
                    self.insert(current_root.left, data)
            elif data >= current_root.data:
                if current_root.right is None:
                    current_root.right = Node(data)
                    current_root.right.parent = current_root
                else:
                    self.insert(current_root.right, data)
                return

    def max(self, current_root):
        if current_root is None:
            return None
        else:
            while(current_root.right is not None):
                current_root = current_root.right
            return current_root

    def find(self, root, data):
        if root is None:
            return None
        else:
            current_root = root
            while(current_root.data != data):
                if data <= current_root.data and current_root.left is not None:
                    current_root = current_root.left
                    continue
                elif data >= current_root.data and current_root.right is not None:
                    current_root = current_root.right
                    continue
                else:
                    return None
            return current_root




    def delete(self, root, data):
        if root is None:
            return None
        else:
            to_del = self.find(self.root, data)
            if to_del is None:
                return None
            else:
                #удаление листа
                if to_del.left is None and to_del.right is None:
                    if to_del is to_del.parent.left:
                        to_del.parent.left = None
                        del to_del
                        return
                    else:
                        to_del.parent.right = None
                        del to_del
                        return
                #удаление узла с одним потомком
                if to_del.right is not None and to_del.left is None: #есть только правый потомок
                    if to_del is to_del.parent.left: #если удаляемый является левым потомком
                        to_del.parent.left = to_del.right
                        to_del.right.parent = to_del.parent
                        del to_del
                        return
                    else:#если удаляемый является правым потомком
                        to_del.parent.right = to_del.right
                        to_del.right.parent = to_del.parent
                        del to_del
                        return
                if to_del.left is not None and to_del.right is None: #есть только левый потомок
                    if to_del is to_del.parent.right:#если удаляемый является правым потомком
                        to_del.parent.right = to_del.left
                        to_del.left.parent = to_del.parent
                        return
                    else:#если удаляемый является левым потомком
                        to_del.parent.left = to_del.left
                        to_del.left.parent = to_del.parent
                        return
                #удаление узла с двумя потомками
                if to_del.left is not None and to_del.right is not None:
                    if to_del.parent.right is to_del:
                        max = self.max(to_del.left)
                        if max is max.parent.right:
                            max.parent.right = None
                            max.parent = to_del.parent
                        elif max is max.parent.left:
                            max.parent.left = max.left
                            max.parent = to_del.parent
                        max.left = to_del.left
                        max.right = to_del.right
                        max.left.parent = max
                        max.right.parent = max
                        to_del.parent.right = max
                        del to_del
                        return
                    else:
                        max = self.max(to_del.left)
                        if max is max.parent.right:
                            max.parent.right = None
                            max.parent = to_del.parent
                        elif max is max.parent.left:
                            max.parent.left = None
                            max.parent = to_del.parent
                        max.left = to_del.left
                        max.right = to_del.right
                        max.left.parent = max
                        max.right.parent = max
                        to_del.parent.right = max
                        del to_del
                        return


class Node():
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.parent = None

def main():
    # gt.generate_file('data/bst.txt', 10)
    t = Tree()
    collection = [20, 30, 10, 15, 5, 25, 23,26,27, 35]
    for i in collection:
        t.insert(t.root, i)
    t.delete(t.root, 5)
    t.delete(t.root, 10)
    t.delete(t.root, 30)
    a = 5

if __name__ == '__main__':
    main()