import numpy as np
import pickle as pkl

from make_graph import df, queue_id
from conditions import *
from cycles import detect_cycles
from k_shortest import k_shortest

'''
init_graph() initalizes graph with edge and node 
weights and stores all the conditions with penalties
'''


def init_graph(input):
    inputs = input.strip().split(',')

    # edges: add input weight from incoming edge
    # of one to outgoing edge of other
    if inputs[0] == '0':
        q1 = queue_id[inputs[1]]
        q2 = queue_id[inputs[2]]
        edges[q1 + n][q2] = float(inputs[3])

    # node: add input weight between the incoming
    # and outgoing edges of same node
    elif inputs[0] == '1':
        q = queue_id[inputs[1]]
        edges[q][q + n] = float(inputs[2])

    # conditions: store the conditions with penalties
    elif inputs[0] == '2':
        conditions.append(Conditions(inputs[1:]))


'''
opt_path_finder() function finds all the possible shortest paths
using modified dijkstra algorithm and imposes penalties according
to stored conditions and returns the final optimal path (/ cost)
'''


def opt_path_finder(source, terminal, token_id, token_amt, token_date):
    init_cost, opt_paths = k_shortest(edges, source, terminal, K=2)
    print("Possible optimal paths: ", opt_paths)

    final_cost = [0 for i in range(len(opt_paths))]

    for i, path in enumerate(opt_paths):
        penalties = [0]
        for cond in conditions:
            p = get_penalty(path, cond, token_id, token_amt, token_date)
            penalties.append(p)

        # impose the max of all the penalties that are being imposed
        final_cost[i] = init_cost[i]*(1 + max(penalties)/100)

        cycle_cost = detect_cycles(path, edges)
        final_cost[i] += np.sum(np.array(cycle_cost))

    return final_cost


'''
get_path_cost() function finds the cost of the path taking
in account the penalty imposed given a path as input
'''


def get_path_cost(path, token_id, token_amt, token_date):
    path_list = [queue_id[x] for x in path.split(":")]
    cost = 0

    for i in range(len(path_list)-1):
        n1 = path_list[i]
        n2 = path_list[i+1]
        cost += edges[n1+n][n2] + edges[n1][n1+n]

    penalties = [0]
    for cond in conditions:
        p = get_penalty(path_list, cond, token_id, token_amt, token_date)
        penalties.append(p)

    cost = cost*(1 + max(penalties)/100)
    cycle_cost = detect_cycles(path_list, edges)
    cost += np.sum(np.array(cycle_cost))

    return cost


'''
overhead_calc() function returns the overhead factor of a path
'''


def overhead_calc(path, token_id, token_amt, token_date, opt_cost):
    path_cost = get_path_cost(path, token_id, token_amt, token_date)
    overhead_factor = path_cost-opt_cost

    return overhead_factor


'''
input_format: 
type_of_input(0),node_1,node_2,weight
type_of_input(2),type_of_condition(3),compare_type(1),token_id,penalty
'''


def get_inputs():
    inputs = [
        "0,Amendment Request,Assigned Orders,4",
        "0,Amendment Request,Cancellation Request,5",
        "0,Assigned Orders,Cancellation Request,2",
        "1,Amendment Request,0",
        "1,Assigned Orders,0",
        "1,Cancellation Request,0",
        "2,1,Amendment Request:Assigned Orders,Assigned Orders,3"
    ]
    return inputs


# returns token id, token amount and token expiry date
def get_token_data():
    return "546281", 100, "10-2-2021"


# returns the path for calculating overhead factor
def get_path():
    return "Amendment Request:Assigned Orders:Cancellation Request"


if __name__ == "__main__":

    # total number of nodes (n)
    n = len(df["Queue Name"])
    source = 0
    terminal = 2 + n
    
    # load the weights corresponding to latency
    file = open('data/average_latency', 'rb')
    data = pkl.load(file)
    input_edges = data[0]

    # for every node A, we split in 2 nodes A1, A2
    # A1 has all the incoming directed edges
    # A2 has all the outgoing directed edges
    edges = np.ones((2*n, 2*n))*float('inf')

    # array to store conditions
    conditions = []

    inputs = get_inputs()
    path = get_path()
    token_id, token_amt, token_date = get_token_data()

    for input in inputs:
        init_graph(input)

    edges = np.multiply(edges, input_edges)

    opt_cost = min(opt_path_finder(source, terminal,
                   token_id, token_amt, token_date))

    print("Optimal cost: ", opt_cost)

    print("Overhead_Factor: ", overhead_calc(
        path, token_id, token_amt, token_date, opt_cost))