# Trauma SOFA-2 trajectory predictor — deployment preparation

This is a code-only deployment-preparation package for a Streamlit research prototype that estimates binary membership in a Persistent-high or Worsening 0–72 h SOFA-2 trajectory among critically ill adults with trauma.

Streamlit entrypoint: `app.py`.

## Current status

Public inference is **not deployed**. The frozen model is intentionally absent because PhysioNet's 24 April 2024 guidance says that models derived from MIMIC should be treated as sensitive resources and, if shared, should be shared through PhysioNet under the same agreement as the source data. Written clarification is still required for public third-party hosting and an unrestricted inference endpoint.

The public repository name proposed for later use is `trauma-sofa2-trajectory-predictor`. It was not present under the intended GitHub account when checked on 17 October 2026, but no name or Streamlit subdomain has been reserved.

## Locked model contract

- Algorithm: XGBoost within the complete STEP20 preprocessing pipeline.
- SHA-256: `ef4917e9dd145e1699d2dac644798ac24fad8f2b67bc5a2fd80b2f2f12479bf1`.
- Input order: the exact 14-variable sequence in `config/input_schema.json`.
- Positive class: Persistent-high or Worsening trajectory membership.
- The model does not estimate mortality and supplies no clinical intervention threshold.

## Package behavior

The default authorized model location is:

`model/XGBoost_FINAL_TRAINING_ONLY_PIPELINE.pkl`

An authorized local environment may instead define `SOFA2_TRAUMA_MODEL_PATH`. Before deserialization, the application verifies the exact SHA-256. Arbitrary model upload is not supported. If the model is absent, the page stops with a generic governance message and does not reveal server paths.

## Verified environment

- Python 3.12
- Streamlit 1.56.0
- pandas 3.0.6
- NumPy 2.5.1
- scikit-learn 1.9.1
- XGBoost 3.4.1

Streamlit Community Cloud currently defaults to Python 3.12, but the version must be explicitly checked in Advanced settings before an authorized deployment.

## Local code-only QA

```powershell
py -3.12 -m pip install -r requirements.txt
py -3.12 -m pip install -r requirements-dev.txt
py -3.12 -m pytest -q
```

The package deliberately excludes the model and patient-level data. Model-dependent end-to-end tests remain documented in the locked STEP24 local project and must be repeated only in an authorized environment.

## Repository structure

```text
app.py
model_backend.py
requirements.txt
.streamlit/config.toml
config/input_schema.json
config/model_manifest.json
assets/
tests/
README.md
MODEL_CARD.md
PUBLICATION_REVIEW.md
GITHUB_STREAMLIT_DEPLOY_GUIDE_CN.md
```

## Deployment gate

Do not create a public repository containing the model or expose public inference until every mandatory item in `AUTHORIZED_DEPLOYMENT_STEPS.md` is complete. A code-only repository or HOLD page must not be represented as a functioning predictor. See `COMPLIANCE_REVIEW.md`, `PUBLICATION_REVIEW.md`, `PHYSIONET_PERMISSION_INQUIRY_EMAIL.md`, and the Chinese deployment guide.

