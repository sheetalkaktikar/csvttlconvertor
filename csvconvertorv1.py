#Import files here:
import sys
import json
import getopt
import pprint
import csv
import codecs

from rdflib import Graph, XSD, Literal, URIRef, RDF, Namespace
from urllib import parse


def csv_to_RDFTriples(infile, config):
    def form_id_triple(item,id_dict,forced_id=None):
        if id_dict.get("col"):
            _id = URIRef("{}{}".format(config["id"][id_dict["col"]],parse.quote_plus(item[id_dict["col"]])))
            print("here")
        else:
            _id = URIRef("{}{}".format(config["prefixes"][id_dict["prefix"]],parse.quote_plus(forced_id)))
        value = URIRef("{}{}".format(config["prefixes"][id_dict["type_prefix"]],parse.quote_plus(id_dict["type"])))
        return(_id, RDF.type, value)

    def form_literal_triple(_id,item,literal_dict):
        XSDliterals = {
            "XSD.string" : XSD.string,
            "XSD.integer" :XSD.integer,
            "XSD.date" : XSD.date,  
            "XSD.boolean" : XSD.boolean
        }
        predicate_term = literal_dict.get("alias") if literal_dict.get("alias") else literal_dict["col"]
        predicate = URIRef("{}{}".format(config["prefixes"][literal_dict["prefix"]],predicate_term.replace(" ","_")))
        #todo: work out how to process nulls and defaults

        if not literal_dict.get("value"):
            value = Literal(item[literal_dict["col"]], datatype = XSDliterals[literal_dict["type"]])
        else:
            value = Literal(literal_dict["value"],datatype=XSDliterals[literal_dict["type"]])

    def form_link_triple(_id,link,link_dict):
        predicate_term = link_dict.get("alias") if link_dict.get("alias") else link_dict["col"]
        predicate = URIRef("{}{}".format(config["prefixes"][link_dict["prefix"]],predicate_term.replace(" ","_")))
        link_value = URIRef("{}{}".format(config["prefixes"][link_dict["link_prefix"]],parse.quote_plus(item[link_dict["col"]])))
        return (_id,predicate,link_value)

    g = Graph()
    with open(infile, mode='r', encoding ='utf-8', errors='replace') as f:
        reader = csv.DictReader(f,delimiter = ",")
        for item in reader:
            id_triple = form_id_triple(item, config["id"])
            _id = id_triple[0]
            if not config["id"].get("create"):
                g.add(id_triple)
            for literal in config["literals"]:
                if literal.get("skip_list"):
                    if item[literal["col"]] in literal["skip_list"]:
                        continue
               # literal_triple = form_literal_triple(_id,item,literal)
               # g.add(literal_triple)

            for link in config["links"]:
                if link.get("skip_list"):
                    if item[link["col"]] in link["skip_list"]:
                        continue
            #    link_triple = form_link_triple(_id,item,link)
            #   g.add(link_triple)
    return g




#main entry point begins here
#-----------------------------------------------------------------------------------------------
def main(argv):
    try:
        opts,args = getopt.getopt(argv,"hi:o:c:", ["help","input=","output=","config="])
    except getopt.GetoptError as e:
        print(e.msg,e.opt)
        print('utils.py -i <inputfile> -o <outputfile> -c<configfile>')
        sys.exit(2)
    print(opts,args)

    infile = "input.ttl"
    outfile = "somettl.ttl"
    cfile = "sampleconfig.cfg"

    for opt ,arg in opts:
        if opt == '-h':
            print('utils.py -i <inputfile> -o <outputfile> -c <configfile>')
            sys.exit()
        elif opt in ("-i", "--input"):
                infile = arg
        elif opt in("-o", "output"):
                outfile = arg
        elif opt in ("-c", "config"):
                cfile = arg
    
    with open(cfile) as f:
        try:
            configo = json.loads(f.read())
            #print (configo)
        except:
            print("Problem parsing configuration file. Please ensure its well formed json")
            sys.exit(3)
    
    pprint.pprint(configo)
    print("Processing...")

    g1 = csv_to_RDFTriples(infile,configo)
    #print("{} statements created".forma(len(g1)))
    #print("Writing to file...")
    #g1.serialise(outfile,format="turtle")
    #print("Done!")



if __name__ == "__main__":
    main(sys.argv[1:])