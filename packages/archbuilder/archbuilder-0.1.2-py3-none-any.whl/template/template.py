"""
"""

import json


class Template:
    """"""

    def __init__(self, name):
        """"""
        self.name = name

    def tails(self):
        """"""
        tails = list()
        for i in self.structure():
            tail = "/".join(i)
            tails.append(tail)
        return tails

    def structure(self):
        """"""
        template = self.load()
        structure = self.traverse(template)
        return list(structure)

    def load(self):
        """"""
        with open(self.name) as f:
            return json.load(f)

    def traverse(self, template, parent=None):
        """"""
        parent = parent[:] if parent else []
        if isinstance(template, dict):
            for key, value in template.items():
                if isinstance(value, dict):
                    for d in self.traverse(value, parent + [key]):
                        yield d
                elif isinstance(value, list) or isinstance(value, tuple):
                    for v in value:
                        for d in self.traverse(v, parent + [key]):
                            yield d
                else:
                    yield parent + [key, value]
        else:
            yield parent + [template]
