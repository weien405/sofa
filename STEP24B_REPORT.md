# STEP24B: public Streamlit deployment preparation and compliance gate

Date: 17 October 2026

## Outcome

The trauma SOFA-2 Streamlit application was converted into a production-oriented, code-only deployment package. Formal public deployment was not performed because authorization to place the MIMIC-derived frozen pipeline on third-party cloud infrastructure and expose unrestricted public inference could not be confirmed from official terms.

No STEP01–24 analysis file was changed. The STEP20 model was not retrained, recalibrated, copied into this package or uploaded. No GitHub repository or Streamlit Community Cloud application was created.

Final repository-root preparation directory:

`C:/Users/weien/Desktop/SOFA-2/STEP24B_STREAMLIT_DEPLOY_PACKAGE/`

The public-source ZIP is generated outside this directory so it cannot include itself. The ZIP contains the files in this directory at archive root, with `app.py` as the Streamlit entrypoint.

## AP reference audit

The existing AP repository and application were inspected without modification. The verified workflow uses a public GitHub repository, a root-level `streamlit_app.py`, `.streamlit/config.toml`, pinned dependencies, a bundled `model/` directory, tests and model/deployment audit documents. These engineering patterns informed the trauma package, but no AP model, variables, data or disease-specific statements were reused.

The proposed trauma repository name `trauma-sofa2-trajectory-predictor` was not found under the intended GitHub account at the time of checking. This does not reserve the repository name or a Streamlit subdomain.

## Compliance decision

PhysioNet's official 24 April 2024 guidance states that models derived from MIMIC should be treated as containing sensitive information and, if shared, should be shared on PhysioNet under the same agreement as the source data. MIMIC-IV and eICU-CRD are credentialed-access projects governed by the PhysioNet Credentialed Health Data License. The reviewed material did not expressly authorize third-party public model hosting or an unrestricted inference endpoint.

Consequently, the fitted pipeline and public inference service remain blocked pending written PhysioNet/MIT-LCP clarification and any required institutional approvals. The existing public AP deployment does not itself establish authorization and was not changed.

## Production preparation completed

- Root-level Streamlit entrypoint named `app.py`.
- Approved English title and research-use wording.
- Exact 14-variable schema, units, time windows and validation ranges.
- Exact expected model SHA-256 and class direction.
- Repository-relative default model location with optional environment override.
- No Windows absolute path in production code.
- Generic visitor-facing failure messages without server paths or raw exceptions.
- No database upload, arbitrary model upload, threshold recommendation, mortality output or four-class output.
- Runtime dependencies pinned for Python 3.12.
- Strict `.gitignore` for model binaries, secrets and common restricted-data formats.
- Synthetic/static tests, model card, input audit, security notes, release inventory and maintenance plan.

## QA

Code-only mode completed 7 tests with the model-dependent test skipped. Authorized local mode, using the original STEP20 file only through an environment variable, completed 7 tests with the compliance-hold test skipped. The full 14-field page rendered in authorized local mode.

The locked STEP24 probability-reproduction evidence remains:

- MIMIC-IV N=820: maximum absolute difference `2.6529693553101197e-08`.
- eICU-CRD N=3,633: maximum absolute difference `2.7311706563004634e-08`.

No patient-level validation data are included in this deployment-preparation folder.

## Required next action

Send the inquiry in `PHYSIONET_PERMISSION_INQUIRY_EMAIL.md`. If written authorization explicitly permits the intended model-hosting route and unrestricted public inference, complete the institutional approvals and follow `AUTHORIZED_DEPLOYMENT_STEPS.md`. Until then, do not upload the model, create a public model service or describe the trauma application as live.

