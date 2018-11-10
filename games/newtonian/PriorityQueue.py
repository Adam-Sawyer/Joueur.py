class PriorityQueue:
    def __init__(self):
        self.buckets = {}  # priority: value

    @property
    def values(self):
        # TODO - Is this organized by priority
        return sum(self.buckets.values(), [])

    def __getattr__(self, index):
        return self.values[index]

    def add(self, priority, value):
        if priority in self.buckets.keys():
            self.buckets[priority].append(value)
        else:
            self.buckets[priority] = [value]

    def pop(self):
        if not self.buckets:
            return -1  ### Returns -1 when empty

        min_key = min(self.buckets.keys())

        temp = self.buckets[min_key].pop(0)

        if len(self.buckets[min_key]) == 0:
            del self.buckets[min_key]

        return temp

    def clear(self):
        self.buckets = {}

if True: #__name__ == '__main__':
    tester = PriorityQueue()
    tester.add(5, '9')
    tester.add(2, '1')
    tester.add(1, '3')
    #tester.add(5, '10')

    print(tester.values)
