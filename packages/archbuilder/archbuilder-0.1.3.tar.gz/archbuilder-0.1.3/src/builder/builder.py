"""
"""

from pathlib import Path


class Builder:
    """"""

    def __init__(self, project, template, output="build", root=Path.cwd()):
        """"""
        self.project = project
        self.template = template
        self.output = output
        self.root = root

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
