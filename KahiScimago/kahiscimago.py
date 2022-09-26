from kahi import kahi, schemas
from time import time
import iso3166

class kahiScimago():
    def __init__(self,verbose=0):
        '''
        Base class to parse scimago data into colav standard
        '''
        self.schemas=schemas.ImportSchemas()
        self.source=self.schema.get_source()
        self.verbose=verbose

    def parse_sources(self,reg):
        self.source["updated"].append({"source":"scimago","time":int(time())})
        self.source["names"].append({"source":"scimago","names":[{"lang":"es","name":reg["Title"]}]})
        self.source["types"].append({"source":"scimago","types":[reg["Type"]]})
        self.source["publisher"].append({"source":"scimago","publisher":{"name":reg["Publisher"]}})

        try:
            code=iso3166.countries_by_alpha2.get(reg["publisher"]["country"].upper()).alpha2
        except:
            code=""
            if self.verbose>=5:
                print("Could not find {} in iso3166 library".format(reg["Country"]))
        self.source["addresses"].append({"source":"doaj","addresses":{"country":reg["Country"],"country_code":code,"region":reg["Region"]}})

        self.source["external_ids"].append({"source":"scimago","external_ids":[]})
        self.source["external_ids"][0]["external_ids"].append({"source":"scimago","id":int(reg["Sourceid"])})
        for issn in reg["Issn"].split(", "):
            issn=issn[:4]+"-"+issn[4:]
            self.source["external_ids"][0]["external_ids"].append({"source":"issn","id":issn})

        self.source["ranking"].append({"source":"scimago","ranking":[]})
        self.source["ranking"][0]["ranking"].append({
            "date":1640995199,
            "rank":reg["SJR Best Quartile"],
            "order":int(reg["Rank"]) if reg["Rank"] else "",
            "id":"",
            "source":"scimago Best Quartile"
        })
        self.source["ranking"][0]["ranking"].append({
            "date":1640995199,
            "rank":int(reg["H index"]),
            "order":int(reg["Rank"]) if reg["Rank"] else "",
            "id":"",
            "source":"scimago hindex"
        })
        if reg["SJR"]:
            rank=""
            if isinstance(reg["SJR"],str):
                rank=float(reg["SJR"].replace(",","."))
            else:
                rank=reg["SJR"]
            self.source["ranking"][0]["ranking"].append({
                "date":1640995199,
                "rank": rank,
                "order":int(reg["Rank"]) if reg["Rank"] else "",
                "id":"",
                "source":"scimago"
            })

        self.source["subjects"].append({"source":"scimago","subjects":[]})
        scimago_subjects=[]
        for cat in reg["Categories"].split(";"):
            scimago_subjects.append({
                "id":"",
                "name":cat.split(" (")[0],
                "date":1640995199,
                "rank":cat.split(" (")[-1].replace(")",""),
                "external_ids":[]
            })
        self.source["subjects"][0]["subjects"].append({
            "source":"scimago",
            "subjects":scimago_subjects
        })