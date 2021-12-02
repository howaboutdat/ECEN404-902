import mysql.connector
import haversine as hs
from pqdict import minpq
from collections import defaultdict


#establish connection to server
conn = mysql.connector.connect(host="0.tcp.ngrok.io",port ="19739", user="root", password="", database="gro_data")
if (conn):
    print("Connection successful")
else:
    print("Connection unsuccessful")

cursor = conn.cursor()



#Queue trash cans that need to be picked up based on status
cursor.execute("SELECT DISTINCT t1.* FROM loc_coordination t1 INNER JOIN loc_data t2 ON t1.ID_module = t2.ID_module AND t2.Status = '1'")
unsorted_route = cursor.fetchall()

cursor.execute("Select * from loc_data WHERE Status = '1'")
trash_table =cursor.fetchall()




def dijkstra(graph, source, target=None):
    dist = {}  # lengths of the shortest paths to each node
    pred = {}  # predecessor node in each shortest path

    # Store distance scores in a priority queue dictionary
    pq = minpq()
    for node in graph:
        if node == source:
            pq[node] = 0
        else:
            pq[node] = float('inf')

    # popitems always pops out the node with min score
    # Removing a node from pqdict is O(log n).
    for node, min_dist in pq.popitems():
        dist[node] = min_dist
        if node == target:
            break

        for neighbor in graph[node]:
            if neighbor in pq:
                new_score = dist[node] + graph[node][neighbor]
                if new_score < pq[neighbor]:
                    # Updating the score of a node is O(log n) using pqdict.
                    pq[neighbor] = new_score
                    pred[neighbor] = node

    return dist, pred






def graph_populate(unsorted_route,unsorted_graph,trash_table):
    for i in range(len(unsorted_route)):
        # use haversine formula to determine the great-circle distance between two points on a sphere given their longitudes and latitudes.
        for j in range(len(unsorted_route)):
            loc1 =(unsorted_route[i][3],unsorted_route[i][2])
            loc2 = (unsorted_route[j][3], unsorted_route[j][2])
            if trash_table[i][2] == "Full": #weighting algorithm is incoporated to calculate the most optimized route
                unsorted_graph[unsorted_route[i][0]][unsorted_route[j][0]] = (hs.haversine(loc1, loc2))*1
            elif trash_table[i][2] == "Close to Full":
                unsorted_graph[unsorted_route[i][0]][unsorted_route[j][0]] = (hs.haversine(loc1, loc2))*0.8


unsorted_graph = defaultdict(dict)

graph_populate(unsorted_route,unsorted_graph,trash_table)
print(unsorted_graph)


dist, pred = dijkstra(unsorted_graph, source='0')

cursor.execute("SELECT * from loc_coordination")
loc_coordination = cursor.fetchall()


#Print out route
for key, value in dist.items():
    cursor.execute(("INSERT INTO route_list SELECT ID_module, Longtitude, Latitude FROM loc_coordination WHERE ID_module = %s") % (key))
    conn.commit()
    print(key, end = " -> ")


