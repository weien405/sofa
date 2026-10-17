# Publication and public-deployment review

Status: **HOLD — code package ready; fitted model not cleared for third-party public hosting**

## Materials suitable for the GitHub source package

- Streamlit source code and input validation logic.
- Pinned dependency and Streamlit configuration files.
- Aggregate model performance, model card and research disclaimer.
- Input definitions, units and time windows.
- Synthetic/static automated tests.
- Aggregate SHAP publication figure, subject to the study team's ordinary figure-release review.

## Materials excluded from the GitHub ZIP

- `XGBoost_FINAL_TRAINING_ONLY_PIPELINE.pkl` and every other pickle/joblib artifact.
- Fitted preprocessing objects stored separately from the pipeline.
- MIMIC-IV or eICU patient-level inputs, labels, identifiers or predictions.
- Credentials, Streamlit secrets, tokens and private local paths.

## Reason for HOLD

PhysioNet's 24 April 2024 guidance states that MIMIC-derived models should be treated as sensitive resources and, if shared, should be shared through PhysioNet under the same agreement as the source data. The reviewed official text does not clearly authorize uploading the fitted model to GitHub, a private repository connected to Streamlit, or other third-party storage to operate an unrestricted public inference endpoint.

The code-only repository may be prepared without the model, but it must not be represented as a functioning public predictor. The included application displays an explicit model-unavailable/governance message when the authorized model asset is absent and never fabricates a probability.

## Approval required before activation

1. Written PhysioNet/MIT-LCP clarification covering the proposed third-party model-hosting route and public inference interface.
2. Study PI approval.
3. Applicable institutional IRB/data-governance, privacy, cybersecurity and legal/technology-transfer approval.
4. Confirmation that the selected hosting route does not retain clinical inputs or use them for training or human review.
5. Final anonymous-access, mobile, hash, dependency and synthetic-output QA.

See `COMPLIANCE_REVIEW.md` and `PHYSIONET_PERMISSION_INQUIRY_EMAIL.md`.

