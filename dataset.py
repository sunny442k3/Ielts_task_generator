import torch
from torch.utils.data import Dataset
from transformers import T5Tokenizer


class CustomDataset(Dataset):

    def __init__(self, dataset, max_len=128):
        super(CustomDataset, self).__init__()
        self.tokenizer = T5Tokenizer.from_pretrained("t5-base") 
        self.tokens = []
        self.labels = []
        self.build_dataset(dataset, max_len)


    def slicing_tokens(self, tokens, max_len):
        unk_ids = self.tokenizer.get_vocab()["<unk>"]
        eos_ids = self.tokenizer.get_vocab()["</s>"]
        for token in tokens:
            token = torch.tensor(token)
            data = token.unfold(0, max_len-1, 1)
            data = torch.cat((torch.tensor([unk_ids]*data.size(0)).unsqueeze(-1), data), dim=-1)[:-1]
            label = token[1:].unfold(0, max_len-1, 1)
            label = torch.cat((label, torch.tensor([eos_ids]*label.size(0)).unsqueeze(-1)), dim=-1)
            self.tokens += data.tolist()
            self.labels += label.tolist()
      

    def build_dataset(self, data, max_len):
        tokens = self.tokenizer(data, truncation=True)["input_ids"]
        self.slicing_tokens(tokens, max_len)


    def __len__(self):
        return len(self.tokens)


    def __getitem__(self, idx):
        data = torch.tensor(self.tokens[idx]).long()
        label = torch.tensor(self.labels[idx]).long()
        return data, label