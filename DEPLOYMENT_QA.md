# STEP24B deployment-preparation QA

## Preserved frozen-model evidence

The original STEP24 offline reproduction audit remains unchanged:

- MIMIC-IV held-out test: N=820; maximum absolute probability difference `2.6529693553101197e-08`.
- eICU-CRD external records: N=3,633; maximum absolute probability difference `2.7311706563004634e-08`.
- Both passed the prespecified `1e-6` tolerance without refitting.

These patient-level inputs and predictions are not copied into this package.

The final deployment package backend was also rerun locally against the locked STEP20/STEP21 files without refitting. It reproduced the same maximum differences. The public-safe aggregate output is saved as `DEPLOYMENT_BACKEND_CONSISTENCY.json`; the temporary local audit script and all patient-level inputs were removed before packaging.

## Code-only package checks

- Exact 14-variable order preserved.
- Positive class remains 1.
- Model hash constant preserved.
- Windows absolute model path removed.
- Arbitrary pickle upload absent.
- Public model binary absent and ignored by Git.
- Patient-level data absent and ignored by Git.
- Production errors do not reveal server paths or raw exception text.
- Title updated to the approved production wording.
- Python and package versions pinned.
- Only synthetic/static tests are included.

Automated results:

- Code-only compliance-hold mode: 7 passed, 1 authorized-runtime test skipped.
- Authorized local runtime using the original STEP20 model path: 7 passed, 1 compliance-hold test skipped.
- The authorized-runtime test confirmed the full 14-field page rendered without copying the model into this package.
- A real code-only Streamlit process started on localhost, returned HTTP 200 with `ok` from `/_stcore/health`, returned HTTP 200 from the root page, and was then stopped. Details are in `STREAMLIT_STARTUP_QA.json`.

## Deployment result

No public GitHub repository and no Streamlit Community Cloud application were created. Public model hosting and inference remain blocked pending written authorization.

