class ArrayStorage:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)
        return item

    def remove(self, item):
        for i in range(len(self.items)):
            if self.items[i] is item:
                last_index = len(self.items) - 1
                self.items[i] = self.items[last_index]
                self.items.pop()
                return True

        return False

    def get_active_items(self):
        return list(self.items)

    def clear(self):
        self.items.clear()