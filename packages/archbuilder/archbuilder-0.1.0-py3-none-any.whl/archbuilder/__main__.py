import argparse

from builder import Builder
from template import Template


def get_args():
    parser = argparse.ArgumentParser(
        prog="archbuilder",
        description="Use '%(prog)s' to quickly build project structures from JSON templates",
    )
    parser.add_argument("project", type=str)
    parser.add_argument("template", type=str)
    parser.add_argument("-o", "--output", type=str, default="build")

    return parser.parse_args()


def main():
    args = get_args()

    template = Template(args.template)
    project = Builder(args.project, template, args.output)

    project.build()


if __name__ == "__main__":
    main()
