# Model card: trauma SOFA-2 unfavorable-trajectory XGBoost V2

## Purpose

The frozen model estimates the probability that an adult critical-care record in the study's severe-trauma, 72-hour-landmark population belongs to either the Persistent-high or Worsening SOFA-2 trajectory group. The alternative label combines Low-stable and Improving trajectories.

This is a research phenotype-prediction model. It is not a mortality model, a diagnostic device, a treatment-effect model, or a four-class trajectory classifier.

## Frozen artifact

- Source: STEP20 expanded prediction analysis.
- Algorithm: XGBoost.
- Training records: 1,907; unfavorable trajectories: 289.
- Inputs: 14 variables in the exact order recorded in `config/input_schema.json`.
- Positive class: 1.
- SHA-256: `ef4917e9dd145e1699d2dac644798ac24fad8f2b67bc5a2fd80b2f2f12479bf1`.
- Missing continuous values: medians fitted in the MIMIC-IV training set and stored inside the frozen pipeline.
- The web application performs no fitting, selection, recalibration, or threshold optimization.

## Evaluation

MIMIC-IV held-out evaluation included 820 patients, including 125 unfavorable trajectories. AUROC was 0.757 (95% CI 0.709–0.800), average precision 0.443, and Brier score 0.110.

Cross-database evaluation used 3,633 eICU-CRD ICU records from 3,579 patients and 113 hospitals, including 436 unfavorable trajectories. AUROC was 0.729 (95% CI 0.703–0.755), average precision 0.302, and Brier score 0.096.

These results evaluate prediction of trajectory labels transported using the frozen MIMIC-IV LCMM structure. They do not constitute independent validation of the full trajectory-discovery-plus-prediction process. V2 was developed after V1 test and eICU results had been reviewed.

## Intended inputs

Age is recorded at ICU admission. Temperature, mean arterial pressure, and systolic blood pressure use the earliest valid value during 0–6 h. Platelet count, serum creatinine, blood urea nitrogen, total calcium, white blood cell count, glucose, and hematocrit use the earliest valid value during 0–24 h. Renal replacement therapy, invasive mechanical ventilation, and vasopressor inputs use documented 0–24 h events.

For the eICU-derived rule, age above 89 years was encoded as 90. A value of 90 therefore need not represent a precisely known age. Treatment value 0 means no qualifying use was found in the audited source; it does not prove non-use.

## Limitations

- Inputs extend through 24 h, while the label summarizes the entire 0–72 h trajectory.
- Development and evaluation populations were restricted to patients meeting the study's later 72-hour landmark eligibility criteria. Use in all newly admitted ICU patients is unsupported.
- Missingness and recording practices differ between hospitals and databases.
- Some predictors, including organ-support interventions and organ-function measurements, overlap conceptually with the SOFA-2 trajectory label. Their model contribution is predictive, not causal.
- External evaluation does not cover uncertainty in LCMM discovery, transported label assignment, hospital-level heterogeneity, or the complete model-development history.
- Decision-curve analysis in STEP23 represented hypothetical exploratory triage scenarios only. No probability threshold has clinical validation.

## Prohibited uses

Do not use the prototype to diagnose disease, predict death, allocate treatment, withhold treatment, rank patients for care, or make autonomous clinical decisions. Do not represent its probability as an individual confidence interval, a treatment threshold, or a causal effect.

## Governance and release status

The model is loaded only from a trusted configured path after a SHA-256 check. The application accepts no model uploads and stores no patient inputs. The model binary and fitted preprocessing object are intentionally absent from this deployment-preparation package.

Public inference is blocked pending written clarification from PhysioNet/MIT-LCP and the required institutional approvals. The code-only package must not be represented as a functioning public model service.
