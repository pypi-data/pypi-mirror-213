"""
"""

from pathlib import Path


class Builder:
    """"""

    root = Path(__file__).resolve().parent.parent.parent

    def __init__(self, project, template, output="build"):
        """"""
        self.project = project
        self.output = output
        self.template = template

    def build(self):
        """"""
        for path in self.paths():
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch(exist_ok=True)

    def paths(self):
        """"""
        paths = list()
        for tail in self.template.tails():
            path = Path(self.root / self.output / self.project / tail)
            paths.append(path)
        return paths
