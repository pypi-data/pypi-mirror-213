from numbers import Number

from rich.tree import Tree


def create_tree_row(columns, root, traverse_fn, extract_value_fn):
    column_data_list = [[] for _ in columns]

    def format_cell_value(cell_value) -> str:
        if cell_value is None:
            return ""
        elif isinstance(cell_value, Number):
            return format(cell_value, ".2f")
        return str(cell_value)

    def traverse_build(node, node_tree):
        for i, column in enumerate(columns):
            cell_value = format_cell_value(extract_value_fn(column, node))
            column_data_list[i].append(cell_value)

        children = traverse_fn(node)
        if children is not None:
            for child in children:
                child_tree = node_tree.add(child.title)
                traverse_build(child, child_tree)

    root_tree = Tree(root.title)
    traverse_build(root, root_tree)

    row = []
    for i, column in enumerate(columns):
        if column.data == "title":
            row.append(root_tree)
        else:
            row.append("\n".join(column_data_list[i]))

    return row
