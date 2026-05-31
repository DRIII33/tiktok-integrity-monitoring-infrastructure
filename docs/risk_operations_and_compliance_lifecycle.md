### Integrated Workflow & File Relationship Summary

 **Risk Operations & Compliance Lifecycle**. Below is the map of how the data files function as a single technical ecosystem:

#### 1. The Ingestion Layer (Raw Signal)
*   **`tiktok_phase1_pipeline_telemetry.csv`**: This is your "Ground Truth" source. It contains the raw 45,000 records of processing latencies, click-to-conversion deltas, and biometric scores.
*   **Role**: It provides the raw signals used to isolate the top 9% of high-risk traffic.

#### 2. The Normalization Layer (Detection Logic)
*   **`normalized_policy_anomalies.csv`**: Generated in Phase 2, this file takes the high-risk subset and passes it through the Python NLP pipeline.
*   **Role**: It stores the "Cleaned" versus "Raw" text, demonstrating the pipeline's ability to recover words like "whatsapp" from obfuscated strings like "Wh@tsapp".

#### 3. The Validation Layer (Statistical Proof)
*   **`phase3_validation_metrics.csv`** & **`phase3_production_validation_metrics.csv`**: These are the audit logs from your McNemar's hypothesis testing.
*   **Role**: They prove that your Phase 2 pipeline isn't just different from legacy filters, but **statistically superior**, delivering a verified +40% accuracy lift against zero-width and homoglyph attacks.

#### 4. The Governance & Equity Layer (Regulatory Compliance)
*   **`phase4_algorithmic_bias_audit.csv`**: The output of your NIST-aligned fairness audit.
*   **Role**: It mathematically verifies that your enforcement triggers do not exhibit systemic bias against demographic proxies.
*   **`TS_2026_P2_Policy_Brief.pdf`**: Your executive-ready export that translates technical data into professional policy language.

#### 5. The Enforcement Layer (Dynamic Recalibration)
*   **`phase5_recalibrated_ahr_lifecycle.csv`**: The output of the Dynamic AHR Recalibration Engine.
*   **Role**: This translates all previous signals (Unicode anomalies, velocity, and recidivism) into a final **Account Health Rating (AHR)**, categorizing merchants into automated risk tiers (Tier 1-3).

#### 6. The Advanced Data Integrity Layer (Stress Testing)
*   **`phase6_stratified_validation_metrics.csv`** & **`phase6_remediated_validation_metrics.csv`**: These files log the results of 15% network packet loss simulations and subsequent remediation attempts.
*   **Role**: They demonstrate the engine's ability to use Tiered Imputation (cohort medians and means) to recover missing data, perform Stratified McNemar Testing to verify model stability, and track the impact of architectural remediations on performance across distinct market cohorts (TikTok Shop vs. TT4B).

### Current System State: **Partial Production Approval / Ongoing Optimization**

As of May 2026, the system has achieved the following:
1.  **Ingestion**: Streaming telemetry is correctly partitioned.
2.  **Detection**: Normalization successfully neutralizes 'algospeak'.
3.  **Validation**: Model lift is statistically significant ($p < 0.05$).
4.  **Equity**: Disparate Impact Ratio (DIR) is within compliant boundaries (0.937).
5.  **Enforcement**: Merchant profiles have been dynamically recalibrated into risk tiers.
6.  **Integrity**: While architectural remediations (caching, multimodal fusion, adversarial re-weighting) stabilized the TT4B cohort's performance, the TikTok Shop (E-Comm) cohort showed a statistically significant *decrease* in accuracy (-21.57% lift) under 15% packet loss, indicating that performance restoration for this high-entropy segment remains an ongoing optimization challenge.
