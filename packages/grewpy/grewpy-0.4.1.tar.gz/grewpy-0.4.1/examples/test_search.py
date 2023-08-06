import sys, os, json

sys.path.insert(0, os.path.abspath(os.path.join( os.path.dirname(__file__), "../"))) # Use local grew lib

# from grewpy import Graph, CorpusDraft, Request, Corpus, GRS, request_counter
from grewpy import Corpus, GRSDraft, Rule, Request, Commands, GRS

from grewpy import set_config
set_config("sud")

pud_file = "examples/resources/fr_pud-sud-test.conllu"
pud = Corpus(pud_file)
print(f"nb of graph in {pud_file} = {len(pud)}")


# g = pud[9]
# print(g)
# print (g.edge('8', '4'))

r = Request('e: N -[1=subj]-> M;')
print (pud.count(r))

x = Request('e: N -[subj]-> M;')
print (pud.count(x))

exit (0)

r = Request('e: N -> M; M[form="a"]')
print (r)

matchings = pud.search(r, ['e.label'])
print (json.dumps(matchings, indent=2)) 
{'1': 'nsubj'}
print ("------------------------------------------")

grs = GRS ("""
rule r { pattern { N[upos=NOUN] } commands { N.upos=N} } 
""")


# grs = GRS ("""
# rule r {
#   pattern { 
#     N -[1=nsubj]-> M
#   } 
#   without { N -[xxx]-> M }
#   commands { add_edge N -[xxx]-> M} } 
# """)

o = grs.run(pud, 'r')

print (type(o))

for sent_id, graph_list in o.items():
  print (f"{sent_id} --> {len(graph_list)}")

print ("======================================")

g = pud[9]
print (type(g))
g2 = grs.apply(g, 'Onf(r)')
print (type(o))

print (g2.edge('8', '4'))
# for sent_id get_sent_ids(o):
#   print (sent_id)
#   # print (g.to_json())
