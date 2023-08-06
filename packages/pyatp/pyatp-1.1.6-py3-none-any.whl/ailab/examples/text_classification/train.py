import os
from ailab.atp_dataset.dataset import AILabDataset
from ailab.atp_dataset.constant import Sources
from ailab.atp_finetuner.constant import Task, Framework
from ailab.atp_finetuner.finetuner import AILabFinetuner

def train_progress(percent:float):
    pass

def text_classfication_test():
        model_name = os.environ.get("MODEL_NAME")
        dataset_path = os.environ.get("DATASET_PATH")
        output_dir = os.environ.get("OUTPUT_DIR","./my_text_model")
        model_path = os.environ.get("MODEL_PATH")
        tokenizer_path = os.environ.get("TOKENIZER_PATH")

        if not model_name or not dataset_path or not model_path or not tokenizer_path:
            raise TypeError(f'os.environ should have (MODEL_NAME,DATASET_PATH,MODEL_PATH,TOKENIZER_PATH)')
        
        dataset = AILabDataset.load_dataset(dataset_path, src=Sources.huggingface)
        dataset.train_test_split(test_size=0.2)
        args = {
                "model_args" : {
                        "num_labels":3,
                        "id2label":{0: "NEGATIVE", 1: "NEUTRAL", 2: "POSITIVE"},
                        "label2id":{"NEGATIVE": 0, "NEUTRAL": 1, "POSITIVE":2}
                },
                "train_args" : {
                        "output_dir":output_dir, 
                        "evaluation_strategy":"epoch",
                        "save_strategy":"epoch",
                        "learning_rate":2e-5,
                        "per_device_train_batch_size":16,
                        "gradient_accumulation_steps":4,
                        "per_device_eval_batch_size":16,
                        "num_train_epochs":2,
                        "weight_decay":0.01,
                        "logging_steps":10,
                        "warmup_steps":100,
                        "fp16":True,
                        "optim":"adamw_torch",
                        "eval_steps":200,
                        "save_steps":200,
                        "max_steps":5000,
                        "resume_from_checkpoint":True,
                },
                }
        finetuner = AILabFinetuner(Task.text_classification, Framework.Pytorch, dataset, \
                                   model_name, train_progress, 
                                   model_path,
                                   tokenizer_path,
                                   **args)
        finetuner.finetuner()

if __name__ == '__main__' :
    text_classfication_test()