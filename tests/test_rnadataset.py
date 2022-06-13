'''Bla bla

'''
from io_rna import NucleotideSequenceDataset
from torch.utils.data import DataLoader

TEST_DATA = '../test_data/'
def test_simple_read():
    data = NucleotideSequenceDataset(TEST_DATA)
    dloader = DataLoader(data)
    for dd in dloader:
        print (dd)

if __name__ == '__main__':
    test_simple_read()