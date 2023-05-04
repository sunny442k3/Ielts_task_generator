import re
import nltk
import json
from torch.utils.data import Dataset


class IeltsDataset(Dataset):


    def __init__(self, data_path, tokenizer, max_length=128):
        super().__init__()
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.data = self._get_data(data_path)    


    def _clean_essay(self, text):
        sentences = nltk.sent_tokenize(text)
        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        for tokens in tokenized_sentences:
            for i, token in enumerate(tokens):
                tokens[i] = re.sub(r'\s+', ' ', token).strip()
                if i > 0 and re.match(r'[^\w\s]', token):
                    tokens[i-1] = re.sub(r'\s+', ' ', tokens[i-1]).strip()
        tokenized_sentences = [" ".join(sen) for sen in tokenized_sentences]
        return tokenized_sentences


    def _get_data(self, data_path):
        data = json.load(open(data_path, "r"))
        data = [
            self._clean_essay(par) for par in data
        ]
        
        new_data = []
        for idx, par in enumerate(data):
            par = [par[0]] + [" " + i for i in par[1:]]
            par_token = [
                self.tokenizer.tokenize(sentence) for sentence in par
            ]
            par_token = [
                token for sentence_token in par_token for token in sentence_token
            ]

            num_blocks = (len(par_token) // self.max_length)
            for i in range(num_blocks):
                st = i*self.max_length
                en = st + self.max_length
                new_data.append(self.tokenizer.convert_tokens_to_string(par_token[st:en]))
            if len(par_token) % self.max_length != 0:
                new_data.append(self.tokenizer.convert_tokens_to_string(par_token[-self.max_length:]))
        return new_data


    def __len__(self):
        return len(self.data)


    def __getitem__(self, idx):
        txt = self.data[idx]
        inputs = self.tokenizer(txt, max_length=self.max_length, padding="max_length", truncation=True, return_tensors="pt")
        inputs["labels"] = inputs["input_ids"]
        return inputs
    