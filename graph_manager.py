import math

class Cluster:
    def __init__(self, cluster_id, num):
        self.id = cluster_id
        self.amount_of_nodes = num

    def __str__(self):
        return "Cluster " + str(self.id) + \
               " contains " + str(self.amount_of_nodes) + " nodes"

class Node:
    def __init__(self, x, y, node_id):
        self.pmn = x
        self.gsr = y
        #self.abm = z
        self.id = node_id
        self.cluster_num = None

    def distance_to_node(self, node) -> float:
        return math.sqrt(pow(node.pmn - self.pmn, 2) +
                         pow(node.gsr - self.gsr, 2))

    def __str__(self):
        return "id:{} pmn:{} gsr:{}".format(self.id, self.pmn, self.gsr)

class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.amount_of_clusters = 2
        self.max_nodes = []
        self.max_dists = []
        self.clusters = []

    def add_node(self, source, dest, dist):
        self.adjacency_list.update({source: [dest, dist]})

    def get_last_node(self):
        return list(self.adjacency_list.keys())[-1]

    def generate_clusters(self):
        max_dist = None
        max_node = None
        for key, value in self.adjacency_list.items():
            if value[1] is None:
                break
            if max_dist is None or max_dist < value[1]:
                max_dist = value[1]
                max_node = key
        print("Maximum arc distance : {}".format(max_dist))

        self.max_nodes.append(max_node)
        self.max_dists.append(max_dist)

        cluster_num = 1
        for key in self.adjacency_list.keys():
            key.cluster_num = cluster_num
            if key == max_node:
                cluster_num += 1

    def proximity_measure(self) -> float:
        proximity_list = []
        for i in range(1, (self.amount_of_clusters + 1)):
            proximity_list.append(self.proximity_in_cluster(i))
        proximity_sum = sum(proximity_list)
        ρ = proximity_sum/self.amount_of_clusters
        print("Total proximity measure: {}".format(ρ))
        return ρ

    def proximity_in_cluster(self, i) -> float:
        nodes_amount = 0
        proximity = 0
        for key, value in self.adjacency_list.items():
            if key.cluster_num == i:
                nodes_amount += 1
                if value[1] is not None:
                    proximity += value[1]

        for node in self.max_nodes:
            if node.cluster_num == i:
                proximity -= self.adjacency_list[node][1]

        c = Cluster(cluster_id=i, num=nodes_amount)
        print(c)

        self.clusters.append(c)
        print("Average proximity in cluster {} : {}"
              .format(i, proximity/nodes_amount))
        return proximity/nodes_amount

    def distance_between_clusters(self) -> float:
        distance_sum = sum(self.max_dists)
        d = distance_sum/(self.amount_of_clusters - 1)
        print("Distance between clusters: {}".format(d))
        return d

    def point_distribution_equability(self) -> float:
        for k in self.clusters:
            print(k)

        Π = 1
        for cluster in self.clusters:
            Π *= (cluster.amount_of_nodes/len(self.adjacency_list))
        h = Π * pow(self.amount_of_clusters, self.amount_of_clusters)
        print("Point distribution equability: {}".format(h))
        return h

    def print_cluster_dedication(self):
        for key in self.adjacency_list.keys():
            print("Node {} -> cluster {}".format(key.id, key.cluster_num))

    def __str__(self):
        for key, value in self.adjacency_list.items():
            print("{} -> {} : {}".format(key.id, value[0].id, value[1]))
        return "graph end"
