# Deployment steps after written authorization

Do not execute this checklist until written authorization explicitly covers third-party hosting of the fitted model and an unrestricted public inference endpoint.

1. Record the written PhysioNet/MIT-LCP decision and any conditions.
2. Obtain required institutional, PI, IRB/data-governance, privacy, cybersecurity and legal/technology-transfer approvals.
3. Decide the permitted model-hosting route. Do not weaken `.gitignore` or move the model until that route is approved.
4. Create the independent GitHub repository `trauma-sofa2-trajectory-predictor`; keep secrets and restricted assets out of commit history.
5. Use `app.py` as the entrypoint and Python 3.12 in Streamlit Advanced settings.
6. Verify the runtime pipeline SHA-256 equals `ef4917e9dd145e1699d2dac644798ac24fad8f2b67bc5a2fd80b2f2f12479bf1`.
7. Confirm the exact 14-feature order and class order `[0, 1]`.
8. Run synthetic-only tests locally and in the authorized cloud environment.
9. Compare the cloud output for the fixed synthetic example with its approved local expected probability; never upload the 820 MIMIC or 3,633 eICU patient-level records.
10. Check anonymous desktop and mobile access, generic failure messages, no input persistence, no file upload and no model upload.
11. Review all public text for research-only scope, landmark restriction and non-mortality target.
12. Save the commit SHA, model hash, dependency versions, cloud URL, screenshots and signed-out QA record.

