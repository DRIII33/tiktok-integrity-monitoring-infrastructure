-- ===================================================================================
-- TikTok Global Operations - Trust & Safety Core Engineering
-- Component: Real-Time BI Database View Implementations (Phase 6.5)
-- Target Platform: Google BigQuery
-- Description: Transforms raw metrics into live reporting views, eliminating runtime lag.
-- ===================================================================================

-- View 1: Operational Ingestion Performance & Error Optimization Tracking
CREATE OR REPLACE VIEW `driiiportfolio.trust_and_safety.vw_rocc_pipeline_performance` AS
WITH base_metrics AS (
  SELECT
    account_id,
    platform_cohort,
    CAST(demographic_proxy_group AS INT64) AS demographic_proxy_group,
    CAST(unicode_anomalies_count AS INT64) AS unicode_anomalies_count,
    CAST(click_to_conversion_delta_t_sec AS FLOAT64) AS click_to_conversion_delta_t_sec,
    CAST(initial_ahr_score AS INT64) AS initial_ahr_score,
    CAST(recalibrated_ahr_score AS INT64) AS recalibrated_ahr_score,
    enforcement_risk_tier,
    pipeline_enforcement_flag,
    raw_unicode_telemetry,
    raw_velocity_telemetry,
    cached_unicode_telemetry,
    fused_velocity_telemetry,
    CAST(ground_truth_violation AS INT64) AS ground_truth_violation,
    CAST(optimized_pipeline_pred AS INT64) AS optimized_pipeline_pred,
    CAST(legacy_pred AS INT64) AS legacy_pred,
    TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL CAST(MOD(ABS(FARM_FINGERPRINT(account_id)), 1440) AS INT64) MINUTE) AS event_timestamp
  FROM
    `driiiportfolio.tiktok_integrity_monitoring.phase6_remediated_validation_metrics`
)
SELECT
  *,
  CASE WHEN legacy_pred = ground_truth_violation THEN 1 ELSE 0 END AS is_legacy_correct,
  CASE WHEN optimized_pipeline_pred = ground_truth_violation THEN 1 ELSE 0 END AS is_optimized_correct,
  CASE WHEN raw_unicode_telemetry IS NULL THEN 1 ELSE 0 END AS is_unicode_packet_drop,
  CASE WHEN raw_velocity_telemetry IS NULL THEN 1 ELSE 0 END AS is_velocity_packet_drop,
  CASE WHEN optimized_pipeline_pred = 1 AND ground_truth_violation = 0 THEN 1 ELSE 0 END AS is_false_positive
FROM
  base_metrics;

-- View 2: Continuous Algorithmic Fairness & Regulatory Compliance Verification
CREATE OR REPLACE VIEW `driiiportfolio.trust_and_safety.vw_rocc_fairness_audit` AS
WITH group_rates AS (
  SELECT
    demographic_proxy_group,
    COUNT(*) AS total_accounts,
    SUM(pipeline_enforcement_flag) AS total_enforcements,
    SAFE_DIVIDE(SUM(pipeline_enforcement_flag), COUNT(*)) AS selection_rate
  FROM
    `driiiportfolio.trust_and_safety.vw_rocc_pipeline_performance`
  GROUP BY
    demographic_proxy_group
)
SELECT
  g1.selection_rate AS sensitive_group_rate,
  g0.selection_rate AS baseline_group_rate,
  SAFE_DIVIDE(g1.selection_rate, g0.selection_rate) AS disparate_impact_ratio,
  0.80 AS regulatory_compliance_floor
FROM
  (SELECT selection_rate FROM group_rates WHERE demographic_proxy_group = 1) g1,
  (SELECT selection_rate FROM group_rates WHERE demographic_proxy_group = 0) g0;
