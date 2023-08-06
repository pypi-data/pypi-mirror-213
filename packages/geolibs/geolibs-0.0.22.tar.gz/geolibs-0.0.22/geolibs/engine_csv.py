import json, copy
import numpy as np
from tqdm import tqdm

import pandas as pd 

from mmengine.registry import DATASETS
from torch.utils.data import Dataset
from typing import List, Union, Callable, Optional, Sequence

from mmengine.dataset import BaseDataset, Compose
from multiprocessing import Pool


@DATASETS.register_module()
class EngineCSV(BaseDataset):
    def __init__(self,
                 data_path: str,
                 raster_dir_path: str,
                 vector_dir_path: str,
                 split: str = "train",
                 class_title: str = None,
                 pipeline: List[Union[dict, Callable]] = [],
                 multilabel: bool = False,
                 test_mode: bool = False,
                 serialize_data: bool = True,
                 lazy_init: bool = False,
                 indices: Optional[Union[int, Sequence[int]]] = None,
                 max_refetch: int = 1000):
        self.raster_data_path = f"{data_path}/{raster_dir_path}"
        self.vector_data_path = f"{data_path}/{vector_dir_path}"

        self.split = split
        self.class_title = class_title
        self.multilabel = multilabel
        self.test_mode = test_mode
        self.serialize_data = serialize_data
        self._indices = indices

        self.pipeline = Compose(pipeline)
        self.max_refetch = max_refetch

        if not lazy_init:
            self.full_init()

    def full_init(self):
        """Load annotation file and set ``BaseDataset._fully_initialized`` to
        True."""
        super().full_init()

        #  To support the standard OpenMMLab 2.0 annotation format. Generate
        #  metainfo in internal format from standard metainfo format.
        if 'categories' in self._metainfo and 'classes' not in self._metainfo:
            categories = sorted(
                self._metainfo['categories'], key=lambda x: x['id'])
            self._metainfo['classes'] = tuple(
                [cat['category_name'] for cat in categories])
    
    def process_record(self, record):

        file_name = record["image:01"].split("/")[-1]
        file_path = f"{self.raster_data_path}/{file_name}"

        if self.multilabel:
            gt_label = []
            for x in record[self.class_title].split('\t'):
                gt_label.append(self.class_map[x])
        else:
            gt_label = self.class_map[record[self.class_title]]

        return {
            "img_path": file_path,
            "img_id": record["image-id"],
            "gt_label": gt_label
        }

    def load_data_list(self):
        meta_path = f"{self.vector_data_path}/metadata.json"
        fin = open(meta_path, "r")
        metadata = json.load(fin)
        fin.close()

        if not self.class_title:
            self.CLASSES = metadata["label:metadata"][0]["options"]
            self.class_title = metadata["label:metadata"][0]["title"].replace(" ", "-").lower()
            self.class_title_idx = 0
        else:
            for idx, question in enumerate(metadata["label:metadata"]):
                if question["title"] == self.class_title:
                    self.CLASSES = question["options"]
                    self.class_title = self.class_title.replace(" ", "-").lower()
                    self.class_title_idx = idx 

        self._metainfo = {
            "title": metadata["title"],
            "description": metadata["description"],
            "tags": metadata["tags"],
            "problemType": metadata["problemType"] if "problemType" in metadata else None,
            "question_title": metadata["label:metadata"][self.class_title_idx]["title"],
            "question_description": metadata["label:metadata"][self.class_title_idx]["description"],
            "classes": metadata["label:metadata"][self.class_title_idx]["options"]
        }

        self.class_map = {v:k for k,v in enumerate(metadata["label:metadata"][self.class_title_idx]["options"])}

        vec_path = f"{self.vector_data_path}/{metadata['dataset'][self.split]}"
        df = pd.read_csv(vec_path)
        records = df.to_dict('records')
        
        pool = Pool(16)
        data_list = list(tqdm(pool.imap(self.process_record, records), total=len(records)))
        pool.close()

        return data_list
