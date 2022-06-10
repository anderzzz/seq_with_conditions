'''Bla bla

'''
from pathlib import Path
from torch.utils.data import Dataset
from Bio import SeqIO

class RNASequenceDataset(Dataset):

    def __init__(self, source_directory, file_pattern='*.gb'):
        super(RNASequenceDataset, self).__init__()

        p = Path(source_directory)
        if not p.is_dir():
            raise ValueError('File folder {} not found'.format(source_directory))

        self.file_paths = list(p.glob(file_pattern))
        self.seq_mapper = {}
        index = 0
        for ff in self.file_paths:
            records = self._read_file_(ff)
            for record in records:
                self.seq_mapper[index] = (ff, record.id)
                index += 1

        self.n_file_paths = index

    def __len__(self):
        return self.n_file_paths

    def __getitem__(self, item):
        fp, record_id = self.seq_mapper[item]
        records = self._read_file_(fp)

        counter = int(record_id.split('.')[-1])
        record = records[counter - 1]

        return record.seq.__str__(), record.id, record.name

    def _read_file_(self, fp, format_name='genbank'):
        return [record for record in SeqIO.parse(fp, format_name)]