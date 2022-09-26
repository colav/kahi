import json
import pathlib
import os




class ImportSchemas():
    def __init__(self):
        pass

    def get_affiliation(self):
        root=pathlib.Path().resolve()
        path=os.path.join(root,"etc","schemas","affiliation.json")
        with open(path) as f:
            return json.load(f)

    def get_person(self):
        root=pathlib.Path().resolve()
        path=os.path.join(root,"etc","schemas","person.json")
        with open(path) as f:
            return json.load(f)

    def get_source(self):
        root=pathlib.Path().resolve()
        path=os.path.join(root,"etc","schemas","source.json")
        with open(path) as f:
            return json.load(f)

    def get_subject(self):
        root=pathlib.Path().resolve()
        path=os.path.join(root,"etc","schemas","subject.json")
        with open(path) as f:
            return json.load(f)

    def get_work(self):
        root=pathlib.Path().resolve()
        path=os.path.join(root,"etc","schemas","work.json")
        with open(path) as f:
            return json.load(f)
