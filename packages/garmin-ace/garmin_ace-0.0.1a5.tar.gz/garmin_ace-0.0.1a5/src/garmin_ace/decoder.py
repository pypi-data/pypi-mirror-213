import os
import sys

from garmin_ace import constants
from garmin_ace import models
from garmin_ace.utils import StringScanner, from_char

class ACEFileDecoder:
    @staticmethod
    def read_from_file(filename):
        with open(filename, 'rb') as f:
            data = f.read()
        return ACEFileDecoder.decode(data)

    @staticmethod
    def decode(data):
        header = data[:10]
        if header != constants.MAGIC_NUMBER_AND_REVISION:
            raise Exception("Invalid magic number or revision")
        
        # Strip the header and end of the file (checksum)
        body = data[10:-6] 

        body_string = body.decode('cp1252')
        return ACEFileDecoder.decode_body(body_string)

    @staticmethod
    def decode_body(body):
        scanner = StringScanner(body)
        checklist_file = ACEFileDecoder.scan_header(scanner)

        while not scanner.match(constants.SET_END):
            checklist_group = ACEFileDecoder.scan_group(scanner)
            if checklist_group is None:
                raise Exception("Expected checklist group")
            checklist_file.groups.append(checklist_group)
        return checklist_file

    @staticmethod
    def scan_header(scanner):
        name = scanner.scan_up_to(constants.CRLF)
        if name is None:
            raise Exception("Invalid header")
        
        make_and_model = scanner.scan_up_to(constants.CRLF)
        if make_and_model is None:
            raise Exception("Invalid header")

        aircraft_info = scanner.scan_up_to(constants.CRLF)
        if aircraft_info is None:
            raise Exception("Invalid header")

        manufacturer_id = scanner.scan_up_to(constants.CRLF)
        if manufacturer_id is None:
            raise Exception("Invalid header")

        copyright = scanner.scan_up_to(constants.CRLF)
        if copyright is None:
            raise Exception("Invalid header")

        return models.ChecklistFile(name, make_and_model, aircraft_info, manufacturer_id, copyright)

    @staticmethod
    def scan_group(scanner):
        if scanner.scan(1) != constants.GROUP_START:
            return None

        indent = scanner.scan(1)
        name = scanner.scan_up_to(constants.CRLF)
        if name is None:
            raise Exception("Invalid header")

        group = models.ChecklistGroup(name, indent)

        while not scanner.match(constants.GROUP_END):
            checklist = ACEFileDecoder.scan_checklist(scanner)
            if checklist is None:
                raise Exception("Expected checklist")
            group.checklists.append(checklist)
        scanner.skip(1)

        if not scanner.match(constants.CRLF):
            raise Exception("Expected newline")
        scanner.skip(len(constants.CRLF))

        return group

    @staticmethod
    def scan_checklist(scanner):
        if scanner.scan(1) != constants.CHECKLIST_START:
            return None

        indent = scanner.scan(1)
        name = scanner.scan_up_to(constants.CRLF)
        if name is None:
            raise Exception("Invalid header")

        checklist = models.Checklist(name, indent)

        while not scanner.match(constants.CHECKLIST_END):
            item = ACEFileDecoder.scan_item(scanner)
            checklist.items.append(item)
        scanner.skip(len(constants.CHECKLIST_END))

        if not scanner.match(constants.CRLF):
            raise Exception("Expected newline")
        scanner.skip(len(constants.CRLF))

        return checklist

    @staticmethod
    def scan_item(scanner):
        if scanner.match(constants.CRLF):
            return models.Item.blank

        type_char = scanner.scan(1)
        indent_char = scanner.scan(1)

        type = constants.ITEM_TYPE.get(type_char)
        if type is None:
            raise Exception("Invalid item type")
        indent = ACEFileDecoder.parse_indent(indent_char)

        content = scanner.scan_up_to(constants.CRLF)
        if content is None:
            raise Exception("Invalid item content")

        if type == "title":
            return models.Item.title(content, indent)
        elif type == "warning":
            return models.Item.warning(content, indent)
        elif type == "caution":
            return models.Item.caution(content, indent)
        elif type == "note":
            return models.Item.note(content, indent)
        elif type == "plaintext":
            return models.Item.plaintext(content, indent)
        elif type == "challenge_response":
            challenge, response = content.split(constants.CHALLENGE_RESPONSE_SEPARATOR)
            return models.Item.challenge_response(challenge, response, indent)

    @staticmethod
    def parse_indent(indent):
        if indent == constants.CENTERED_INDENT:
            return "centered"
        else:
            try:
                return int(indent)
            except ValueError:
                raise Exception("Invalid indent level")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(sys.argv[0])} <filename>")
        return

    file_name = sys.argv[1]

    with open(file_name, "rb") as file:
        data = file.read()

    decoder = ACEFileDecoder()
    checklist_file = decoder.decode(data)

    print(checklist_file.__dict__)


if __name__ == "__main__":
    main()

