import pandas as pd # for data manipulation
import networkx as nx # for drawing graphs
import matplotlib.pyplot as plt # for drawing graphs

# for creating Bayesian Belief Networks (BBN)
from pybbn.graph.dag import Bbn
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.jointree import EvidenceBuilder
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable
from pybbn.pptc.inferencecontroller import InferenceController


def getcode(p):
    if p[0:3].isnumeric():
        return int(p[0:3])
    return 0

def prop_cat(propcode):
    code = getcode(propcode)
    if code >= 100 and code < 200:
        return "Assembly"
    elif code >= 200 and code < 300:
        return "Educational"
    elif code >= 300 and code < 400:
        return "HCDC"
    elif code >= 400 and code < 500:
        return "Residential"
    elif code >= 500 and code < 600:
        return "Mercantile"
    elif code >= 600 and code < 700:
        return "Industrial"
    elif code >= 700 and code < 800:
        return "Manufacturing"
    elif code >= 800 and code < 900:
        return "Storage"
    elif code >= 900 and code < 1000:
        return "Special"
    elif code == 000:
        return "Other"
    return "None"

def incid_cat(incidcode):
    code = getcode(incidcode)
    if code >= 100 and code < 200:
        return "Fire"
    elif code >= 200 and code < 300:
        return "Rupture"
    elif code >= 300 and code < 400:
        return "Rescue"
    elif code >= 400 and code < 500:
        return "Hazardous"
    elif code >= 500 and code < 600:
        return "Service"
    elif code >= 600 and code < 700:
        return "Good Intent"
    elif code >= 700 and code < 800:
        return "False Alarm"
    elif code >= 800 and code < 900:
        return "Natural Disaster"
    elif code >= 900 and code < 1000:
        return "Special"
    elif code == 000:
        return "Other"
    return "None"

pd.options.display.max_columns = 15
df = pd.read_csv('../data/IncidentData.csv')

df = df[pd.isnull(df['PropCode']) == False]
df = df[pd.isnull(df['IncidentCode']) == False]

# Create bands for variables that we want to use in the model
df['PropCode'] = df['PropCode'].apply(lambda x: prop_cat(x))
df['IncidentCode'] = df['IncidentCode'].apply(lambda x: incid_cat(x))



# # Create nodes by manually typing in probabilities
PropCode = BbnNode(Variable(0, 'Prop', ['Assembly', 'Educational', 'HCDC', 'Residential', 'Mercantile', 'Industrial', 'Manufacturing', 'Storage', 'Special', 'Other', 'None']),
                   [0.1, 0.2, .05, .1, .2, .05, .025, .025, .05, .15, .05])
Incid = BbnNode(Variable(1, 'Incid', ['Yes', 'No']), [.2, .8,
                                                  .4, .6,
                                                  .1, .9,
                                                  .3, .7,
                                                  .4, .6,
                                                  .75, .25,
                                                  .05, .95,
                                                  .3, .7,
                                                  .65, .35,
                                                  .7, .3,
                                                  .45, .55])

# Create Network
bbn = Bbn() \
    .add_node(PropCode) \
    .add_node(Incid) \
    .add_edge(Edge(PropCode, Incid, EdgeType.DIRECTED))

# # Convert the BBN to a join tree
join_tree = InferenceController.apply(bbn)

# Set node positions
pos = {0: (-1, 2), 1: (0, -1)}

# Set options for graph looks
options = {
    "font_size": 16,
    "node_size": 4000,
    "node_color": "white",
    "edgecolors": "black",
    "edge_color": "red",
    "linewidths": 5,
    "width": 5, }

# Generate graph
n, d = bbn.to_nx_graph()
nx.draw(n, with_labels=True, labels=d, pos=pos, **options)

# Update margins and print the graph
ax = plt.gca()
ax.margins(0.10)
plt.axis("off")
plt.show()

def evidence(ev, node, cat, val):
    ev = EvidenceBuilder() \
    .with_node(join_tree.get_bbn_node_by_name(node)) \
    .with_evidence(cat, val) \
    .build()
    join_tree.set_observation(ev)

def print_probs():
    for node in join_tree.get_bbn_nodes():
        potential = join_tree.get_bbn_potential(node)
        print("Node:", node)
        print("Values:")
        print(potential)
        print('----------------')

#Print Probs
print("BEFORE")
print_probs()

print("")
print("")
print("")

print("")
print("")

print("AFTER")
evidence('', 'Prop', 'Special', 1.0)

print_probs()

