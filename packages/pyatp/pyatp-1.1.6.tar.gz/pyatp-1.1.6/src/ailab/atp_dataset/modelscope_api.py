from typing import (Dict,  Union)
from modelscope.msdatasets import MsDataset

class MSDatasetAPI :
    def __init__(self) -> None:
        pass

    def load(dataset_name: str, namespace: str,) -> Union[dict, 'MsDataset'] :
        ms_dataset = MsDataset.load(dataset_name, namespace = namespace)
        return ms_dataset