# AP Streamlit deployment reference audit

Audit date: 17 October 2026

## Verified public reference

- Repository: https://github.com/weien405/sofa2-trajectory-predictor
- Application: https://sofa2-trajectory-predictor-gzhp3dybsebvv3g9lcomrr.streamlit.app/
- Repository visibility: public.
- Branch: `main`.
- Entrypoint: `streamlit_app.py`.
- Streamlit configuration: `.streamlit/config.toml`.
- Runtime model directory: `model/` beside the entrypoint.
- Anonymous HTTPS request on 17 October 2026 returned status 200 from the stated Streamlit URL.

## Verified repository structure

The repository contains `.streamlit/`, `model/`, `tests/`, `.gitignore`, `MODEL_AND_APP_AUDIT.md`, `PUBLIC_DEPLOYMENT_CHECKLIST.md`, `README.md`, `model_utils.py`, `requirements.txt`, local launch scripts and `streamlit_app.py`.

Pinned dependencies in the public AP repository are Streamlit 1.56.0, Altair 6.1.0, pandas 3.0.2, NumPy 2.4.4, scikit-learn 1.8.0, XGBoost 3.2.0 and SHAP 0.51.0.

## Elements reused conceptually

- Root-level Streamlit entrypoint.
- Root-level dependency file and `.streamlit/config.toml`.
- Clear research-only warning and target definition.
- Frozen model integrity check and automated tests.
- README, model audit and deployment checklist.

## Elements not reused

No AP model, feature list, fitted preprocessing object, patient data, threshold, result, manifest or disease-specific conclusion was copied into the trauma predictor. The trauma package uses its own 14-variable schema and its own STEP20 model hash.

## Governance note

The public AP deployment is a technical precedent only. It cannot be treated as permission for a second public MIMIC-derived model because the relevant official guidance requires a separate model-sharing assessment.

