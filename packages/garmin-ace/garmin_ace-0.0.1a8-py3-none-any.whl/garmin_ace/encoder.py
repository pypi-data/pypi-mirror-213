import zlib
import struct

from garmin_ace import constants
from garmin_ace import models


class ACEFileEncoder:

    def __init__(self, checklist_file: models.ChecklistFile):
        self.checklist_file = checklist_file

    def write_to_data(self):
        data = bytearray()
        self.write(data)
        return data

    def write_to_file(self, filename: str):
        data = self.write_to_data()
        with open(filename, "wb") as f:
            f.write(data)

    def write(self, data: bytearray):
        data.extend(constants.MAGIC_NUMBER_AND_REVISION)
        self.encode_set(self.checklist_file, data)
        self.encode_string(constants.SET_END, data, newline=True)
        data.extend(self.checksum(data))

    def encode_set(self, checklist_file: models.ChecklistFile, data: bytearray):
        self.encode_string(checklist_file.name, data, newline=True)
        self.encode_string(checklist_file.make_and_model, data, newline=True)
        self.encode_string(checklist_file.aircraft_info, data, newline=True)
        self.encode_string(checklist_file.manufacturer_id, data, newline=True)
        self.encode_string(checklist_file.copyright, data, newline=True)
        for group in checklist_file.groups:
            self.encode_group(group, data)

    def encode_group(self, group: models.ChecklistGroup, data: bytearray):
        self.encode_string(constants.GROUP_START, data)
        self.encode_indent(group.indent, data)
        self.encode_string(group.name, data, newline=True)
        for checklist in group.checklists:
            self.encode_checklist(checklist, data)
        self.encode_string(constants.GROUP_END, data, newline=True)

    def encode_checklist(self, checklist: models.Checklist, data: bytearray):
        self.encode_string(constants.CHECKLIST_START, data)
        self.encode_indent(checklist.indent, data)
        self.encode_string(checklist.name, data, newline=True)
        for item in checklist.items:
            self.encode_item(item, data)
        self.encode_string(constants.CHECKLIST_END, data, newline=True)

    def encode_item(self, item: models.Item, data: bytearray):
        if item.type == 'title':
            self.encode_string("t", data)
            self.encode_indent(item.indent, data)
            self.encode_string(item.text, data, newline=True)
        elif item.type == 'warning':
            self.encode_string("w", data)
            self.encode_indent(item.indent, data)
            self.encode_string(item.text, data, newline=True)
        elif item.type == 'caution':
            self.encode_string("c", data)
            self.encode_indent(item.indent, data)
            self.encode_string(item.text, data, newline=True)
        elif item.type == 'note':
            self.encode_string("n", data)
            self.encode_indent(item.indent, data)
            self.encode_string(item.text, data, newline=True)
        elif item.type == 'plaintext':
            self.encode_string("p", data)
            self.encode_indent(item.indent, data)
            self.encode_string(item.text, data, newline=True)
        elif item.type == 'challenge_response':
            self.encode_string("r", data)
            self.encode_indent(item.indent, data)
            self.encode_string(item.text, data)
            self.encode_string(constants.CHALLENGE_RESPONSE_SEPARATOR, data)
            self.encode_string(item.response, data, newline=True)
        elif item.type == 'blank':
            self.encode_string("", data, newline=True)
        else:
            raise ValueError(f"Unexpected item type: {type(item)}")

    def encode_indent(self, indent, data: bytearray):
        if indent == "centered":
            self.encode_string(constants.CENTERED_INDENT, data)
        else: # level indentation
            self.encode_string(str(indent), data)

    def encode_string(self, string: str, data: bytearray, newline: bool = False):
        try:
            string_data = string.encode('cp1252')
        except UnicodeEncodeError:
            raise EncoderError('Invalid character for encoding')
        data.extend(string_data)
        if newline:
            data.extend(constants.CRLF.encode('cp1252'))

    def checksum(self, data: bytearray):
        checksum = zlib.crc32(data)
        return struct.pack('<L', ~checksum & 0xffffffff)

