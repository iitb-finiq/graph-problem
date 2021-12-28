import datetime
from make_graph import df, queue_id

# total number of nodes (n)
n = len(df["Queue Name"])

'''
Conditions specify different types of conditions
the user can use to impose penalty on the edges/ path
'''


class Conditions:
    def __init__(self, inputs):

        self.type = inputs[0]
        self.penalty = float(inputs[-1])

        # segment of nodes match
        # Ex: A->B->C should be inside the path
        if self.type == '0':
            self.segement = []
            for x in inputs[1].split(":"):
                self.segement += [queue_id[x], queue_id[x] + n]
            # self.segement=self.segement[::-1]

        # segment of node given a single node
        # Ex: A->B->C given D should be inside the path
        elif self.type == '1':
            self.segement = []
            for x in inputs[1].split(":"):
                self.segement += [queue_id[x], queue_id[x] + n]
            # self.segement=self.segement[::-1]
            self.conditional_node = queue_id[inputs[2]]

        # given start, end and set of nodes
        # Ex: path should start from A to T and has nodes C, D
        elif self.type == '2':
            self.start = queue_id[inputs[1]]
            self.end = queue_id[inputs[2]] + n
            self.set_nodes = [queue_id[x] for x in inputs[3].split(",")]

        # token id match
        # Ex: token id should start with/ end with/ fully match
        elif self.type == '3':
            self.token_type = inputs[1]
            self.token_id = inputs[2]

        # token amount match
        # Ex: token amount should be greater than/ less than/ equal to
        elif self.type == '4':
            self.compare_type = inputs[1]
            self.token_amt = inputs[2]

        # token date match
        # Ex: token date should be greater than/ less than/ equal to
        elif self.type == '5':
            self.compare_type = inputs[1]
            self.token_date = inputs[2]


'''
get_penalty() function calculates if the penalty 
should be imposed based on condition or not
returns penalty that should be imposed, else 0
'''


def get_penalty(path, cond, token_id, token_amt, token_date):
    # segment of nodes match
    if cond.type == '0':
        if check_subpath(path, cond.segement):
            return cond.penalty

    # segment of node given a single node
    elif cond.type == '1':
        if cond.conditional_node in cond.segement and check_subpath(path, cond.segement):
            return cond.penalty

    # given start, end and set of nodes
    elif cond.type == '2':
        print(cond.set_nodes, path, cond.start, cond.end)
        if path[0] == cond.start and path[-1] == cond.end and is_subset(cond.set_nodes, path):
            return cond.penalty

    # token id match (start with/ end with/ fully match)
    elif cond.type == '3':
        if cond.token_type == '0' and token_id.startswith(cond.token_id):
            return cond.penalty
        if cond.token_type == '1' and token_id.endswith(cond.token_id):
            return cond.penalty
        if cond.token_type == '2' and token_id == cond.token_id:
            return cond.penalty

    # token amount match (greater than/ less than/ equal to)
    elif cond.type == '4':
        if cond.compare_type == '0' and token_amt > cond.token_amt:
            return cond.penalty
        if cond.compare_type == '1' and token_amt == cond.token_amt:
            return cond.penalty
        if cond.compare_type == '2' and token_amt < cond.token_amt:
            return cond.penalty

    # token date match (greater than/ less than/ equal to)
    elif cond.type == '5':
        date = cond.token_date.split("-")
        token_dates = token_date.split("-")

        d1 = datetime.datetime(date[2], date[1], date[0])
        d2 = datetime.datetime(token_dates[2], token_dates[1], token_dates[0])

        if cond.compare_type == '0' and d2 > d1:
            return cond.penalty
        if cond.compare_type == '1' and d2 == d1:
            return cond.penalty
        if cond.compare_type == '2' and d2 < d1:
            return cond.penalty

    return 0


# helper function
# returns true if x is a subset of y


def is_subset(x, y):
    it = iter(y)
    return all(any(c == ch for c in it) for ch in x)


# helper function
# returns true if segment is present in path

def check_subpath(path, segment):
    def z_function(path):
        n = int(len(path))
        z = [0 for i in range(n)]
        l = 0
        r = 0
        for i in range(1, n):
            if (i <= r):
                z[i] = min(r - i + 1, z[i - l])
            while (i + z[i] < n and path[z[i]] == path[i + z[i]]):
                z[i] += 1
            if (i + z[i] - 1 > r):
                l = i
                r = i + z[i] - 1
        return z

    temp = segment.copy()
    temp.append(float('-inf'))
    temp += path
    vec = z_function(temp)
    for ele in vec:
        if ele == len(segment):
            return True
    return False
