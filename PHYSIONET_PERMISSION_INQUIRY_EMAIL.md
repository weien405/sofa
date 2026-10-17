# Permission inquiry draft

**To:** contact@physionet.org  
**Subject:** Clarification request on public inference service for a MIMIC-IV-derived research model

Dear PhysioNet Support Team,

We are preparing a research-only web application based on a fitted prediction model developed using credentialed MIMIC-IV data. The model predicts membership in an unfavorable 0–72-hour SOFA-2 trajectory among critically ill adults with trauma. The eICU Collaborative Research Database was used only for an external cross-database evaluation.

The proposed public web application would accept 14 manually entered, non-identifying early clinical variables and return only the corresponding model probability. It would not provide access to MIMIC-IV or eICU records, patient-level development data, database extracts, or individual study predictions. The application would be labelled for research use only and would not provide diagnostic, treatment or mortality recommendations.

To provide inference, however, the third-party Streamlit Community Cloud server would need to load the frozen fitted pipeline, including its preprocessing object and XGBoost model. We have reviewed PhysioNet's April 2024 “Guidelines for creating datasets and models from MIMIC,” which state that derived models should be treated as sensitive resources and, if shared, should be shared through PhysioNet under the same agreement as the source data.

Could you please clarify whether either of the following would be permitted?

1. Hosting the frozen model in a private GitHub repository or private cloud storage accessible only to Streamlit Community Cloud, while making the inference webpage publicly accessible; or
2. Hosting the model through an approved PhysioNet project with credentialed access while exposing only a public, input-to-probability inference interface.

If neither arrangement is permitted, could you advise whether public inference must be avoided entirely and whether the model may instead be distributed only as a credentialed PhysioNet resource?

No model or patient-level data will be uploaded to a third-party platform until we receive clarification. We would be happy to provide additional information about the model, inputs, security controls and intended research use.

Thank you for your guidance.

Sincerely,

En Wei, Fei Zhao, Yuanqi Gong, and Fuxing Li
The Second Affiliated Hospital of Nanchang University

