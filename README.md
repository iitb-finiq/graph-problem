# Graph Problems

## Problem Overview
- **Optimal Path Problem:** Given a workflow, find the optimal token path after modelling different types of conditional penalties on various paths.
- **Overhead Calculation:** Rank different token paths traversed by each token, compare each traverser with the model path. Compute “Overhead Factor” considering the degree of deviation, extra time taken over the model duration.
- **Loops Detection:** Given a workflow path, come up with a way to determine if there exists a loop. And if yes, also detect if the loops are repeated and accordingly increase the overall cost of the path.

## Solution Overview
### Graph Structure 
- **Nodes:** Each queue is modelled as a node. Ex: “Amendment Request” is one node.
- **Edges:** Each transition between any two queues is modelled as an edge. Ex: “Amendment Request” on success goes to “Assigned Orders”, which means there’ll be an edge between both the nodes.

Each node A in the graph is split into two nodes where one is for the incoming edges and the other for outgoing edges.

The edge between both these split nodes A1 and A2 is used to add the node cost that was imposed on A.

### Modelling Conditional Penalties
- Penalty on Segment

If a segment of nodes (ex: A→B→C→E) is present in a particular path, then increase the cost of that path by the penalty.

- Penalty on Token Amount

If the token amount > 4M (let’s say), then increase the overall cost of the path by the penalty.

### K-Shortest Algorithm
Detect the shortest path using Dijkstra's algorithm. After that, iterate over all the nodes in all the (k - 1) shortest paths and check for the possible deviation in the path. For detailed information, refer to the link below.

## File System
- `language.py`: initializes the graph based on the inputs from the user and calls the `opt_path_finder()` function to return the optimal path and also calculates overhead factor of the input path.
- `make_graph.py`: used to read the Workflow data and store the queues and transitions between different queues
- `conditions.py`: contains different types of conditions the user can use to impose penalty on the edges/ path. These are compiled inside the class `Conditions`.
- `k_shortest.py`: defines k-shortest path algorithm which returns the shortest k paths along with their lengths.
- `cycle.py`: returns different loops along with their costs present inside a path.
- `latency.py`: calculates the average latency over which a softmax function is applied to be used as a multiplier to the edge weights.

## Running Code
### Generating latency file 
First run the `format_data.py` file to generate a file that has the date in uniform format which gets saved in a `latency_formatted.xlsx` file. Now, one needs to manually sort the data in the saved excel file: apply multi-level sort first on the basis of TS_TID, then date, and finally time. Also, add a column with a header "Latency". 

Now, run the file `latency.py` which requires the name of workflow as an input (ex: bond_order_blotter). This saves the average latency weights in a pickle file named `latency.xlsx`.

### Running `language.py`
While running this file, the user needs to input the name of the workflow as an input. In addition to that, we have assumed that the user needs to define the following functions, `get_inputs()`, `get_token_data()` and `get_path()` to get the corresponding data which is hardcoded currently. 

The file outputs Possible optimal paths, Optimal cost and Overhead_Factor.

## References
- Djkstra's Algorithm: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
- K-shortest Path Algorithm: https://en.wikipedia.org/wiki/Yen%27s_algorithm
- Z-Function: https://cp-algorithms.com/string/z-function.html