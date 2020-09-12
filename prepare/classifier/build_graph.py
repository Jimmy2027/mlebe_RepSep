import networkx as nx
import pygraphviz as pgv  # pygraphviz should be available


def draw_training_graph():
    G = nx.DiGraph()
    G.add_edge('Volume', 'Model')
    G.add_edge('Model', 'Mask', label='Prediction')
    G.add_edge('Mask', 'Error')
    G.add_edge('Template Mask', 'Error')
    G.add_edge('Error', 'Model', label='Update')

    A = nx.drawing.nx_agraph.to_agraph(G)
    one = A.add_subgraph(rank='same')
    one.add_node('Volume',
                 label='<Volume\n\n\n<BR /> <FONT POINT-SIZE="10">\n\n\n registered by the Generic workflow</FONT>>')
    one.add_node('Model')
    one.add_node('Mask', color='springgreen3')
    two = A.add_subgraph(rank='same')
    two.add_node('Template Mask', color='springgreen3')
    two.add_node('Error', color='red2')

    A.draw('../data/training.dot', prog='dot')


def draw_workflow_graph():
    D = nx.DiGraph()
    D.add_edge('Volume', 'Classifier', label='Volume')
    D.add_edge('Volume', 'SAMRI Workflow', label='\nVolume')
    D.add_edge('Classifier', 'SAMRI Workflow', label='Mask')
    D.add_edge('SAMRI Workflow', 'Registered Volume', label='registration')

    B = nx.drawing.nx_agraph.to_agraph(D)
    one = B.add_subgraph(rank='same')
    one.add_node('Volume', label='<Volume\n\n\n<BR /> <FONT POINT-SIZE="10">\n\n\n unregistered</FONT>>')
    one.add_node('Classifier')
    one.add_node('SAMRI Workflow')
    one.add_node('Registered Volume')

    B.draw('../data/workflow.dot', prog='dot')


draw_training_graph()
draw_workflow_graph()
