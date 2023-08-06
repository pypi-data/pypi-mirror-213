import argparse

import ast_comments as ast
import black
from pathier import Pathier


def get_seat_sections(source: str) -> list[tuple[int, int]]:
    """Return a list of line number pairs for content between `# Seat` comments in `source`.

    If `source` has no `# Seat` comments, a list with one tuple will be returned: `[(1, number_of_lines_in_source)]`"""

    if "# Seat" in source:
        lines = source.splitlines()
        sections = []
        previous_endline = lambda: sections[-1][1]
        for i, line in enumerate(lines):
            if "# Seat" in line:
                if not sections:
                    sections = [(1, i + 1)]
                else:
                    sections.append((previous_endline() + 1, i + 1))
        sections.append((previous_endline() + 1, len(lines) + 1))
        return sections
    return [(1, len(source.splitlines()) + 1)]


class Seats:
    def __init__(self):
        self.before = []
        self.assigns = []
        self.dunders = []
        self.properties = []
        self.functions = []
        self.after = []
        self.seats = []
        # These will be a list of tuples containing the node and the index it was found at
        # so they can be reinserted after sorting
        self.expressions = []
        self.comments = []

    def sort_nodes_by_name(self, nodes: list[ast.stmt]) -> list[ast.stmt]:
        return sorted(nodes, key=lambda node: node.name)

    def sort_dunders(self, dunders: list[ast.stmt]) -> list[ast.stmt]:
        """Sort `dunders` alphabetically, except `__init__` is placed at the front, if it exists."""
        dunders = self.sort_nodes_by_name(dunders)
        init = None
        for i, dunder in enumerate(dunders):
            if dunder.name == "__init__":
                init = dunders.pop(i)
                break
        if init:
            dunders.insert(0, init)
        return dunders

    def sort_assigns(self, assigns: list[ast.stmt]) -> list[ast.stmt]:
        """Sort assignment statments."""

        def get_name(node: ast.stmt) -> str:
            type_ = type(node)
            if type_ == ast.Assign:
                return node.targets[0].id
            else:
                return node.target.id

        return sorted(assigns, key=get_name)

    def sort(self) -> list[ast.stmt]:
        """Sort and return members as a single list."""
        self.dunders = self.sort_dunders(self.dunders)
        self.functions = self.sort_nodes_by_name(self.functions)
        self.properties = self.sort_nodes_by_name(self.properties)
        self.assigns = self.sort_assigns(self.assigns)
        body = (
            self.before
            + self.assigns
            + self.dunders
            + self.properties
            + self.functions
            + self.seats
            + self.after
        )
        for expression in self.expressions + self.comments:
            body.insert(expression[1], expression[0])
        return body


def seat(
    source: str, start_line: int | None = None, stop_line: int | None = None
) -> str:
    """Sort the contents of classes in `source`, where `source` is parsable Python code.
    Anything not inside a class will be untouched.

    The modified `source` will be returned.

    #### :params:

    * `start_line`: Only sort contents after this line.

    * `stop_line`: Only sort contents before this line.

    If you have class contents that are grouped a certain way and you want the groups individually sorted
    so that the grouping is maintained, you can use `# Seat` to demarcate the groups.

    i.e. if the source is:
    >>> class MyClass():
    >>>     {arbitrary lines of code}
    >>>     # Seat
    >>>     {more arbitrary code}
    >>>     # Seat
    >>>     {yet more code}

    Then the three sets of code in brackets will be sorted independently from one another
    (assuming no values are given for `start_line` or `stop_line`).

    #### :Sorting and Priority:

    * Class variables declared in class body outside of a function
    * Dunder methods
    * Functions decorated with `property` or corresponding `.setter` and `.deleter` methods
    * Class functions

    Each of these groups will be sorted alphabetically with respect to themselves.

    The only exception is for dunder methods.
    They will be sorted alphabetically except that `__init__` will be first.
    """
    tree = ast.parse(source, type_comments=True)
    start_line = start_line or 0
    stop_line = stop_line or len(source.splitlines()) + 1
    sections = get_seat_sections(source)
    for section in sections:
        for i, stmt in enumerate(tree.body):
            if type(stmt) == ast.ClassDef:
                order = Seats()
                for j, child in enumerate(stmt.body):
                    try:
                        type_ = type(child)
                        if child.lineno <= start_line or child.lineno < section[0]:
                            order.before.append(child)
                        elif stop_line < child.lineno or child.lineno > section[1]:
                            order.after.append(child)
                        elif type_ == ast.Expr:
                            order.expressions.append((child, j))
                        elif type_ == ast.Comment:
                            if "# Seat" in child.value:
                                order.seats.append(child)
                            else:
                                order.comments.append((child, j))
                        elif type_ in [ast.Assign, ast.AugAssign, ast.AnnAssign]:
                            order.assigns.append(child)
                        elif child.name.startswith("__") and child.name.endswith("__"):
                            order.dunders.append(child)
                        elif child.decorator_list:
                            for decorator in child.decorator_list:
                                decorator_type = type(decorator)
                                if (
                                    decorator_type == ast.Name
                                    and "property" in decorator.id
                                ) or (
                                    decorator_type == ast.Attribute
                                    and decorator.attr in ["setter", "deleter"]
                                ):
                                    order.properties.append(child)
                                    break
                            if child not in order.properties:
                                order.functions.append(child)
                        else:
                            order.functions.append(child)
                    except Exception as e:
                        print(ast.dump(child, indent=2))
                        raise e
                tree.body[i].body = order.sort()
    return ast.unparse(tree)


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("file", type=str, help=""" The file to format. """)
    parser.add_argument(
        "--start",
        type=int,
        default=None,
        help=""" Optional line number to start formatting at. """,
    )
    parser.add_argument(
        "--stop",
        type=int,
        default=None,
        help=""" Optional line number to stop formatting at. """,
    )
    parser.add_argument(
        "-nb",
        "--noblack",
        action="store_true",
        help=""" Don't format file with Black after sorting. """,
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help=""" Write changes to this file, otherwise changes are written back to the original file. """,
    )
    parser.add_argument(
        "-d",
        "--dump",
        action="store_true",
        help=""" Dump ast tree to file instead of doing anything else. 
        For debugging purposes.""",
    )
    args = parser.parse_args()

    return args


def main(args: argparse.Namespace | None = None):
    if not args:
        args = get_args()
    source = Pathier(args.file).read_text()
    if args.dump:
        file = Pathier(args.file)
        file = file.with_name(f"{file.stem}_ast_dump.txt").write_text(
            ast.dump(ast.parse(source, type_comments=True), indent=2)
        )
    else:
        source = seat(source, args.start, args.stop)
        if not args.noblack:
            source = black.format_str(source, mode=black.Mode())
        Pathier(args.output or args.file).write_text(source)


if __name__ == "__main__":
    main(get_args())
