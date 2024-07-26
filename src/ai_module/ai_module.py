import pickle
from typing import List, Tuple
import json
import ast

from tqdm import tqdm
import pandas as pd
import numpy as np
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.base import BaseEstimator

from src.models.firewall_rule import FirewallRuleBaseModel
from src.common.utils import filter_dict
from src.common.config import BaseAIModelConfig
from src.ai_module.models import select_hyperparameter
from src.ai_module.utils.new_dataset import normalize
from src.models.enums import Action
from src.common.persistence import PersistableObject

class AiModule(PersistableObject):

    def __init__(self, list_models: List[Tuple[str, BaseEstimator]], config: BaseAIModelConfig, df: pd.DataFrame) -> None:
        self.config = config.model_dump()
        self.columns = df.columns
        self.list_models = list_models
        self.ensemble_model = None
    
    def create_ensemble(self, df):
        for i, tupla in enumerate(self.list_models):
            name, model = tupla
            if name == "dt":
                continue
            self.config[name][0] = filter_dict(self.config[name][0], model.__init__)
            self.list_models[i] = (name, select_hyperparameter(model, self.config[name], df))
        self.ensemble_model = VotingClassifier(estimators=self.list_models, voting='soft')
    
    def _load(self, model_bytes: bytes) -> None:
        self.ensemble_model, self.columns = pickle.loads(model_bytes)
        
    def _dump(self) -> bytes:
        return pickle.dumps([self.ensemble_model, self.columns])     

    def train(self,  df : pd.DataFrame) -> np.ndarray:
        x_train = df.drop('Label', axis=1)
        y_train = df['Label']
        self.ensemble_model.fit(x_train, y_train)
    
    def predict(self, row: pd.DataFrame) -> int:
        return self.ensemble_model.predict(row)
    
    def evaluate(self, df : pd.DataFrame) -> None:
        x_test = df.drop('Label', axis=1)
        y_test = df['Label']
        y_pred = self.ensemble_model.predict(x_test)
        print(classification_report(y_test, y_pred))
        print(confusion_matrix(y_test, y_pred))
    
    def change_model(self, file_path) -> None:
        with open(file_path, 'rb') as file:
            model_byte = file.read()
        self._load(model_byte)
    
    def save_model(self, file_path):
        model_byte = self._dump()    
        with open(file_path, 'wb') as file:
            file.write(model_byte)

    def evaluate_package(self, df: pd.DataFrame, config : dict) -> list[FirewallRuleBaseModel]:
        protocol_map = config['protocol']
        normalized_df = normalize(df.copy())
        set_rules = set()
        rules = []
        rules.append(['dst_port', 'protocol', 'fl_byt_s', 'fl_pkt_s', 'tot_fw_pk', 'tot_bw_pk', 'action'])
        with tqdm(total= len(normalized_df)) as pbar:
            for index, row in normalized_df.iterrows():
                original_row : pd.Series = df.loc[index]
                label = self.predict(row.to_frame().T)
                if label != 0:
                    set_rules.add(tuple(original_row[['Dst Port', 'Protocol', 'Flow Byts/s', 'Flow Pkts/s', 'Tot Fwd Pkts', 'Tot Bwd Pkts']].tolist()) + (Action.BLOCK,))
                pbar.update(1)
        for rule in set_rules:
            critical_rule_instance = FirewallRuleBaseModel(
                dst_port=int(rule[0]),
                protocol=protocol_map[int(rule[1])],
                min_fl_byt_s=rule[2] * 0.95,  
                max_fl_byt_s=rule[2] * 1.05,  
                min_fl_pkt_s=rule[3] * 0.95,  
                max_fl_pkt_s=rule[3] * 1.05,  
                min_tot_fw_pk=int(rule[4] * 0.95),  
                max_tot_fw_pk=int(rule[4] * 1.05),  
                min_tot_bw_pk=int(rule[5] * 0.95),  
                max_tot_bw_pk=int(rule[5] * 1.05),  
                action=rule[6]
            )
            rules.append(critical_rule_instance)
        return rules
    
