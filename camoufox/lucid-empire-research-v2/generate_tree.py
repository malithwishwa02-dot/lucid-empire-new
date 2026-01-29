import os

def generate_tree(startpath):
    tree_str = ""
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree_str += '{}{}/\n'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            tree_str += '{}{}\n'.format(subindent, f)
    return tree_str

if __name__ == "__main__":
    root_dir = os.path.abspath(".")
    tree = generate_tree(root_dir)
    with open("LUCID_REPO_TREE.txt", "w", encoding="utf-8") as f:
        f.write(tree)
    print("Tree generated at LUCID_REPO_TREE.txt")
