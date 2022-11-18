import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
import graph_manager as gm
from graph_manager import Node

# Load dataset
dataset = pd.read_excel('abm.xls')
X = dataset.iloc[:, [8, 9, 10]].values

# Handle empty fields in dataset.
# Consider usage of 'mean', 'median', 'most_frequent', 'constant' as the strategy
imputer = SimpleImputer(missing_values=np.nan, strategy='mean', fill_value=0)
imputer.fit(X[:, :])
X[:, :] = imputer.transform(X[:, :])

# print(X)

# Render dataset representation in Cartesian system
dataset_plot = plt.figure('Dataset representation in Cartesian system')
dataset_plot = dataset_plot.add_subplot(projection='3d')
dataset_plot.scatter(X[:, 0], X[:, 1], X[:, 2], c='b', marker='o')
dataset_plot.set_xlabel('PMNs in CSF, %')
dataset_plot.set_ylabel('Gram Smear Result')
dataset_plot.set_zlabel('Acute Bacterial Meningitis')


dataset_test = pd.read_excel('test.xls')
X_test = dataset_test.iloc[:, [1, 2]].values


graph = gm.Graph()
node_list = []

# Transform features in node representation
for i in range(X_test.shape[0]):
    node_list.append(gm.Node(X_test[i, 0], X_test[i, 1], i))

# Init graph with at least one node
if len(node_list) >= 1:
    graph.add_node(node_list[0], None, None)
    node_list.remove(node_list[0])
else:
    print('Node list is empty. Termination')
    exit(2)

# Creating graph
while node_list:
    min_dist = None
    min_node = None
    for node in node_list:
        dist = graph.get_last_node().distance_to_node(node)
        if min_dist is None or min_dist > dist:
            min_dist = dist
            min_node = node
    graph.add_node(graph.get_last_node(), min_node, min_dist)
    graph.add_node(min_node, Node(None, None, None), None)
    node_list.remove(min_node)

print(graph)
graph.generate_clusters()
graph.print_cluster_dedication()
graph.proximity_measure()
graph.distance_between_clusters()
graph.point_distribution_equability()
