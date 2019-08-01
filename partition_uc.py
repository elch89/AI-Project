import itertools
import timeit
import tracemalloc
from random import sample


def get_input():
    top_range = 50
    group = []
    print("What is the size of the universe you want to create?")
    group_size = int(input())
    if group_size >= top_range:
        print("Group size must be smaller than", top_range)
        exit(1)
    universe = list(range(1, top_range))

    not_valid = True
    num_of_tries = 0
    while not_valid:
        num_of_tries=num_of_tries+1
        group = sample(universe, group_size)
        group.sort()
        print("Created a group:\n", group)
        target = sum(group)/2
        if target % 2 != 0:
            if num_of_tries > 10:
                print("Too many tries. Aborting...")
                exit(1)
            else:
                print("sum is odd (", target, ") trying again")
        else:
            not_valid = False
    return group


def state_space(s, depth):
    """:returns list of all subsets possible (combinations) in group S
            Part of defining the search problem."""
    successor_subset = set(itertools.combinations(s, depth))
    return [list(elem) for elem in successor_subset]


def create_dictionary(subsets, group):
    """Make a dictionary from  sum of subset
        And append sum of subsets as values and elements in S as keys.
        Part of defining the search problem"""
    dcnary = {}
    for val in subsets:
        val.sort()
        for ele in val:
            if ele > sum(group) / 2:  # input element is too big
                return None
            if ele != sum(val):
                # put in dictionary only possible values smaller than target sum, reduce runtime
                if sum(val) <= sum(group) / 2:
                    dcnary.setdefault(ele, []).append(sum(val))
                else:  # Case element doesnt have matching sum - insert empty values
                    dcnary.setdefault(ele, [])
    return dcnary


class PriorityQueue(object):
    """A simple implementation Class of Priority Queue based and highest value"""
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

        # for checking if the queue is empty

    def is_empty(self):
        return len(self.queue) == 0

        # for inserting an element in the queue

    def insert(self, data):
        self.queue.append(data)

    # for popping an element based on Priority
    def pop(self):
        try:
            max_val = 0
            for i in range(len(self.queue)):
                if self.queue[i] > self.queue[max_val]:
                    max_val = i
            item = self.queue[max_val]
            del self.queue[max_val]
            return item
        except IndexError:
            print("Q empty")
            return


def uniform_cost(subset_dictionary, group_s):
    """Uniform algorithm for doing the search"""
    queue = PriorityQueue()
    # Initialize first element in queue as empty subset, path is 0
    queue.insert((0, [0]))
    # List of visited states
    visited = list()
    visited_vertex = list()
    iterations = 1
    while not queue.is_empty():
        # print("queue", queue)
        (vertex, path) = queue.pop()  # pop vertex and path from highest priority in queue

        if path not in visited:  # add to visited paths and visited vertexes
            visited.append(path)
            visited_vertex.append(vertex)
            # print("visited", visited)
        else:
            # Skip to next iteration (already visited)
            continue

        if sum(path) == sum(group_s)/2:
            # Result is found - we got the wanted group
            return path
        else:
            # Add all possible next elements to path and put in queue
            for j in group_s:
                in_dict = False
                for v in subset_dictionary[vertex]:
                    if sum(path+[j]) == v:  # Make sure the new path is in dictionary (based on sum)
                        in_dict = True
                        break

                if j != visited_vertex[-1] and j not in path and in_dict:
                    queue.insert((j, path + [j]))
        # print("iteration #:", iterations)
        iterations = iterations + 1
    return "None"


def partition_problem(group_input=None):
    print("\n===== Uniform Cost =====")
    # group_input = {9, 14, 24, 29, 37, 47}
    # group_input =set([47, 27, 3, 37, 6]) #{9, 10, 12, 19, 30}
    print("target", sum(group_input)/2)
    if group_input is None:
        group_input = set()
    subset_lists = list()
    # Get a list of all subsets that exists - 2^n subsets
    for i in range(len(group_input)):
        subset_lists.extend(state_space(group_input, i))
    # Make a dictionary out of subsets
    subset_dictionary = create_dictionary(subset_lists, list(group_input))
    if subset_dictionary is None:
        return "None"
    # initialize 0 key as list of elements in given set S
    subset_dictionary[0] = list(x for x in group_input)
    # for isd in subset_dictionary:
    #     print(isd, subset_dictionary[isd])

    # preform search on state space
    res = uniform_cost(subset_dictionary, group_input)
    if type(res) == list:
        return res[1:]

    return res


if __name__ == '__main__':
    # f = open("partitionResults.txt", "a+")
    group = get_input()
    target = sum(group)/2
    print("\nTarget sum is", target)
    tracemalloc.start()
    start = timeit.default_timer()
    uc_res = partition_problem(set(group))

    end = timeit.default_timer()
    print("result is:", uc_res)
    print("sum: ", sum(uc_res))
    print("\nRuntime: ", (end - start), "seconds")
    print("Memory usage: %d" % tracemalloc.get_tracemalloc_memory(), "Bytes")
    # if uc_res != "None":
    #     f.write("\r\nSet is: {} - length {}\r\nTarget sum: {}\r\n".format(group, len(group), target))
    #     f.write("\r\r\n==== Uniform Cost =====\r\r\n"
    #             "Runtime: {} seconds\r\nMemory usage: {} Bytes\r\n"
    #             "Result set: {}\r\n "
    #             .format((end-start), tracemalloc.get_tracemalloc_memory(), uc_res))
    tracemalloc.stop()
