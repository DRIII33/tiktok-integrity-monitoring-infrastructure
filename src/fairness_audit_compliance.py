"""
TikTok Global Operations - Trust & Safety Engineering
Component: Algorithmic Fairness Audit & Bias Invariant Validation Engine (Phase 4)
Description: Evaluates automated enforcement ratios against the EEOC Four-Fifths compliance rule.
"""

import pandas as pd
import numpy as np

class ComplianceEquityAuditor:
    def __init__(self, compliance_floor: float = 0.80):
        self.compliance_floor = compliance_floor

    def execute_fairness_audit(self, df: pd.DataFrame, proxy_col: str, action_col: str) -> dict:
        """Calculates selection metrics and checks for demographic bias across groups."""
        summary_stats = df.groupby(proxy_col)[action_col].agg(['count', 'sum']).reset_index()
        summary_stats['selection_rate'] = summary_stats['sum'] / summary_stats['count']
        
        try:
            base_rate = summary_stats.loc[summary_stats[proxy_col] == 0, 'selection_rate'].values[0]
            sensitive_rate = summary_stats.loc[summary_stats[proxy_col] == 1, 'selection_rate'].values[0]
        except IndexError:
            raise ValueError("Data frame must contain both Group 0 (Control) and Group 1 (Protected) proxy markers.")
            
        if sensitive_rate > base_rate and base_rate > 0:
            disparate_impact_ratio = base_rate / sensitive_rate
        elif base_rate > 0:
            disparate_impact_ratio = sensitive_rate / base_rate
        else:
            disparate_impact_ratio = 1.0

        is_compliant = disparate_impact_ratio >= self.compliance_floor
        
        return {
            'control_group_selection_rate': float(base_rate),
            'protected_group_selection_rate': float(sensitive_rate),
            'disparate_impact_ratio': float(disparate_impact_ratio),
            'regulatory_compliance_status': "COMPLIANT" if is_compliant else "NON-COMPLIANT_BREACH"
        }

if __name__ == "__main__":
    np.random.seed(42)
    sim_audit_data = pd.DataFrame({
        'demographic_proxy_group': [0]*100 + [1]*100,
        'pipeline_enforcement_flag': list(np.random.choice([0, 1], size=100, p=[0.7, 0.3])) + 
                                     list(np.random.choice([0, 1], size=100, p=[0.68, 0.32]))
    })
    auditor = ComplianceEquityAuditor()
    audit_results = auditor.execute_fairness_audit(sim_audit_data, 'demographic_proxy_group', 'pipeline_enforcement_flag')
    print("Fairness Audit Output Matrix Summary:")
    for metric, val in audit_results.items():
        print(f"  {metric}: {val}")
