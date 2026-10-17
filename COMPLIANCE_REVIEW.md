# Public deployment compliance review

Review date: 17 October 2026

## Official sources reviewed

1. PhysioNet, “Guidelines for creating datasets and models from MIMIC,” published 24 April 2024: https://physionet.org/news/post/mimic-derived-datasets-models/
2. PhysioNet Credentialed Health Data License 1.5.0: https://physionet.org/about/licenses/physionet-credentialed-health-data-license-150/
3. MIMIC-IV credentialed-access project page: https://physionet.org/content/mimiciv/
4. eICU Collaborative Research Database v2.0 project page: https://physionet.org/content/eicu-crd/2.0/
5. Streamlit Community Cloud deployment documentation: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
6. Streamlit dependency documentation: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
7. PhysioNet, “Use of MIMIC Data with Large Language Models and Online Services,” updated 24 September 2025: https://physionet.org/news/post/llm-responsible-use/
8. PhysioNet contact page: https://physionet.org/about/#contact_us

## Findings

PhysioNet's 2024 MIMIC guidance states that derived datasets or models should be treated as containing sensitive information. If shared, they should be shared on PhysioNet under the same agreement as the source data. The Credentialed Health Data License also requires restricted data to be secured and prohibits sharing access to restricted data with others. MIMIC-IV and eICU-CRD are credentialed-access resources under this license.

Openly sharing analysis code is distinguishable from sharing a fitted model. The credentialed-data agreement expects publication-related code to be contributed to an open repository, whereas the 2024 guidance expressly places derived models within a sensitive-resource pathway. Therefore a public GitHub repository containing only source code, documentation, tests using synthetic data, and aggregate publication figures is a different activity from uploading the fitted pipeline.

Streamlit Community Cloud needs access to every runtime asset required by the application. Hosting the frozen pipeline in a public repository, a private repository connected to Streamlit, object storage, or another third-party service would still transfer and host the model outside PhysioNet. The official text reviewed does not expressly authorize an unrestricted public inference endpoint that loads a MIMIC-derived model while withholding the binary asset from visitors.

PhysioNet's current online-services guidance also emphasizes third-party data handling, zero retention, no model training and no human review, and advises against using a service when its practices cannot be fully verified. That page addresses online processing rather than specifically resolving public hosting of a fitted model, so it does not remove the need for written clarification.

## Decision

The model-upload and public-inference permission is **not sufficiently clear**. The formal deployment gate therefore fails at this time. No frozen model, fitted preprocessor, patient-level data, private dataset extract, or public inference endpoint has been uploaded or created.

Written confirmation should be obtained from PhysioNet/MIT-LCP. Separate approval should also be obtained from the study PI and the relevant institutional/IRB, data-governance, cybersecurity, legal or technology-transfer functions as locally required. A research disclaimer does not substitute for these permissions.

## Existing AP deployment

The previously created AP repository is public and currently contains a `model` directory and a deployed Streamlit application. It is a useful technical reference but is not evidence that the model-sharing arrangement is authorized under the 2024 PhysioNet guidance. The AP repository and application were not modified in this task. A separate governance review of that existing deployment is advisable.

## Allowed work completed now

- Audited the AP repository structure and its Streamlit workflow.
- Prepared a separate trauma code-only deployment package.
- Removed dependence on Windows absolute paths.
- Added strict model hash verification and safe production error messages.
- Excluded model binaries, patient-level data, secrets and restricted formats through `.gitignore`.
- Preserved synthetic-only automated tests and documented the already completed offline probability-reproduction audit.
- Prepared the permission inquiry and post-authorization deployment checklist.

