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

        symbol_hpq = self._make_heap(symbol_list)

        # keep looping until 1 node left
        while len(symbol_hpq) > 1:

            first_tuple, second_tuple = self._get_next_two_nodes(symbol_hpq)

            # print 'first ' + first_tuple[2].min_element
            # print 'second ' + second_tuple[2].min_element

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
        return symbol_hpq[0][2]

    def _get_next_two_nodes(self, heap1):

        '''

        This function uses a second heap to retrieve the next 2 min elements from a heapq

        '''

        first_tuple = heapq.heappop(heap1)
        second_tuple = heapq.heappop(heap1)

        return (first_tuple, second_tuple)


    def _make_heap(self, symbol_list):

        li = []
        heapq.heapify(li)

        # run through symbol list, create tree nodes, and add tuples to a heap
        for elem in symbol_list:
            # convert each symbol pair to a treenode

            weight = elem[1]
            new_node = self.TreeNode()
            new_node.symbol = elem[0]
            new_node.min_element = elem[0] 

            temp = (weight, new_node.min_element, new_node)  # create a temp tuple with the weight and treenode
            heapq.heappush(li, temp)  # heap push the tuple

        return li

  # Encodes a string of characters into a string of bits using the
  # symbol/weight list provided.
    def encode(self, s):
        assert(s is not None)

        if len(s) == 0:
            return ''

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

        if len(encoded_msg) == 0:
            return ''

        msg_so_far = ''

        decoded_msg = self._decode_helper(self.root, encoded_msg, msg_so_far)

        return decoded_msg

    def _decode_helper(self, root, encoded_msg, msg_so_far):

        # print 'starting encoded msg: ' + encoded_msg

        while len(encoded_msg) > 0:

            # if leaf node
            if root.symbol is not None:
                msg_so_far += root.symbol  # append to msg
                root = self.root  # restart root from the top
                # encoded_msg = encoded_msg[1:]  # update the encoded msg
                # print 'found a leaf node, msg_so_far: ' + msg_so_far
                # print 'encoded msg inside leaf node: ' +  encoded_msg
                continue

            next_char = encoded_msg[0]

            if next_char == '0':
                root = root.left
            elif next_char == '1':
                root = root.right
            encoded_msg = encoded_msg[1:]  # update the encoded msg
            # print 'encoded msg in non leaf node: ' + encoded_msg

        # need to do one more check after while loop
        if root.symbol is not None:
            msg_so_far += root.symbol  # append to msg
        # have leftover str so cant decode
        else:
            return None

        return msg_so_far

# # testing

# a = ['j','e','F','h','Z','x','w','Y','X','q','A','i','I','l','z','O','v','o','V','G','n','E','T','B','L']
# b = [13,10,9,15,5,8,1,7,5,2,12,6,14,3,8,7,5,5,5,9,12,9,14,2,5]
# c = zip(a,b)

# a = [('A',3),('B',5),('C',2)]


# h = HuffmanTree(a)
# ans = BinaryTreeToString(h.root)
# print ans

# assert(ans=='((((EF)(G(LV)))(((XZ)e)((ov)A)))(((n(iO))(jI))((T(Y(l(q(wB)))))(h(xz)))))')
# ((((EF)(G(LV)))(((XZ)e)((ov)A)))(((n(iO))(jI))((T(Y(l(q(wB)))))(h(xz)))))
# ((((EF)(G(LV)))(((XZ)e)((ov)j)))(((An)((((Bq)(wl))i)I))(((OY)T)(h(xz)))))

# encoded = h.encode('ABC')
# decoded = h.decode('10110')
# print 'encoded msg at beginning ' + encoded
# print decoded

