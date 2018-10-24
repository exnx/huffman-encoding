import heapq

# Represents a Huffman tree for use in encoding/decoding strings.
# A sample usage is as follows:
#
# h = HuffmanTree([('A', 2), ('B', 7), ('C', 1)])
# assert(h.encode('ABC') == '01100')
# assert(h.decode(h.encode('ABC')) == 'ABC')

def BinaryTreeToString(root):
    if root.symbol is not None: return root.symbol
    else: return "(%s%s)"%(BinaryTreeToString(root.left), BinaryTreeToString(root.right))


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

        '''

        This function builds a huffman tree by first creating a min heap from the symbol list,
        popping 2 elements from the heap at a time, combines
        those into one node and reinserts the new node into the heap.  It repeats
        this process until there is one remaining node, which is the root of the tree.

        '''

        symbol_hpq = self._make_heap(symbol_list)  # create a heap of the symbol list

        # keep looping until 1 node left
        while len(symbol_hpq) > 1:

            # grab the next two items from the heap, sorts by weight first
            first_tuple, second_tuple = self._get_next_two_nodes(symbol_hpq)

            new_node = self.TreeNode()  # create new node

            # isolate nodes from tuple
            left_node = first_tuple[2]  
            right_node = second_tuple[2]

            # set left and right for new node
            new_node.left = left_node  
            new_node.right = right_node
            
            # check to see which has min element (since heap prioritizes first by the weight, 
            # so could have instance where min element is different)
            if left_node.min_element < right_node.min_element:
                new_node.min_element = left_node.min_element
            else:
                new_node.min_element = right_node.min_element

            new_weight = first_tuple[0] + second_tuple[0]  # combine the weight
            new_tuple = (new_weight, new_node.min_element, new_node)   # create new tuple
            heapq.heappush(symbol_hpq, new_tuple)   # push new tuple back into heap

        # return the last node 
        return symbol_hpq[0][2]  # it's the third element in the tuple

    def _get_next_two_nodes(self, heap1):

        '''

        This function uses a second heap to retrieve the next 2 min elements from a heapq

        '''

        first_tuple = heapq.heappop(heap1)
        second_tuple = heapq.heappop(heap1)

        return (first_tuple, second_tuple)


    def _make_heap(self, symbol_list):

        '''
        
        This function creates a min heap from the symbol list.

        '''

        li = []  # start with a list
        heapq.heapify(li)  # heapify it

        # run through symbol list, create tree nodes, and add tuples to a heap
        for elem in symbol_list:
            # convert each symbol pair to a treenode

            weight = elem[1]  # grab the weight
            new_node = self.TreeNode()  # create a new treenode
            new_node.symbol = elem[0]  # set the symbol to the first element, the letter
            new_node.min_element = elem[0]  # set the min element initially to be the letter as well

            temp = (weight, new_node.min_element, new_node)  # create a temp tuple with the weight and treenode
            heapq.heappush(li, temp)  # heap push the tuple

        return li  # return the li list (heapified)

  # Encodes a string of characters into a string of bits using the
  # symbol/weight list provided.
    def encode(self, s):

        '''

        Takes a string s and encodes it into 0s and 1s based on traversing the 
        huffman tree.

        '''

        assert(s is not None)

        # if s is '', return same
        if len(s) == 0:
            return ''

        encoded_str = ''  # the return ans

        # for every char in s
        for char in s:
            char_code = ''

            # use the encode helper function
            encoded_char = self._encode_helper(self.root, char, char_code)
            encoded_str += encoded_char  # append to the running string

        return encoded_str

    def _encode_helper(self, root, char, char_code):

        '''

        A helper function that recursively traverses the huffman tree
        until it reaches a leaf node, returning the symbol value


        '''

        # if a leaf node, it will have a letter
        if root.symbol is not None:

            # if it's the right letter, return the char_code
            if root.symbol == char:
                return char_code
            # else it's not the letter, so return empty str
            else:
                return ''

        # if not a leaf node, recursively call, going both direction
        # will be empty is it doesn't find the leaf node matching the symbol
        left = self._encode_helper(root.left, char, char_code + '0')
        right = self._encode_helper(root.right, char, char_code + '1')

        return left + right  # return both, since one will be empty

    # Decodes a string of bits into a string of characters using the
    # symbol/weight list provided.
    def decode(self,encoded_msg):


        '''

        This function decodes a 0s and 1s string into letters, using a helper
        function to loop through the string, finding one letter at a time.

        '''

        assert(encoded_msg is not None)

        # if string len empty, return ''
        if len(encoded_msg) == 0:
            return ''

        msg_so_far = ''  # the starting message

        # call the helper function
        decoded_msg = self._decode_helper(self.root, encoded_msg, msg_so_far)

        return decoded_msg

    def _decode_helper(self, root, encoded_msg, msg_so_far):

        '''

        This helper function loops through the encoded message and traverses
        the tree based on a 0 or 1, going left or right, respectively.
        When it reaches a leaf node, it appends a letter, and starts the
        current root node back to the top of the tree.

        '''

        # loop through encoded 0s and 1s
        while len(encoded_msg) > 0:

            # if leaf node
            if root.symbol is not None:
                msg_so_far += root.symbol  # append to msg
                root = self.root  # restart root from the top
                continue

            next_char = encoded_msg[0]  # peek at the next char

            # if 0 or 1, go left or right
            if next_char == '0':
                root = root.left
            elif next_char == '1':
                root = root.right

            # after, remove the first letter in encoded message
            encoded_msg = encoded_msg[1:]  # update the encoded msg

        # need to do one more check after while loop
        if root.symbol is not None:
            msg_so_far += root.symbol  # append to msg
        # have leftover str so cant decode
        else:
            # the way to tell if the encoded message can't be decoded is
            # when the last letter traverses the tree and lands on a
            # non leaf node, in which case, return None
            return None

        # return the decoded message
        return msg_so_far

