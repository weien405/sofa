# Security and privacy controls

- The application accepts only 14 manually entered model variables.
- It has no patient-name, medical-record-number, date-of-birth, free-text, database upload or model upload field.
- It does not persist input to a file or database.
- Server errors shown to visitors are generic and do not expose filesystem paths, stack traces, credentials or secrets.
- The model is loaded only from a configured trusted path and only after exact SHA-256 verification.
- Binary organ-support variables require explicit 0/1 selection; missing binary status is not silently treated as absence.
- Continuous missing values are handled only by the preprocessing object already fitted in the frozen pipeline.
- `.streamlit/secrets.toml`, model binaries and common restricted data formats are excluded from version control.
- No API key or credential is required by the code-only package.
- Public operation remains disabled until model-hosting permission and institutional security review are complete.

