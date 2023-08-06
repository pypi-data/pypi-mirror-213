from ailab.atp_finetuner.model.model import AILabModel
from transformers.models import auto
from ailab.atp_finetuner.build import ModelRg
from ailab.atp_finetuner.constant import Task, Model

@ModelRg.register((Task.question_answering, Model.chatglm_6b))
class ChatGlmModel(AILabModel):
    def __init__(self, model: any) -> None:
        super().__init__(model)

    def forward(self):
        pass
    
    @classmethod
    def build_model(cls, device_name:str, model_name:str, model_dir:str, **kwargs):
        model_name_or_dir = model_name if model_dir is None else model_dir
        model = auto.AutoModel.from_pretrained(model_name_or_dir, load_in_8bit=True, trust_remote_code=True, device_map="auto")
        return cls(model)
    
    def get_inside_models(self, model_type:str):
        pass
