CREATE OR REPLACE VIEW `driiiportfolio.tiktok_integrity_monitoring.vw_rocc_fairness_audit` AS
WITH group_rates AS (
  SELECT
    demographic_proxy_group,
    COUNT(*) AS total_accounts,
    SUM(pipeline_enforcement_flag) AS total_enforcements,
    SAFE_DIVIDE(SUM(pipeline_enforcement_flag), COUNT(*)) AS selection_rate
  FROM
    `driiiportfolio.tiktok_integrity_monitoring.vw_rocc_pipeline_performance`
  GROUP BY
    demographic_proxy_group
)
SELECT
  g1.selection_rate AS sensitive_group_rate, -- Proxy Group 1 (Protected Class)
  g0.selection_rate AS baseline_group_rate,  -- Proxy Group 0 (Control Class)
  SAFE_DIVIDE(g1.selection_rate, g0.selection_rate) AS disparate_impact_ratio,
  0.80 AS regulatory_compliance_floor
FROM
  (SELECT selection_rate FROM group_rates WHERE demographic_proxy_group = 1) g1,
  (SELECT selection_rate FROM group_rates WHERE demographic_proxy_group = 0) g0;
