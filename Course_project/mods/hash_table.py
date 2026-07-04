from mods.linked_list import LinkedList


class HashSlot:
    def __init__(self):
        self.key = None
        self.records = LinkedList()
        self.status = 0
        # 0 — пусто
        # 1 — занято
        # 2 — удалено


SHRINK_LOAD_FACTOR = 0.25


class HashTable:
    def __init__(self, capacity=17, load_factor=0.7):
        self.capacity = self._next_prime(capacity)
        self.initial_capacity = self.capacity
        self.size = 0
        self.load_factor = load_factor
        self.table = [HashSlot() for _ in range(self.capacity)]

    def _is_prime(self, n):
        if n < 2:
            return False

        if n in (2, 3):
            return True

        if n % 2 == 0:
            return False

        i = 3

        while i * i <= n:
            if n % i == 0:
                return False

            i += 2

        return True

    def _next_prime(self, n):
        candidate = max(n, 2)

        while not self._is_prime(candidate):
            candidate += 1

        return candidate

    def _normalize_key(self, key):
        if isinstance(key, int):
            return key

        return sum(ord(char) * (31 ** i) for i, char in enumerate(str(key)))

    def _middle_square_hash(self, key):
        key = self._normalize_key(key)
        square = key * key
        square_str = str(square)

        if len(square_str) <= 3:
            middle = square
        else:
            mid = len(square_str) // 2
            start = max(0, mid - 1)
            end = min(len(square_str), mid + 2)
            middle = int(square_str[start:end])

        return middle % self.capacity

    def _secondary_hash(self, key):
        key = self._normalize_key(key)
        return 1 + (key % (self.capacity - 1))

    def _probe(self, primary_hash, secondary_hash, i):
        return (primary_hash + i * secondary_hash) % self.capacity

    def _need_grow(self):
        return self.size / self.capacity >= self.load_factor

    def _need_shrink(self):
        if self.capacity <= self.initial_capacity:
            return False

        return self.size / self.capacity <= SHRINK_LOAD_FACTOR

    def _rebuild(self, new_capacity):
        old_table = self.table

        self.capacity = new_capacity
        self.size = 0
        self.table = [HashSlot() for _ in range(self.capacity)]

        for slot in old_table:
            if slot.status == 1:
                for record in slot.records:
                    self.insert(slot.key, record)

    def _resize(self):
        self._rebuild(self._next_prime(self.capacity * 2 + 1))

    def _shrink(self):
        self._rebuild(self._next_prime(max(self.initial_capacity, self.capacity // 2)))

    def insert(self, key, record):
        if self._need_grow():
            self._resize()

        primary_hash = self._middle_square_hash(key)
        secondary_hash = self._secondary_hash(key)
        first_deleted = None

        for i in range(self.capacity):
            index = self._probe(primary_hash, secondary_hash, i)
            slot = self.table[index]

            if slot.status == 1 and slot.key == key:
                slot.records.append(record)
                return True

            if slot.status == 2 and first_deleted is None:
                first_deleted = index

            if slot.status == 0:
                target_index = first_deleted if first_deleted is not None else index

                self.table[target_index].key = key
                self.table[target_index].records = LinkedList()
                self.table[target_index].records.append(record)
                self.table[target_index].status = 1

                self.size += 1
                return True

        if first_deleted is not None:
            self.table[first_deleted].key = key
            self.table[first_deleted].records = LinkedList()
            self.table[first_deleted].records.append(record)
            self.table[first_deleted].status = 1

            self.size += 1
            return True

        return False

    def search(self, key):
        primary_hash = self._middle_square_hash(key)
        secondary_hash = self._secondary_hash(key)
        steps = 0

        for i in range(self.capacity):
            index = self._probe(primary_hash, secondary_hash, i)
            slot = self.table[index]
            steps += 1

            if slot.status == 0:
                break

            if slot.status == 1 and slot.key == key:
                return slot.records, steps

        return LinkedList(), steps

    def delete_record(self, key, record):
        primary_hash = self._middle_square_hash(key)
        secondary_hash = self._secondary_hash(key)
        steps = 0

        for i in range(self.capacity):
            index = self._probe(primary_hash, secondary_hash, i)
            slot = self.table[index]
            steps += 1

            if slot.status == 0:
                return False, steps

            if slot.status == 1 and slot.key == key:
                deleted = slot.records.remove_by_reference(record)

                if deleted and slot.records.is_empty():
                    slot.key = None
                    slot.records = LinkedList()
                    slot.status = 2
                    self.size -= 1

                    if self._need_shrink():
                        self._shrink()

                return deleted, steps

        return False, steps

    def clear(self):
        self.size = 0
        self.table = [HashSlot() for _ in range(self.capacity)]

    def debug_print(self):
        lines = []
        lines.append("index | status | key | primary_hash | secondary_hash | records")
        lines.append("-" * 90)

        for i, slot in enumerate(self.table):
            if slot.status == 1:
                primary_hash = self._middle_square_hash(slot.key)
                secondary_hash = self._secondary_hash(slot.key)
                records_count = len(slot.records)
            else:
                primary_hash = "---"
                secondary_hash = "---"
                records_count = 0

            lines.append(
                f"{i:<5} | {slot.status:<6} | {str(slot.key):<5} | "
                f"{str(primary_hash):<12} | {str(secondary_hash):<15} | записей: {records_count}"
            )

        return "\n".join(lines)