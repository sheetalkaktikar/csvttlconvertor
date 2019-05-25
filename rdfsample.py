import rdflib

g=rdflib.Graph()
result = g.parse("http://www.w3.org/People/Berners-Lee/card")

print("Graph has %s statements." %len(g))

for subj,pred,obj in g:
    if (subj,pred,obj) not in g:
        raise Exception("It better be!")

s=g.serialize(format='turtle')

