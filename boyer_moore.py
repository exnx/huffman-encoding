# Implementation of the Boyer-Moore majority vote algorithm.
#
# Given a list of elements `l`, one would use this class in the following way
# to get the element that appears the majority of the time in the list:
#

class BoyerMooreMajority:
  def __init__(self):
    self.guess = None
    self.counter = 0

  # Registers another element to be considered by the algorithm. This will
  # influence the majority element guess returned by `get_majority`.
  def add_next_element(self, element):
    assert(element is not None)

    # if counter is 0, set the guess to the element
    if self.counter == 0:
      self.guess = element

    # if counter not 0, there's a current guess, update its count
    # based on what the element is
    if element == self.guess:
      self.counter += 1  # increase if matched
    else:  # decreased if not matched
      self.counter -= 1

  # Gives the best guess of which of the elements seen so far make up the
  # majority of the elements in set of elements. If a majority element exists,
  # this algorithm will report it correctly. Otherwise, there is no guarantee
  # about the output.
  def get_majority(self):
    return self.guess  # return the current guess


# l = [2, 2, 2, 4, 5, 5, 2, 2, 3]

# b = BoyerMooreMajority()
# for elem in l:
#   b.add_next_element(elem)

# print b.get_majority()