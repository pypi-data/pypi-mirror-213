#!/usr/bin/env python3

import orgparse
import sys

import models
from encoder import ACEFileEncoder

def org_to_checklist(filename):
    root = orgparse.load(filename)

    file = models.ChecklistFile()
    group = models.ChecklistGroup()
    file.add_group(group)

    # Iterate over the children of the root node. Each child is a checklist
    for checklist_node in root.children:
        checklist = models.Checklist(checklist_node.heading)
        group.add_checklist(checklist)

        # Iterate over the children of the checklist node. Each child is an item
        for item_node in checklist_node.children:
            handle_node(item_node, checklist, 0)

    return file


def handle_node(node, checklist, depth):
    """A recursive function to handle items at any level of depth"""

    item = models.Item.challenge_response(node.heading, 'OK', depth)
    checklist.add_item(item)

    for child in node.children:
        handle_node(child, checklist, depth + 1)


def main():
    if len(sys.argv) != 3:
        print(f"Convert orgmode file to ace file")
        print(f"Usage: {sys.argv[0]} <source.org> <dest.ace>")
        sys.exit(1)

    source_filename = sys.argv[1]
    dest_filename = sys.argv[2]

    ace_obj = org_to_checklist(source_filename)

    encoder = ACEFileEncoder(ace_obj)
    encoder.write_to_file(dest_filename)

if __name__ == "__main__":
    main()

