
import numpy as np
import shap
from pandas.core.interchange.dataframe_protocol import DataFrame
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
from src.services.database import InjectedSession
from src.models.firewall_rule import FirewallRule, FirewallRuleOutModel, GetAllFirewallRules


class EnsembleManager(VersionedObjectManager[EnsembleModel]):

    def __init__(self) -> None:
        self._classification_report: str | dict | None = None
        self._confusion_matrix: np.ndarray | None = None
        self.rules : list[FirewallRuleBaseModel] | None = None
        super().__init__(cls=EnsembleModel)

    def _reset_cache(self):
        self._classification_report = None
        self._confusion_matrix = None
        self.rules = None

    @property
    def already_evaluated(self) -> bool:
        return self._classification_report is not None and self._confusion_matrix is not None

    def train_new_ensemble(self, df_training: DataFrame):
        with self.load_guard():
            new_ensemble = EnsembleModel()
            new_ensemble.train(df_training)
            self.load_new_version(new_ensemble)
            self._reset_cache()

    def evaluate_loaded_ensemble(self, df_test: DataFrame):
        if not self.already_evaluated:
            with self.load_guard():
                ensemble: EnsembleModel = self.get_loaded_version()
                self._classification_report, self._confusion_matrix = ensemble.evaluate(df_test)
        return self._classification_report, self._confusion_matrix
    
    def check_critical_rule_collision(rule, protocol_map):
        session: InjectedSession
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
        total_rows = session.query(CriticalRule).count()
        crs: list[CriticalRuleOutModel] = (session.query(CriticalRule).order_by(CriticalRule.id)
                                       .offset(0).limit(100).all())
        critical_rules = GetAllCriticalRules(total=total_rows, data=crs)
        colision = False
        for critical_rule in critical_rules:
            if (dst_port != critical_rule.dst_port) and critical_rule.dst_port != None:
                continue
            if (protocol != critical_rule.protocol) and critical_rule.protocol != None:
                continue
            if not (((min_fl_byt_s > critical_rule.max_fl_byt_s) and (max_fl_byt_s > min_fl_byt_s)) or (min_fl_byt_s == None and max_fl_byt_s == None)):
                continue
            if not (((min_fl_pkt_s > critical_rule.max_fl_pkt_s) and max_fl_pkt_s > min_fl_pkt_s) or (min_fl_pkt_s == None and max_fl_pkt_s == None)):
                continue
            if not (((min_tot_fw_pk > critical_rule.max_tot_fw_pk) and max_tot_fw_pk > min_tot_fw_pk) or (min_tot_fw_pk == None and max_tot_fw_pk == None)):
                continue
            if not (((min_tot_bw_pk > critical_rule.max_tot_bw_pk) and max_tot_bw_pk > min_tot_bw_pk) or (min_tot_bw_pk == None and max_tot_bw_pk == None)):
                continue
            colision = True
        return colision
    
    def check_rule_collision(rule, protocol_map):
        session: InjectedSession
        dst_port=int(rule[0]),
        protocol=protocol_map[int(rule[1])]
        fl_byt_s=rule[2],
        fl_pkt_s=rule[3] * 0.95,
        tot_fw_pk=int(rule[4] * 0.95),
        tot_bw_pk=int(rule[5] * 0.95),
        total_rows = session.query(CriticalRule).count()
        fwrs: list[FirewallRuleOutModel] = (session.query(FirewallRule).order_by(FirewallRule.id)
                                       .offset(0).limit(1000).all())
        GetAllFirewallRules(data=fwrs, total=total_rows)
        firewall_rules = GetAllCriticalRules(total=total_rows, data=fwrs)
        colision = False
        for firewall_rule in firewall_rules:
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
            colision = True             
        return colision


    def create_static_rules(self, df: pd.DataFrame, config : DatasetConfig):
        protocol_map = config.protocol
        ensemble = self.get_loaded_version()
        normalized_df = normalize(df.copy())
        set_rules = set()
        with tqdm(total= len(normalized_df)) as pbar:
            for index, row in normalized_df.iterrows():
                original_row : pd.Series = df.loc[index]
                label = ensemble.predict(row.to_frame().T)
                if label != 0:
                    set_rules.add(tuple(original_row[config['rule_variables']].tolist()) + (Action.BLOCK,))
                pbar.update(1)
        for rule in set_rules:
            static_rule = FirewallRuleBaseModel(
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
                self.rules.append(static_rule)
        
    def create_dynamic_rules(self, package: pd.Series, config):
        protocol_map = config['protocol']
        ensemble = self.get_loaded_version()
        normalized_package = normalize(package.copy())
        label = ensemble.predict(normalized_package.to_frame().T)
        if label != 0:
            rule = tuple(package[config['rule_variables']].tolist()) + (Action.BLOCK,)
            dynamic_rule = FirewallRuleBaseModel(
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
            self.rules.append(dynamic_rule)
        

    
    def save_shap_plots(self, shap_values, class_index, class_name, model_name):
        # Bar plot
        shap.plots.bar(shap_values[:, :, class_index], show = False)
        plt.savefig(f"src/ai_module/plots/{model_name}/{model_name}_{class_name}_feature_importance.png", bbox_inches='tight')
        plt.close()

        # Beeswarm plot
        shap.plots.beeswarm(shap_values[:, :, class_index], show = False)
        plt.savefig(f"src/ai_module/plots/{model_name}/{model_name}_{class_name}_shap.png", bbox_inches='tight')
        plt.close()

    def shap_metrics(self, df_train: pd.DataFrame, df_test: pd.DataFrame, model_name):
        X_train = df_train.drop('Label', axis=1)
        X_test = df_test.drop('Label', axis=1)
        X_sub = shap.sample(X_train, 1000)
        explainer = shap.Explainer(self.ensemble_model.predict_proba, X_sub)
        shap_values = explainer(X_test[0:2000])
        self.save_shap_plots(shap_values, 0, "allow", model_name)
        self.save_shap_plots(shap_values, 1, "bruteforce", model_name)
        self.save_shap_plots(shap_values, 2, "web", model_name)
        self.save_shap_plots(shap_values, 3, "DOS", model_name)
        self.save_shap_plots(shap_values, 4, "DDOS", model_name)
        self.save_shap_plots(shap_values, 5, "botnet", model_name)