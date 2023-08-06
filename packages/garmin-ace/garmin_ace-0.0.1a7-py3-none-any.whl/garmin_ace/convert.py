#!/usr/bin/env python3

import orgparse
import sys
import os

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

from garmin_ace import models
from garmin_ace.decoder import ACEFileDecoder
from garmin_ace.encoder import ACEFileEncoder


class FileHandler:
    extension = None

    @classmethod
    def matches_extension(cls, filename):
        return os.path.splitext(filename)[1] == cls.extension

    def import_file(self, filename):
        raise NotImplementedError(f"Importing from {self.extension} format is not supported")

    def export_file(self, obj, filename):
        raise NotImplementedError(f"Exporting to {self.extension} format is not supported")


class OrgFileHandler(FileHandler):
    extension = '.org'

    def import_file(self, filename):
        root = orgparse.load(filename)
        file = models.ChecklistFile()
        group = models.ChecklistGroup()
        file.add_group(group)

        for checklist_node in root.children:
            checklist = models.Checklist(checklist_node.heading)
            group.add_checklist(checklist)

            for item_node in checklist_node.children:
                self.handle_node(item_node, checklist, 0)

        return file

    @staticmethod
    def handle_node(node, checklist, depth):
        try:
            challenge, response = node.heading.split(':', 1)
            response = response.upper()
        except ValueError:
            challenge, response = node.heading, 'OK'

        item = models.Item.challenge_response(challenge, response, depth)
        checklist.add_item(item)

        for child in node.children:
            OrgFileHandler.handle_node(child, checklist, depth + 1)


class AceFileHandler(FileHandler):
    extension = '.ace'

    def import_file(self, filename):
        return ACEFileDecoder.read_from_file(filename)

    def export_file(self, obj, filename):
        encoder = ACEFileEncoder(obj)
        encoder.write_to_file(filename)


class HtmlFileHandler(FileHandler):
    extension = '.html'

    def export_file(self, obj, filename):
        html = self.format_items_html(obj)
        with open(filename, 'w') as f:
            f.write(html)

    @classmethod
    def format_items_html(cls, cl_obj):
        root = Element('html')
        head = SubElement(root, 'head')

        title = SubElement(head, 'title')
        title_str = f'Checklist'# {cl_obj.make_and_model} ({cl_obj.aircraft_info})'
        title.text = title_str

        style = SubElement(head, 'style')
        style.text = cls.get_style()

        body = SubElement(root, 'body')
        h1 = SubElement(body, 'h1', {'style': "text-align: center"})
        h1.text = title_str

        for cl_group in cl_obj.groups:
            h2 = SubElement(body, 'h2')
            h2.text = cl_group.name

            for cl in cl_group.checklists:
                cl_div = cls.div_multi_col() #cl.name == "Preflight Inspection")
                h3 = SubElement(cl_div, 'h3', {'style': "text-align: center"})
                h3.text = cl.name

                ul = SubElement(cl_div, 'ul')
                for cl_item in cl.items:
                    li = SubElement(ul, 'li', {'class': 'row'})

                    left = SubElement(li, 'span', {'class': 'left'})
                    left.text = cl_item.text

                    ellipsis = SubElement(li, 'span', {'class': 'ellipsis'})
                    ellipsis.text = '.' * 1000

                    right = SubElement(li, 'span', {'class': 'right'})
                    if cl_item.type == 'challenge_response':
                        right.text = cl_item.response
                    else:
                        right.text = 'OK'

                body.append(cl_div)

        html_str = minidom.parseString(tostring(root)).toprettyxml(indent="   ")
        return html_str

    @classmethod
    def div_multi_col(cls, multi=False):
        div_style = "border-style:solid; margin: 10px; column-count:1; page-break-inside:avoid;"
        if multi:
            div_style = "border-style:solid; margin: 10px; column-break-inside:avoid; column-count:2; page-break-inside:avoid;"
        return Element('div', {'style': div_style})

    @classmethod
    def get_style(cls):
        current_file = os.path.realpath(__file__)
        parent_folder = os.path.dirname(current_file)
        parent_folder = os.path.dirname(parent_folder) # Go up two folders
        style_filename = os.path.join(parent_folder, 'html', 'style.css')
        with open(style_filename, 'r') as f:
            return f.read()


def get_handler_for_file(filename, handlers):
    for handler in handlers:
        if handler.matches_extension(filename):
            return handler()
    raise ValueError(f"Unsupported file format: {filename}")


def get_supported_formats(handlers):
    import_formats = [
        handler.extension for handler in handlers 
        if handler.import_file != FileHandler.import_file
    ]
    export_formats = [
        handler.extension for handler in handlers 
        if handler.export_file != FileHandler.export_file
    ]
    return import_formats, export_formats


def main():
    handlers = [OrgFileHandler, AceFileHandler, HtmlFileHandler]

    if len(sys.argv) != 3:
        print(f"Convert source file to destination file")
        print(f"Usage: {sys.argv[0]} <source> <dest>")

        import_formats, export_formats = get_supported_formats(handlers)
        print(f"Supported source formats are: {', '.join(import_formats)}")
        print(f"Supported destination formats are: {', '.join(export_formats)}")

        sys.exit(1)

    source_filename = sys.argv[1]
    dest_filename = sys.argv[2]
    try:
        importer = get_handler_for_file(source_filename, handlers)
        exporter = get_handler_for_file(dest_filename, handlers)

        file_obj = importer.import_file(source_filename)
        exporter.export_file(file_obj, dest_filename)
    except NotImplementedError as e:
        sys.exit(f"Error: {e}")


if __name__ == "__main__":
    main()

