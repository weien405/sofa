# Maintenance and update plan

After an authorized deployment:

1. Treat the model hash, feature order and dependency lock as a single released version.
2. Never replace the model file in place. Any model change requires a new version, complete local reproduction audit and renewed governance review.
3. Run synthetic smoke tests after every dependency or UI change.
4. Recheck anonymous desktop and mobile access after each deployment.
5. Monitor only aggregate service health. Do not log clinical inputs, prediction values, IP-linked medical entries or uploaded files.
6. Display a visible outage message if hash verification or model loading fails; never fall back to a different model.
7. Maintain a changelog containing date, commit SHA, model SHA-256, dependency changes and QA result.
8. Reassess permissions if PhysioNet terms, Streamlit hosting arrangements, institutional policies or intended use change.
9. Remove public access promptly if authorization is withdrawn or a privacy/security concern is identified.

