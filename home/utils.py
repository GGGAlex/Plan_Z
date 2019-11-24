import math


class Pagination(object):
    def __init__(self, page, per_page, iterable):
        self.page = page
        self.per_page = per_page
        self.iterable = iterable
        self.total = len(iterable)

    @property
    def total_pages(self):
        return int(math.ceil(self.total/self.per_page))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.total_pages

    @property
    def items(self):
        index = self.page - 1
        start = index * self.per_page
        end = start + self.per_page
        return self.iterable[start:end]

    @property
    def range_last(self):
        if self.page - 5 > 0:
            return self.page - 5
        else:
            return 0

    @property
    def range_next(self):
        if self.page + 5 < self.total_pages:
            return self.page + 5
        else:
            return self.total_pages