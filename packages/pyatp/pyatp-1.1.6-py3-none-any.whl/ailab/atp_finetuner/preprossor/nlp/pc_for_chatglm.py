import transformers
from transformers import models
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_finetuner.build import PreProcessorRg
from ailab.atp_finetuner.constant import Task, Model
from ailab.atp_finetuner.preprossor import AILabPreprocessor

@PreProcessorRg.register((Task.question_answering, Model.chatglm_6b))
class ChatGlmPreProcessor(AILabPreprocessor):
    def __init__(self, dataset, preprocessor):
        self.config = None
        super().__init__(dataset, preprocessor)

    @classmethod
    def build_preprocessor(cls, model_name:str, dataset: AILabDataset, pc_dir:str, **kwargs):
        pc_name_dir = model_name if pc_dir is None else pc_dir
        preprocessor = models.auto.AutoTokenizer.from_pretrained(pc_name_dir, trust_remote_code=True)
        config = transformers.AutoConfig.from_pretrained(pc_name_dir, trust_remote_code=True, device_map='auto')
        chatglm_inst =  cls(dataset, preprocessor)
        chatglm_inst.config = config
        return chatglm_inst

    def process_data(self) ->AILabDataset:
        tokenizer = self._preprocessor
        config = self.config

        def preprocess(tokenizer, config, example, max_seq_length):
            prompt = example["context"]
            target = example["target"]
            prompt_ids = tokenizer.encode(prompt, max_length=max_seq_length, truncation=True)
            target_ids = tokenizer.encode(
                target,
                max_length=max_seq_length,
                truncation=True,
                add_special_tokens=False)
            input_ids = prompt_ids + target_ids + [config.eos_token_id]
            return {"input_ids": input_ids, "seq_len": len(prompt_ids)}

        def read_format_row(example, max_seq_length, skip_overlength=False):
            feature = preprocess(tokenizer, config, example, max_seq_length)
            feature["input_ids"] = feature["input_ids"][:max_seq_length]
            return feature

        def format_row(example: dict) -> dict:
            context = f"Instruction: {example['instruction']}\n"
            if example.get("input"):
                context += f"Input: {example['input']}\n"
            context += "Answer: "
            target = example["output"]
            return {"context": context, "target": target}

        def generate_and_tokenize_prompt(data_point):
            formated_row = format_row(data_point)
            dataset_row = read_format_row(formated_row, 200, True)
            return dataset_row
        tokenized_dataset = self._dataset.to_hf_dataset().map(generate_and_tokenize_prompt)
        return AILabDataset(tokenized_dataset)