class ChecklistFile:
    def __init__(self, name, make_and_model, aircraft_info, manufacturer_id, copyright):
        self.name = name
        self.make_and_model = make_and_model
        self.aircraft_info = aircraft_info
        self.manufacturer_id = manufacturer_id
        self.copyright = copyright
        self.groups = []

    def add_group(self, group):
        self.groups.append(group)


class ChecklistGroup:
    def __init__(self, name, indent):
        self.name = name
        self.indent = indent
        self.checklists = []

    def add_checklist(self, checklist):
        self.checklists.append(checklist)


class Checklist:
    def __init__(self, name, indent):
        self.name = name
        self.indent = indent
        self.items = []

    def add_item(self, item):
        self.items.append(item)


class Item:
    def __init__(self, type, text=None, indent=None, challenge=None, response=None):
        self.type = type
        self.text = text
        self.indent = indent
        self.challenge = challenge
        self.response = response

    @classmethod
    def title(cls, text, indent):
        return cls("title", text=text, indent=indent)

    @classmethod
    def warning(cls, text, indent):
        return cls("warning", text=text, indent=indent)

    @classmethod
    def caution(cls, text, indent):
        return cls("caution", text=text, indent=indent)

    @classmethod
    def note(cls, text, indent):
        return cls("note", text=text, indent=indent)

    @classmethod
    def plaintext(cls, text, indent):
        return cls("plaintext", text=text, indent=indent)

    @classmethod
    def challenge_response(cls, challenge, response, indent):
        return cls("challenge_response", challenge=challenge, response=response, indent=indent)

    @classmethod
    def blank(cls):
        return cls("blank")

