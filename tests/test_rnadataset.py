'''Bla bla

'''
from io_rna import RNASequenceDataset

TEST_DATA = '../test_data/'
def test_simple_read():
    data = RNASequenceDataset(TEST_DATA)
    for dd in data:
        print (dd)

if __name__ == '__main__':
    test_simple_read()