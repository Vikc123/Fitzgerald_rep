class ArrayStorage:
    def __init__(self):
        self.items = []

    def add(self, item):
        for i in range(len(self.items)):
            if self.items[i] is None:
                self.items[i] = item
                return item

        self.items.append(item)
        return item

    def remove(self, item):
        for i in range(len(self.items)):
            if self.items[i] is item:
                self.items[i] = None
                return True

        return False

    def get_active_items(self):
        return [item for item in self.items if item is not None]

    def clear(self):
        self.items.clear()