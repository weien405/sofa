# Restricted model asset — not included

Required frozen file after authorization:

`model/XGBoost_FINAL_TRAINING_ONLY_PIPELINE.pkl`

Required SHA-256:

`ef4917e9dd145e1699d2dac644798ac24fad8f2b67bc5a2fd80b2f2f12479bf1`

The model file is intentionally absent from this repository-ready package and ZIP. Do not rename, encode, split, compress, embed in source code or otherwise bypass the release restriction.

For an authorized local-only test, define `SOFA2_TRAUMA_MODEL_PATH` to the existing trusted STEP20 file. The application will reject any file with a different SHA-256, feature order or class order.

Streamlit Community Cloud cannot access a Windows local path. A functioning cloud predictor therefore requires a separately approved model-hosting mechanism. A private GitHub repository or private object-storage location is still third-party hosting and is not automatically authorized.

