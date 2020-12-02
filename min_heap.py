# Course: CS261 - Data Structures
# Assignment: 5
# Student: Sky Jacobson
# Description: Implement the MinHeap class by completing the skeleton code provided.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initializes a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'HEAP ' + str(self.heap)

    def is_empty(self) -> bool:
        """
        Return True if no elements in the heap, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.heap.length() == 0

    def add(self, node: object) -> None:
        """
        TODO: Write this implementation
        Adds a new node to the MinHeap maintaining heap properly
        """
        # if heap is empty
        if self.is_empty():
            # append node and end method
            self.heap.append(node)
            return

        # get parent node index and value
        parent_index = int((self.heap.length() - 1) / 2)

        # append node to DynamicArray
        node_index = self.heap.length()
        self.heap.append(node)

        # percolate the node up the tree until the parent is less than node
        while self.heap[node_index] < self.heap[parent_index]:
            # swap node and parent
            self.heap.swap(parent_index, node_index)
            # update node index
            node_index = parent_index
            # update parent node and index
            parent_index = int((parent_index - 1) / 2)

    def get_min(self) -> object:
        """
        TODO: Write this implementation
        Returns an object with a minimum key without removing it from the heap. If
        the heap is empty, the method raises a MinHeapException.
        """
        # heap is empty
        if self.is_empty():
            raise MinHeapException

        # returns first node
        return self.heap[0]

    def remove_min(self) -> object:
        """
        TODO: Write this implementation
        Returns object with a minimum key and removes it from the heap. If the
        heap is empty, the method raises a MinHeapException.
        """
        # heap is empty
        if self.is_empty():
            raise MinHeapException

        # Remember value of min element
        root = self.heap[0]

        # Replace val of first element with last element, then remove last element
        last_index = self.heap.length() - 1
        self.heap.swap(0, last_index)
        self.heap.pop()

        # 3 conditions: no children, one child or two children
        # percolate root down
        i = 0
        while 2 * i + 1 < self.heap.length():
            node = self.heap[i]

            # only left child exists
            if 2 * i + 2 >= self.heap.length():
                # compare current node with left node
                if node > self.heap[2 * i + 1]:
                    # swap nodes
                    self.heap.swap(i, 2 * i + 1)
                # end of heap
                return root

            # node is larger than either child
            elif node > self.heap[2 * i + 1] or node > self.heap[2 * i + 2]:
                # swap with left child, left child is smaller than right child
                if self.heap[2 * i + 1] <= self.heap[2 * i + 2]:
                    self.heap.swap(i, 2 * i + 1)
                    i = 2 * i + 1

                # swap with right child, right child is smaller than left child
                else:
                    self.heap.swap(i, 2 * i + 2)
                    i = 2 * i + 2

            # node is smaller than children
            else:
                return root

        return root

    def build_heap_helper(self, da2: DynamicArray, i: int):
        """
        Method for percolating nodes down to build a min heap
        from an unsorted array.
        """
        left_child = 2 * i + 1  # index of left child
        right_child = 2 * i + 2  # index of right child

        if left_child >= da2.length():    # we're at a leaf node
            return

        elif right_child >= da2.length(): # no right child
            if da2[left_child] < da2[i]:  # left child is less than node
                # swap node with left child
                da2.swap(left_child, i)
                self.build_heap_helper(da2, left_child)

        # one child is less than node
        elif da2[left_child] < da2[i] or da2[right_child] < da2[i]:
            # left child is less than or equal to right child
            if da2[left_child] <= da2[right_child]:
                # swap node with left child
                da2.swap(left_child, i)
                self.build_heap_helper(da2, left_child)
            else:
                # swap with right child
                da2.swap(right_child, i)
                self.build_heap_helper(da2, right_child)

        # node is smaller than its children
        return

    def build_heap(self, da: DynamicArray) -> None:
        """
        TODO: Write this implementation
        Receives a dynamic array with objects in any order and builds a proper
        MinHeap from them. Current content of the MinHeap is lost.
        Runtime complexity must be O(n), not O(nlogn).
        """
        da2 = DynamicArray()  # create copy of argument da
        for node in da:
            da2.append(node)

        # make sure DynamicArray is a heap (start from the end)
        i = int(da2.length() / 2) - 1  # index of first non-leaf node

        while i >= 0:
            # percolate each node down
            self.build_heap_helper(da2, i)
            # increment i
            i -= 1

        # override current heap with new one
        self.heap = da2


# BASIC TESTING
if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)


    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())


    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty():
        print(h, end=' ')
        print(h.remove_min())


    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)
    da.set_at_index(0, 500)
    print(da)
    print(h)