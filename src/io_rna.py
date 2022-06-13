'''Bla bla

'''
from pathlib import Path
from torch.utils.data import Dataset
from Bio import SeqIO

class NucleotideSequenceDataset(Dataset):

    def __init__(self, source_directory,
                 input_file_pattern='*.gb',
                 input_seqio_format='genbank',
                 output_record_filter_func='seq_with_id'):
        super(NucleotideSequenceDataset, self).__init__()

        p = Path(source_directory)
        if not p.is_dir():
            raise ValueError('File folder {} not found'.format(source_directory))

        self.file_paths = list(p.glob(input_file_pattern))
        self.input_seqio_format = input_seqio_format
        if output_record_filter_func == 'seq_with_id':
            self.filter_record_ = self._filter_record_seq_with_id
        elif output_record_filter_func == 'full_record':
            self.filter_record_ = lambda x: x
        elif callable(output_record_filter_func):
            self.filter_record_ = output_record_filter_func
        else:
            raise ValueError('Unknown value for record filter parameter: {}'.format(output_record_filter_func))

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
        records = self._read_file_(fp, format_name=self.input_seqio_format)

        counter = int(record_id.split('.')[-1])
        record = records[counter - 1]

        return self.filter_record_(record)

    def _read_file_(self, fp, format_name='genbank'):
        return [record for record in SeqIO.parse(fp, format_name)]

    def _filter_record_seq_with_id(self, record):
        return record.seq.__str__(), record.id, record.name