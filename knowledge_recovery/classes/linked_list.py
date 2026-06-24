from __future__ import annotations

class node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class linked_list:
    def __init__(self):
        self.top = None
        self.tail = None

    def append(self, data):
        new_node = node(data)
        if self.top is None:
            self.top = new_node
            self.tail = self.top
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node


def main():
    collection = [1,2,3,4,5,6,7,8,9,10]
    linked_list_obj = linked_list()
    for data in collection:
        linked_list_obj.append(data)
    a= 1

if __name__ == "__main__":
    main()