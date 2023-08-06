import torch
from ailab.atp_finetuner.datacollator import AILabDataCollator
from ailab.atp_finetuner import constant
from ailab.atp_finetuner.preprossor import AILabPreprocessor
from ailab.atp_finetuner.build import DataCollatorRg
from ailab.atp_finetuner.constant import Task, Model

@DataCollatorRg.register((Task.question_answering, Model.chatglm_6b))
class ChatglmDataCollator(AILabDataCollator) :
    def __init__(self, datacollator, preprocessor):
        super().__init__(self, preprocessor)
        self.batch_size = 0

    def __call__(self , features: list)-> dict:
        tokenizer = self._preprocessor.preprocessor_ins

        len_ids = [len(feature["input_ids"]) for feature in features]
        longest = max(len_ids)
        input_ids = []
        labels_list = []
        for ids_l, feature in sorted(zip(len_ids, features), key=lambda x: -x[0]):
            ids = feature["input_ids"]
            seq_len = feature["seq_len"]
            labels = (
                [-100] * (seq_len - 1) + ids[(seq_len - 1) :] + [-100] * (longest - ids_l)
            )
            ids = ids + [tokenizer.pad_token_id] * (longest - ids_l)
            _ids = torch.LongTensor(ids)
            labels_list.append(torch.LongTensor(labels))
            input_ids.append(_ids)
        input_ids = torch.stack(input_ids)
        labels = torch.stack(labels_list)
        self.batch_size = input_ids.shape[0]
        return {
            "input_ids": input_ids,
            "labels": labels,
        }
    
    def __len__(self):
        return self.batch_size
    
    def forward(self, **kwargs):
        pass

    @classmethod
    def build_datacollator(cls, framework:constant.Framework, preprocessor:AILabPreprocessor) :
        return cls(None, preprocessor)