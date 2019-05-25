import csv
from rdflib import URIRef, BNode, Literal, Namespace,Graph
from rdflib.namespace import RDF


csvfile = 'testadd.csv'
ttlfile = 'testoutput.ttl'

ifile = open(csvfile,'r')
reader = csv.reader(ifile)

ofile = open(ttlfile,'wb')

g=Graph()

rootns = Namespace("http://wwww.testproj.com/RFirms")
NSkey = Namespace("http://testproj.com/CustID")
AttribNS = Namespace("http://testproj.com/terms")
PropNS_1 = Namespace("http://testproj.com/terms/HouseNumber")
PropNS_2 = Namespace("http://testproj.com/terms/Street")
PropNS_3 = Namespace("http://testproj.com/terms/City")
PropNS_4 = Namespace("http://testproj.com/terms/State")
PropNS_5 = Namespace("http://testproj.com/terms/Postcode")

rownum = 0
for row in reader:
    if rownum == 0 :
        pass
    else: 
        id = row[1]
        council = URIRef(n+)
        g.add((council, RDF.type, pol.Council))
        g.add((council, core.preferredLabel, Literal(row[2])))
        g.add((council, core.sameAs,URIRef(row[3])))
    rownum+=1

d = g.serialize(format='turtle')
ofile.write(d)

ofile.close()
ifile.close()


