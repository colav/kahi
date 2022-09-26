from kahi import kahi, schemas
from time import time
import iso3166

class kahiDoaj():
    def __init__(self,verbose=0):
        '''
        Base class to parse doaj data into colav standard
        '''
        self.schemas=schemas.ImportSchemas()
        self.source=self.schema.get_source()
        self.verbose=verbose

    def parse_sources(self,reg):
        reg=reg["bibjson"]
        self.source["updated"].append({"source":"doaj","time":int(time())})
        self.source["names"].append({"source":"doaj","names":{"lang":"en","name":reg["title"]}})
        self.source["keywords"].append({"source":"doaj","keywords":reg["keywords"]})
        self.source["languages"].append({"source":"doaj","languages":[l.lower() for l in reg["language"]]})
        self.source["publisher"].append({"source":"doaj","publisher":{"name":reg["publisher"]["name"]}})
        self.source["external_urls"].append({"source":"doaj","external_urls":[{"source":ref,"url":url} for ref,url in reg["ref"].items()]})
        self.source["review_processes"].append({"source":"doaj","review_process":reg["editorial"]["review_process"]})
        self.source["plagiarism_detection"].append({"source":"doaj","plagiarism_detection":reg["plagiarism"]["detection"]})
        self.source["open_access_start_year"].append({"source":"doaj",})
        self.source["publication_time_weeks"].append({"source":"doaj","publication_time_weeks":reg["publication_time_weeks"]})
        self.source["copyright"].append({"source":"doaj","copyright":reg["copyright"]})
        self.source["licenses"].append({"source":"doaj","licenses":reg["license"]})
        
        try:
            country=iso3166.countries_by_alpha2.get(reg["publisher"]["country"].upper()).name
        except:
            if self.verbose>=5:
                print("Could not find {} in iso3166 library".format(reg["publisher"]["country"]))
            country=""

        self.source["addresses"].append({"source":"doaj","addresses":{"country_code":reg["publisher"]["country"],"country":country}})

        if "apc" in reg.keys():
            if reg["apc"]["has_apc"]:
                self.source["apc"].append({"sorce":"doaj","apc":{"charges":reg["apc"]["max"][-1]["price"],"currency":reg["apc"]["max"][-1]["currency"]}})
        
        self.source["external_ids"].append({"source":"doaj","external_ids":{}})
        if "eissn" in reg.keys():
            self.source["external_ids"][0]["external_ids"].append({"source":"eissn","id":reg["eissn"]})
        if "pissn" in reg.keys():
            self.source["external_ids"][0]["external_ids"].append({"source":"pissn","id":reg["pissn"]})

        subjects_source={}
        if "subject" in reg.keys():
            if reg["subject"]:
                for sub in reg["subject"]:
                    sub_entry={
                        "id":"",
                        "name":sub["term"],
                        "external_ids":[{"source":sub["scheme"],"id":sub["code"]}]
                    }
                    if sub["scheme"] in subjects_source.keys():
                        subjects_source[sub["scheme"]].append(sub_entry)
                    else:
                        subjects_source[sub["scheme"]]=[sub_entry]
        self.source["subjects"].append({"source":"doaj","subjects":[]})
        for source,subs in subjects_source.items():
            entry["subjects"][0]["subjects"].append({
                "source":source,
                "subjects":subs
            })

