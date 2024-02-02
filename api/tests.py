from django.test import TestCase
import sys
# Create your tests here.
def check_for_match_in_range(round, root):
        range_len = 2**(round - 1)
        if root % range_len != 0:
            range_end = ((root // range_len) + 1) * range_len
        else:
             range_end = (root // range_len) * range_len
        range_start = (range_end - range_len) + 1
        for i in range(range_start, range_end + 1):
            print(i)
        print(list(range(range_start, range_end + 1))[int(len(range(range_start, range_end + 1)) / 2):])

check_for_match_in_range(int(sys.argv[1]), int(sys.argv[2]))
# print(sys.argv)