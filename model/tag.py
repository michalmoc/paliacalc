from functools import cached_property


class Tag:
    def __init__(self, lst):
        self.lst = lst

    @cached_property
    def options(self) -> [str]:
        return [i['key'] for i in self.lst]
