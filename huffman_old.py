import heapq

# Represents a Huffman tree for use in encoding/decoding strings.
# A sample usage is as follows:
#
# h = HuffmanTree([('A', 2), ('B', 7), ('C', 1)])
# assert(h.encode('ABC') == '01100')
# assert(h.decode(h.encode('ABC')) == 'ABC')
class HuffmanTree:
    # Helper object for building the Huffman tree.
    # You may modify this constructor but the grading script rlies on the left, right, and symbol fields.
    class TreeNode:
        def __init__ (self):
            self.left = None
            self.right = None
            self.symbol = None
            self.min_element = None

  # The `symbol_list` argument should be a list of tuples `(symbol, weight)`,
  # where `symbol` is a symbol that can be encoded, and `weight` is the
  # the unnormalized probabilitiy of that symbol appearing.
    def __init__(self, symbol_list):
        assert(len(symbol_list) >= 2)
        # YOUR CODE HERE
        self.root = self.build_tree(symbol_list) # (place TreeNode object here)

    def build_tree(self, symbol_list):

        symbol_hpq = self._make_heap(symbol_list)

        # keep looping until 1 node left
        while len(symbol_hpq) > 1:

            first_tuple, second_tuple = self._get_next_two_nodes(symbol_hpq)

            new_node = self.TreeNode()  # create new node

            # isolate nodes from tuple
            left_node = first_tuple[1]  
            right_node = second_tuple[1]

            # set left and right for new node
            new_node.left = left_node  
            new_node.right = right_node
            
            new_node.min_element = left_node.min_element  # set min element to the left's

            new_weight = first_tuple[0] + second_tuple[0]  # combine the weight
                        
            new_tuple = (new_weight, new_node)   # create new tuple

            heapq.heappush(symbol_hpq, new_tuple)   # push new tuple back into heap

        # return the last node 
        return symbol_hpq[0][1]

    def _get_next_two_nodes(self, heap1):

        '''

        This function uses a second heap to retrieve the next 2 min elements from a heapq

        '''

        first_tuple = heapq.heappop(heap1)
        second_tuple = heapq.heappop(heap1)

        first_weight = first_tuple[0]
        second_weight = second_tuple[0]

        # if there are still items in hpq, check to see if they're the same weight as second tuple
        # of if first and second tuples have same weights, enter if
        if len(heap1) > 0 and (heap1[0][0] == second_weight or first_weight == second_weight):  

            # store in a second heap, where are the weights are the same
            # and you sort by the min element this time

            heap2 = []
            heapq.heapify(heap2)

            # grab just the node
            first_node = first_tuple[1]
            second_node = second_tuple[1]

            # create new tuple with min element and tree node
            first_heap2_tuple = (first_node.min_element, first_weight, first_node)
            second_heap2_tuple = (second_node.min_element, second_weight, second_node)

            # push the new tuple
            heapq.heappush(heap2, first_heap2_tuple)
            heapq.heappush(heap2, second_heap2_tuple)

            # loop through first heap and grab all the same weighted elements
            while len(heap1) > 0 and heap1[0][0] == second_weight:  # this peeks at the first elem weight
                heap1_tuple = heapq.heappop(heap1)  # pop from heap1
                node_weight = heap1_tuple[0]  # get node weight
                node = heap1_tuple[1]  # get node
                heap2_tuple = (node.min_element, node_weight, node)  # create heap2 tuple
                heapq.heappush(heap2, heap2_tuple)  # push to tuple to heap2

            # now grab the min 2 elements from heap2
            first_from_heap2 = heapq.heappop(heap2)
            second_from_heap2 = heapq.heappop(heap2)

            # assign the tuples for the return values
            first_tuple = (first_from_heap2[1], first_from_heap2[2])
            second_tuple = (second_from_heap2[1], second_from_heap2[2])

            # put the remaining back into the first heap hpq
            # making sure to use the original weight as first elem in tuple
            while len(heap2) > 0:
                remaining_tuple = heapq.heappop(heap2)
                remaining_node_weight = remaining_tuple[1]
                remaining_node = remaining_tuple[2]

                insert_tuple = (remaining_node_weight, remaining_node)
                heapq.heappush(heap1, insert_tuple)

            # print(heap2)

        # return the tuples (weight, node)
        return (first_tuple, second_tuple)


    def _make_heap(self, symbol_list):

        li = []
        heapq.heapify(li)

        # run through symbol list, create tree nodes, and add tuples to a heap
        for elem in symbol_list:
            # convert each symbol pair to a treenode
            new_node = self.TreeNode()
            new_node.symbol = elem[0]  # set to char
            new_node.min_element = elem[0]  # set to char

            temp = (elem[1],new_node)  # create a temp tuple with the weight and treenode
            heapq.heappush(li, temp)  # heap push the tuple

        return li

  # Encodes a string of characters into a string of bits using the
  # symbol/weight list provided.
    def encode(self, s):
        assert(s is not None)

        encoded_str = ''

        for char in s:
            char_code = ''
            encoded_char = self._encode_helper(self.root, char, char_code)
            encoded_str += encoded_char

        return encoded_str

    def _encode_helper(self, root, char, char_code):

        # if a leaf node, it will have a letter
        if root.symbol is not None:

            # if it's the right letter, return the char_code
            if root.symbol == char:
                return char_code
            # else it's not the letter, so return empty str
            else:
                return ''

        # if not a leaf node, recursively call
        left = self._encode_helper(root.left, char, char_code + '0')
        right = self._encode_helper(root.right, char, char_code + '1')

        return left + right

    # Decodes a string of bits into a string of characters using the
    # symbol/weight list provided.
    def decode(self,encoded_msg):
        assert(encoded_msg is not None)
        # YOUR CODE HERE

        msg_so_far = ''

        decoded_msg = self._decode_helper(self.root, encoded_msg, msg_so_far)

        return decoded_msg

    def _decode_helper(self, root, encoded_msg, msg_so_far):

        # if a leaf node
        if root.symbol is not None:
            msg_so_far += root.symbol
            root = self.root
  
       # not a leaf node
       # check if still have chars in encoded_msg

       # if encoded msg is not empty
        if len(encoded_msg) > 0:
        
            # get the next char
            next_char = encoded_msg[0]

            # if next_char is 0, go left
            if next_char == '0':
                msg_so_far += self._decode_helper(root.left, encoded_msg[1:], msg_so_far)
            elif next_char == '1':
                msg_so_far += self._decode_helper(root.right, encoded_msg[1:], msg_so_far)

        return msg_so_far

# testing
h = HuffmanTree([('A', 1), ('B', 1), ('C', 1)])
encoded = h.encode('ABC')
decoded = h.decode('10110')
print encoded
print decoded

