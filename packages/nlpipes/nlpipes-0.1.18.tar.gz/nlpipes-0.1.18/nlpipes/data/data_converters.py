import json
import os
import io
import ijson
import logging
import pprint
from copy import deepcopy
from collections import defaultdict

from dataclasses import dataclass
from typing import Any, List

logger = logging.getLogger(__name__)


@dataclass
class DataConverter():
    
    def from_labelstudio(self, json_file):
        """ """
        task_iterator = self.iterate_on_tasks(json_file)
        for idx, task in enumerate(task_iterator):
            pprint.pprint(task)
            print("\n")
            
    def iterate_on_tasks(self, json_file):
            """ Iterate over the json file of tasks and extract the 
            annotation results"""
            with io.open(json_file, 'rb') as f:
                logger.debug(f'ijson backend in use: {ijson.backend}')
                tasks = ijson.items(
                    f, 'item', use_float=True
                )
                for task in tasks:
                    for annotation in self.get_annotations(task):
                        if annotation is not None:
                            yield annotation
                            
    def get_annotations(self, task):
        """ """
        has_annotations = 'annotations' in task
        
        if not has_annotations:
            logger.warning('Task do not contain annotations')
            return None
        
        annotations = task['annotations']
        
        '''
        # return task with empty annotations
        if not annotations:
            data = Converter.get_data(task, {}, {})
            yield data
        
        # skip cancelled annotations
        cancelled = lambda x: not (
            x.get('skipped', False) or x.get('was_cancelled', False)
        )
        annotations = list(filter(cancelled, annotations))
        if not annotations:
            return None

        # sort by creation time
        annotations = sorted(
            annotations, key=lambda x: x.get('created_at', 0), reverse=True
        )
        '''
        
        data = dict()
        data['text'] = None
        data['labels'] = list()
        labels = dict()
        labels['category'] = None
        labels['polarity'] = None
        labels['aspect'] = None
        labels['opinion'] = None
        
        
        for annotation in annotations:
            result = annotation['result']
            
            for r in result:
                
                if 'from_name' in r and r['from_name'] == 'Categories':
                    value = deepcopy(r['value'])
                    labels['category'] = value['taxonomy']
                    data['text'] = value['text']
                    data['labels'].append(labels)
                    yield data
                    

            #data = Converter.get_data(task, outputs, annotation)
            #data = outputs
            
            #if 'agreement' in task:
            #    data['agreement'] = task['agreement']
            
            