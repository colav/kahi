from kahi import kahi, schemas
from time import time
from pymongo import MongoClient

class KahiRor():
    def __init__(self,verbose=0):
        self.verbose=verbose
        self.schemas=schemas.ImportSchemas()
        self.affiliation=self.schema.get_affiliation()

def parse_affiliations(self,reg):
    self.affiliation["updated"].append({"source":"ror","time":int(time())})
    self.affiliation["names"].append({"source":"ror","names":[{"lang":"es","name":reg["name"]}]})
    self.affiliation["aliases"].append({"source":"ror","aliases":[reg["aliases"]]})
    self.affiliation["types"].append({"source":"ror","types":reg["types"]})
    self.affiliation["status"].append({"source":"ror","status":reg["status"]})

    year=int(reg["established"]) if reg["established"] else -1
    self.affiliation["year_established"].append({"source":"ror","year_established":year})

    self.affiliation["addresses"].append({"source":"ror","addresses":[]})
    for add in reg["addresses"]:
        add_entry={
            "lat":add["lat"],
            "lng":add["lng"],
            "postcode":add["postcode"] if add["postcode"] else "",
            "state":add["state"],
            "city":add["city"],
            "country":"",
            "country_code":"",
        }
        self.affiliation["addresses"][0]["addresses"].append(add_entry)
    self.affiliation["addresses"][0]["addresses"][0]["country"]=inst["country"]["country_name"]
    self.affiliation["addresses"][0]["addresses"][0]["country_code"]=inst["country"]["country_code"]

    self.affiliation["external_urls"].append({"source":"ror","external_urls":[]})
    if reg["links"]:
        for link in reg["links"]:
            url_entry={"source":"site","url":inst["links"][0]}
            if not url_entry in self.affiliation["external_urls"][0]["external_urls"]:
                self.affiliation["external_urls"][0]["external_urls"].append(url_entry)
    if reg["wikipedia_url"]:
        self.affiliation["external_urls"][0]["external_urls"].append({"source":"wikipedia","url":inst["wikipedia_url"]})

    self.affiliation["external_ids"].append({"source":"ror","external_ids":[]})
    if reg["external_ids"]:
        for key,ext in reg["external_ids"].items():
            alll=ext["all"][0] if isinstance(ext["all"],list) else ext["all"]
            ext_entry={"source":key.lower(),"id":alll}
            if not ext_entry in entry["external_ids"]:
                self.affiliation["external_ids"][0]["external_ids"].append(ext_entry)
    self.affiliation["external_ids"][0]["external_ids"].append({"source":"ror","id":inst["id"]})
    

def update_relations(self,
                    mongo_ror_url,mongo_ror_port,ror_db,ror_collection,
                    mongo_colav_url,mongo_colav_port,colav_db,colav_collection,
                    insert=False):
    
    ror_client=MongoClient(mongo_ror_url,mongo_ror_port)
    colav_client=MongoClient(mongo_colav_url,mongo_colav_port)

    self.affiliation["relations"].append({"source":"ror","relations":[]})
    for inst in ror_client[ror_db][ror_collection].find({"relationships":{"$ne":[]}}):
        relations=[]
        updatable_entry=colav_client[colav_db][colav_collection].find_one({"external_ids.external_ids.id":inst["id"]})
        if not updatable_entry:
            if self.verbose>=5:
                print("Could not find institution with id ",inst["id"])
            continue
        for rel in inst["relationships"]:
            db_entry=colav_client[colav_db][colav_collection].find_one({"external_ids.external_ids.id":rel["id"]})
            if db_entry:
                re_sub={"id":db_entry["_id"],"name":db_entry["names"][0]["name"],"type":rel["type"]}
                if not re_sub in rel_entry:
                    relations.append(re_sub)
            else:
                if self.verbose>=5:
                    print("Could not find relation with the ror id ",rel["id"])
        if insert:
            mod={"relations":{"source":"ror","relations":rel_entry}}
            colav_client[colav_db][colav_collection].update_one({"_id":updatable_entry["_id"]},{"$set":mod})

    