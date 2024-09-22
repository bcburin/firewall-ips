from datetime import datetime
import numpy as np
from pandas.core.interchange.dataframe_protocol import DataFrame
from sqlmodel import Session
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt

from src.ai_module.ensemble import EnsembleModel
from src.common.config import DatasetConfig
from src.models.firewall_rule import FirewallRuleBaseModel
from src.ai_module.utils.new_dataset import normalize
from src.models.enums import Action
from src.services.persistence import VersionedObjectManager
from src.models.critical_rule import CriticalRuleOutModel, CriticalRule, GetAllCriticalRules
from src.models.firewall_rule import FirewallRule, FirewallRuleOutModel, GetAllFirewallRules, FirewallRuleCreateModel
from src.services.database import get_session, DBSessionManager
from src.services.executor import SSHExecutor
from src.services.firewall import IPTablesWriter
from src.common.config import ConfigurationManager
from src.services.database import InjectedSession
from src.models.variable import ConfusionMatrixInfo, Time


class EnsembleManager(VersionedObjectManager[EnsembleModel]):

    def __init__(self) -> None:
        server_config = ConfigurationManager().get_server_config()
        database_config = ConfigurationManager().get_dataset_config()
        self._classification_report: str | dict | None = None
        self._confusion_matrix: np.ndarray | None = None
        self._counter_attacktype : list[int] = ([0] * database_config.num_classes)
        self._counter_port: dict[str, int] = {}
        self._model_result_info : ConfusionMatrixInfo
        self._attack_type_map: list[str] = self.get_mapping()
        self._attack_per_minute: dict[(int, int), int] = {}
        executor = SSHExecutor(server_config.executor_credentials.ssh_host,server_config.executor_credentials.ssh_user,server_config.executor_credentials.ssh_key_path)
        self.firewall_writer = IPTablesWriter(executor, server_config.firewall_info.chain, server_config.firewall_info.table)
        super().__init__(cls=EnsembleModel)

    def get_mapping(self):
        database_config = ConfigurationManager().get_dataset_config()
        max_value = max(mapping.value for mapping in database_config.mapping)
        map_list = [None] * (max_value + 1)
        for mapping in database_config.mapping:
            value = mapping.value
            map_list[value] = mapping.type
        return map_list
    
    def _reset_cache(self):
        self._classification_report = None
        self._confusion_matrix = None
        self.rules = []

    @property
    def already_evaluated(self) -> bool:
        return self._classification_report is not None and self._confusion_matrix is not None

    def train_new_ensemble(self, df_training: DataFrame):
        with self.load_guard():
            new_ensemble = EnsembleModel()
            new_ensemble.train(df_training)
            self.load_new_version(new_ensemble)
            self._reset_cache()

    def evaluate_loaded_ensemble(self, df_test: DataFrame) -> ConfusionMatrixInfo:
        if not self.already_evaluated:
            with self.load_guard():
                ensemble: EnsembleModel = self.get_loaded_version()
                self._classification_report, self._confusion_matrix = ensemble.evaluate(df_test)
        confusion_matrix = [[str(val) for val in row] for row in self._confusion_matrix]
        precision = []
        recall = []
        f1_score = []
        for label, metrics in self._classification_report.items():
            if label not in ['accuracy', 'macro avg', 'weighted avg']:
                precision.append(metrics['precision'])
                recall.append(metrics['recall'])
                f1_score.append(metrics['f1-score'])
        accuracy = self._classification_report['accuracy']
        self._model_result_info = ConfusionMatrixInfo(
            confusion_matrix=confusion_matrix,
            precision=precision,
            recall=recall,
            f1_score=f1_score,
            accuracy=accuracy
        )

        return self._model_result_info
    
    def check_critical_rule_collision(self, rule, protocol_map):
        session: Session = DBSessionManager().get_session()
        dst_port=int(rule[0]),
        protocol=protocol_map[int(rule[1])]
        min_fl_byt_s=rule[2],
        max_fl_byt_s=rule[2] * 1.05,
        min_fl_pkt_s=rule[3] * 0.95,
        max_fl_pkt_s=rule[3] * 1.05,
        min_tot_fw_pk=int(rule[4] * 0.95),
        max_tot_fw_pk=int(rule[4] * 1.05),
        min_tot_bw_pk=int(rule[5] * 0.95),
        max_tot_bw_pk=int(rule[5] * 1.05),
        crs: list[CriticalRuleOutModel] = (session.query(CriticalRule).all())
        for critical_rule in crs:
            aux = 0
            if critical_rule.protocol != None:
                if critical_rule.protocol != protocol:
                    continue
            else:
                aux +=1
            if critical_rule.dst_port != None:
                if critical_rule.dst_port != dst_port:
                    continue
            else:
                aux +=1
            if (critical_rule.min_fl_byt_s != None and critical_rule.max_fl_byt_s != None):
                if ((min_fl_byt_s > critical_rule.max_fl_byt_s) or (max_fl_byt_s < critical_rule.min_fl_byt_s)):
                    continue
            else:
                aux +=1
            if (critical_rule.min_fl_pkt_s != None and critical_rule.max_fl_pkt_s != None):
                if ((min_fl_pkt_s > critical_rule.max_fl_pkt_s) or (max_fl_pkt_s < critical_rule.min_fl_pkt_s)):
                    continue
            else:
                aux +=1
            if (critical_rule.min_tot_fw_pk != None and critical_rule.max_tot_fw_pk != None):
                if ((min_tot_fw_pk > critical_rule.max_tot_fw_pk) or (max_tot_fw_pk < critical_rule.min_tot_fw_pk)):
                    continue
            else:
                aux +=1
            if (critical_rule.min_tot_bw_pk != None and critical_rule.max_tot_bw_pk != None):
                if ((min_tot_bw_pk > critical_rule.max_tot_bw_pk) or (max_tot_bw_pk < critical_rule.min_tot_bw_pk)):
                    continue
            else:
                aux +=1
            if aux == 6:
                continue
            return True
        return False
    
    def check_rule_collision(self, rule, protocol_map):
        session: InjectedSession = DBSessionManager().get_session()
        dst_port=int(rule[0]),
        protocol=protocol_map[int(rule[1])]
        fl_byt_s=rule[2],
        fl_pkt_s=rule[3] * 0.95,
        tot_fw_pk=int(rule[4] * 0.95),
        tot_bw_pk=int(rule[5] * 0.95),
        total_rows = session.query(FirewallRule).count()
        fwrs: list[FirewallRuleOutModel] = (session.query(FirewallRule).all())
        
        firewall_rules = GetAllFirewallRules(data=fwrs, total=total_rows)
        for firewall_rule in firewall_rules.data:
            if not (dst_port == firewall_rule.dst_port):
                continue
            if not (protocol == firewall_rule.protocol):
                continue
            if not ((abs(fl_byt_s - firewall_rule.max_fl_byt_s) - abs(fl_byt_s - firewall_rule.min_fl_byt_s)) < 0.2 * (firewall_rule.max_fl_byt_s - firewall_rule.min_fl_byt_s)):
                continue
            if not ((abs(fl_pkt_s - firewall_rule.max_fl_pkt_s) - abs(fl_pkt_s - firewall_rule.min_fl_pkt_s)) < 0.2 * (firewall_rule.max_fl_pkt_s - firewall_rule.min_fl_pkt_s)):
                continue
            if not ((abs(tot_fw_pk - firewall_rule.max_tot_fw_pk) - abs(tot_fw_pk - firewall_rule.min_tot_fw_pk)) < 0.2 * (firewall_rule.max_tot_fw_pk - firewall_rule.min_tot_fw_pk)):
                continue
            if not ((abs(tot_bw_pk - firewall_rule.max_tot_bw_pk) - abs(tot_bw_pk - firewall_rule.min_tot_bw_pk)) < 0.2 * (firewall_rule.max_tot_bw_pk - firewall_rule.min_tot_bw_pk)):
                continue   
            return True            
        return False
    
    def save_rules_in_db(self, rules: list[FirewallRuleCreateModel]):
        session = DBSessionManager().get_session()
        for rule in rules:
            CriticalRule.create_from(create_model=rule).save(session)

    def create_rules(self, df: pd.DataFrame, config : DatasetConfig):
        protocol_map = config.protocol
        session = DBSessionManager().get_session()
        ensemble : EnsembleModel = self.get_loaded_version()
        df = ensemble.filter_col(df)
        normalized_df = normalize(df.copy())
        set_rules = set()
        must_include_columns = [col.name for col in config.columns if col.must_include]
        if 'Label' in normalized_df.columns:
            normalized_df = normalized_df.drop(['Label'], axis=1)
        count = 2000
        with tqdm(total= len(normalized_df)) as pbar:
            for index, row in normalized_df.iterrows():
                original_row : pd.Series = df.loc[index]
                label = ensemble.predict(row.to_frame().T)
                if label[0] != 0:
                    rule = tuple(original_row[must_include_columns].tolist()) + (Action.BLOCK,)
                    set_rules.add(rule)
                    self._counter_attacktype[label[0]] += 1
                    if str(rule[0]) in self._counter_port:
                        self._counter_port[str(rule[0])] += 1
                    else:
                        self._counter_port[str(rule[0])] = 1
                    hour=datetime.now().hour,
                    minute=datetime.now().minute
                    if (hour,minute) in self._attack_per_minute:
                        self._attack_per_minute[(hour,minute)] += 1
                    else:
                        self._attack_per_minute[(hour,minute)] = 1
                pbar.update(1)
                count -= 1
                if count <= 0: 
                    break
        rules : list[FirewallRule] = []
        for rule in set_rules:
            firewall_rule = FirewallRule(
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
            if not self.check_critical_rule_collision(rule, protocol_map) and not self.check_rule_collision(rule, protocol_map):
                rules.append(firewall_rule)
                #self.rules.append(firewall_rule)
                #self.firewall_writer.append_rule(firewall_rule)
            
        FirewallRule.bulk_create(session=session,iterable=rules)
