# Course: CS261 - Data Structures
# Assignment: 5
# Student: Sky Jacobson
# Description: Implement the Hash Map class.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        TODO: Write this implementation
        Clears the content of the hash map. Does not change capacity.
        """
        # Loop through DynamicArray and reset each bucket
        for index in range(self.buckets.length()):
            self.buckets.set_at_index(index, LinkedList())
        # reset size to 0
        self.size = 0

    def get(self, key: str) -> object:
        """
        TODO: Write this implementation
        Returns the value associated with the given key.
        If the key is not in the hash map, the method returns None.
        """
        index = self.hash_function(key) % self.capacity     # get index of LinkedList
        value = self.buckets[index].contains(key)           # find node with key
        if value is not None:                               # if node existed
            return value.value
        else:
            return value                                    # value should be None

    def put(self, key: str, value: object) -> None:
        """
        TODO: Write this implementation
        Updates the key / value pair in the hash map.
        If key exists in hash map, value should be replaced with new value.
        If key not in hash map, key / value pair should be added.
        """
        # find bucket to modify
        hash_index = self.hash_function(key) % self.capacity
        bucket = self.buckets.get_at_index(hash_index)

        # find key in bucket
        # bucket found then modify node
        if bucket.contains(key) is not None:
            node = bucket.contains(key)
            node.value = value
        # bucket not found then add node
        # and increment size
        else:
            bucket.insert(key, value)
            self.size += 1

    def remove(self, key: str) -> None:
        """
        TODO: Write this implementation
        Removes the given key and its associated value from the hash map.
        If key is not in hash map, the method does nothing.
        """
        index = self.hash_function(key) % self.capacity     # find index of key
        removed = self.buckets[index].remove(key)           # remove value
        if removed is True:                                 # if value is removed then increment size
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        TODO: Write this implementation
        Returns True if the given key is in the hash map, otherwise it returns False.
        An empty hash map does not contain any keys.
        """
        if self.capacity == 0:                          # edge case capacity is 0
            return False

        index = self.hash_function(key) % self.capacity # find index of would be key
        node = self.buckets[index].contains(key)        # find node with key
        if node is not None:                            # found node with key
            return True
        return False                                    # key not in HashMap

    def empty_buckets(self) -> int:
        """
        TODO: Write this implementation
        Returns the number of empty buckets in the hash table.
        """
        count = 0
        # loop through each bucket
        for bucket in self.buckets:
            # if bucket is empty then increment count
            if bucket.length() == 0:
                count += 1
        return count

    def table_load(self) -> float:
        """
        TODO: Write this implementation
        Returns the current hash table load factor
        # load factor: 𝝺=n/m (average number of elements in each bucket)
        n = number of elements
        m = number of buckets
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        TODO: Write this implementation
        Changes the capacity of hash table.
        All existing key / value pairs remain in new hash map and all hash table links rehashed.
        """
        # If new_capacity is less than 1, this method should do nothing.
        if new_capacity < 1:
            return

        reassigned_buckets = DynamicArray()                         # create new hash table
        for _ in range(new_capacity):
            reassigned_buckets.append(LinkedList())

        self.capacity = new_capacity                                # reassign capacity

        for bucket in self.buckets:                                 # loop through current hash table
            # if bucket.length() > 0:
            for node in bucket:                                     # get key of nodes in each LinkedList
                key = node.key
                index = self.hash_function(key) % self.capacity     # assign new index for key using hash function
                reassigned_buckets[index].insert(key, node.value)   # reassign node to its new LinkedList

        self.buckets = reassigned_buckets   # reassign HashMap


    def get_keys(self) -> DynamicArray:
        """
        TODO: Write this implementation
        Returns a DynamicArray that contains all keys stored in your hash map.
        Order of the keys in the DA does not matter.
        """
        result = DynamicArray()              # create a DynamicArray

        for bucket in self.buckets:          # loop through buckets
            for node in bucket:              # add every key in each bucket to result
                result.append(node.key)

        return result


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
