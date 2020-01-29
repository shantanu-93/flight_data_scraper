import csv

def breadth_first_search(node_data_list, edge_list, weight_list, source, sink, residual_capacity):
    # Mark all the vertices as not visited 
    visited=[[] for x in range(len(node_data_list))]
    for ind,node in enumerate(node_data_list):
        visited[ind].append([False]*len(edge_list[ind]))

    queue = [] 
    queue.append(source) 
    capacity = 0
    while queue: 
        node = queue.pop(0) 
        if node == sink:
            break
        node_index = node_data_list.index(node)
        for to_in_edge in edge_list[node_index]: 
            edge_node_index = (edge_list[node_index]).index(to_in_edge)
            current_node = (visited[node_index])[0]
            if current_node[edge_node_index] == False: 
                queue.append(to_in_edge) 
                current_node[edge_node_index] = True
                capacity += int(weight_list[node_index][edge_node_index])

    return capacity, visited
  

def find_network_capacity(node_data_list, edge_list, weight_list, source, sink):
    total_capacity = 0                  
    residual_capacity = []              
    capacity_of_path, path = breadth_first_search(node_data_list, edge_list, weight_list, source, sink, residual_capacity)
    total_capacity += capacity_of_path
    v = sink
    return total_capacity


def main():
    with open(("flight_data.csv"), mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader, None)
        flight_from, flight_to, deptime, arrtime, airline, aircraft, capacity = zip(*csv_reader)
    source = 'LAX'
    sink = 'JFK'
    layover = ['SFO','SEA','PHX','DEN','ORD','ATL','IAD','BOS']
    node_data_list = []
    edge_list = []
    weight_list =[]
    edge_count = 0
    for i in range(len(flight_from)):
        edge_list_of_node = []
        weight_list_of_node = []
        if flight_from[i] == source:
            if source not in node_data_list:
                node_data_list.append(source)
                edge_list.append(["_".join([flight_from[i],deptime[i],flight_to[i],arrtime[i],airline[i]])])
                weight_list.append([capacity[i]])
            else:
                source_ind = node_data_list.index(source)
                node_data = "_".join([flight_from[i],deptime[i],flight_to[i],arrtime[i],airline[i]])
                if i>0 and (node_data == edge_list[source_ind][i-1] or node_data == (edge_list[source_ind][i-1]).rsplit("_",1)[0]):
                    node_data = node_data+"_"+str(i)
                edge_list[source_ind].append(node_data)
                weight_list[source_ind].append(capacity[i])
        node_data = "_".join([flight_from[i],deptime[i],flight_to[i],arrtime[i],airline[i]])
        if i>0 and (node_data == node_data_list[i] or node_data == (node_data_list[i]).rsplit("_",1)[0]):
            node_data = node_data+"_"+str(i)
        node_data_list.append(node_data)
        if flight_to[i] == sink:
            edge_list_of_node.append(sink)
            weight_list_of_node.append(capacity[i])
        for j,dest in enumerate(flight_to):
            if (flight_from[j] == flight_to[i] and int(deptime[j])>int(arrtime[i])):
                edge_list_of_node.append("_".join([flight_from[j],deptime[j],flight_to[j],arrtime[j],airline[j]]))
                edge_count +=1
                weight_list_of_node.append(capacity[j])
        edge_list.append(edge_list_of_node)
        weight_list.append(weight_list_of_node)
    print(find_network_capacity(node_data_list, edge_list, weight_list, source, sink))

if __name__ == "__main__":
    main()