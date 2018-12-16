class DisjointSetUnion:
    parents = {}
    num_sets = 0

    def make_set(self, a):
        self.parents[a] = a
        self.num_sets += 1

    def find_set(self, a):
        if a == self.parents[a]:
            return a
        else:
            self.parents[a] = self.find_set(self.parents[a])
            return self.parents[a]

    def union_sets(self, a, b):
        a = self.find_set(a)
        b = self.find_set(b)
        if a != b:
            self.num_sets -= 1
            self.parents[b] = a
