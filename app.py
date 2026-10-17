from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st


APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from model_backend import (  # noqa: E402
    EXPECTED_MODEL_SHA256,
    FEATURE_ORDER,
    INPUT_SCHEMA,
    InputValidationError,
    load_frozen_pipeline,
    predict_probability,
    synthetic_example,
)


st.set_page_config(
    page_title="Early SOFA-2 Trajectory Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp { background: #f5f7fa; }
    .block-container { max-width: 1240px; padding-top: 1.8rem; padding-bottom: 4rem; }
    h1, h2, h3, h4 { color: #16263b; letter-spacing: -0.02em; }
    .hero {
        padding: 1.5rem 1.65rem;
        background: linear-gradient(120deg, #14385f 0%, #1d7090 100%);
        border-radius: 18px;
        color: white;
        box-shadow: 0 10px 28px rgba(21, 57, 91, 0.16);
        margin-bottom: 1rem;
    }
    .hero h1 { color: white; font-size: 2rem; line-height: 1.18; margin: 0.18rem 0 0.45rem; }
    .hero p { color: #eaf5f8; margin: 0; font-size: 1.02rem; }
    .eyebrow { color: #a7dce8; font-size: 0.76rem; font-weight: 750; letter-spacing: 0.1em; text-transform: uppercase; }
    .scope-card, .result-card {
        background: white; border: 1px solid #dae3ec; border-radius: 15px;
        padding: 1.1rem 1.25rem; box-shadow: 0 4px 16px rgba(30, 52, 76, 0.06);
    }
    .result-card { border-left: 7px solid #16708f; }
    .probability { color: #0d5874; font-size: 2.75rem; font-weight: 780; line-height: 1.05; margin: 0.2rem 0; }
    .fine { color: #5d6a78; font-size: 0.88rem; }
    .definition { color: #637181; font-size: 0.82rem; line-height: 1.35; margin-top: -0.45rem; margin-bottom: 0.7rem; }
    div[data-testid="stForm"] { background: white; border: 1px solid #dbe3eb; border-radius: 16px; padding: 1.05rem 1.2rem; }
    div[data-testid="stMetric"] { background: white; border: 1px solid #dde5ed; border-radius: 12px; padding: 0.75rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def get_pipeline():
    return load_frozen_pipeline()


def initialize_demo_values() -> None:
    for feature, value in synthetic_example().items():
        if INPUT_SCHEMA[feature]["type"] == "binary":
            st.session_state[f"input_{feature}"] = int(value)
        else:
            st.session_state[f"input_{feature}"] = f"{value:g}"


def clear_values() -> None:
    for feature in FEATURE_ORDER:
        st.session_state.pop(f"input_{feature}", None)
    st.session_state.pop("prediction", None)


def continuous_widget(feature: str) -> str:
    spec = INPUT_SCHEMA[feature]
    note = spec.get("note", "")
    st.text_input(
        f"{spec['label']} ({spec['unit']})",
        key=f"input_{feature}",
        placeholder="Leave blank if unavailable",
        help=(
            f"{spec['window']}. Audited accepted range: {spec['minimum']:g}–"
            f"{spec['maximum']:g} {spec['unit']}. {note}"
        ).strip(),
    )
    st.markdown(
        f"<div class='definition'>{spec['window']} · valid range "
        f"{spec['minimum']:g}–{spec['maximum']:g} {spec['unit']}</div>",
        unsafe_allow_html=True,
    )
    return st.session_state.get(f"input_{feature}", "")


def binary_widget(feature: str) -> int | None:
    spec = INPUT_SCHEMA[feature]
    st.selectbox(
        spec["label"],
        options=[0, 1],
        index=None,
        key=f"input_{feature}",
        format_func=lambda value: (
            "0 — No qualifying use recorded" if value == 0 else "1 — Documented use"
        ),
        placeholder="Select one",
        help=(
            f"{spec['window']}. A value of 0 means no qualifying use was found in the audited "
            "source; it does not prove that the treatment was not given."
        ),
    )
    st.markdown(
        "<div class='definition'>0–24 h documented-event definition · 0 does not prove non-use</div>",
        unsafe_allow_html=True,
    )
    return st.session_state.get(f"input_{feature}")


try:
    pipeline = get_pipeline()
except Exception:
    st.error(
        "The verified research model is currently unavailable. No input has been stored. "
        "Public inference remains disabled pending data-governance authorization."
    )
    st.stop()

if st.query_params.get("demo") == "1" and not st.session_state.get("demo_query_loaded"):
    initialize_demo_values()
    demo_probability, demo_missing = predict_probability(pipeline, synthetic_example())
    st.session_state["prediction"] = {
        "probability": demo_probability,
        "imputed_fields": demo_missing,
    }
    st.session_state["demo_query_loaded"] = True

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Research prototype · frozen XGBoost model</div>
      <h1>Early Prediction of Unfavorable SOFA-2 Trajectories in Critically Ill Patients With Trauma</h1>
      <p>A Research Prototype Based on MIMIC-IV and eICU-CRD</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.warning(
    "Research use only. This prototype is not a clinical decision support system, does not estimate "
    "mortality, and must not be used for diagnosis, treatment selection, or autonomous patient-care decisions."
)

with st.sidebar:
    st.header("Prediction target")
    st.markdown(
        "**Unfavorable:** Persistent-high or Worsening SOFA-2 trajectory.\n\n"
        "**Other:** Low-stable or Improving SOFA-2 trajectory."
    )
    st.caption("The output is a probability of binary trajectory membership, not a four-class assignment.")
    st.divider()
    st.subheader("Frozen model")
    st.markdown("**Algorithm:** XGBoost  \n**Inputs:** 14 early variables  \n**Positive class:** 1")
    st.caption(f"Verified model SHA-256: {EXPECTED_MODEL_SHA256[:16]}…")
    st.divider()
    st.button("Load synthetic demonstration values", on_click=initialize_demo_values, width="stretch")
    st.button("Clear all inputs", on_click=clear_values, width="stretch")
    st.caption("The demonstration values are not a real patient record.")

st.subheader("Enter early ICU information")
st.caption(
    "Vital signs use the earliest valid value during 0–6 h; laboratory measurements use the earliest "
    "valid value during 0–24 h; organ-support variables describe documented use during 0–24 h."
)

with st.form("prediction_form", clear_on_submit=False):
    values: dict[str, object] = {}
    col_left, col_right = st.columns(2, gap="large")
    with col_left:
        st.markdown("#### Demographic characteristics")
        values["age"] = continuous_widget("age")

        st.markdown("#### Kidney function and support")
        values["serum_creatinine"] = continuous_widget("serum_creatinine")
        values["BUN"] = continuous_widget("BUN")
        values["RRT_any_0_24h"] = binary_widget("RRT_any_0_24h")

        st.markdown("#### Hemodynamics and respiratory support")
        values["temperature"] = continuous_widget("temperature")
        values["mean_arterial_pressure"] = continuous_widget("mean_arterial_pressure")
        values["systolic_bp"] = continuous_widget("systolic_bp")
        values["vasopressor_any_0_24h"] = binary_widget("vasopressor_any_0_24h")
        values["invasive_mechanical_ventilation_0_24h"] = binary_widget(
            "invasive_mechanical_ventilation_0_24h"
        )

    with col_right:
        st.markdown("#### Hematological and laboratory measurements")
        values["platelet_count"] = continuous_widget("platelet_count")
        values["calcium"] = continuous_widget("calcium")
        values["WBC"] = continuous_widget("WBC")
        values["glucose"] = continuous_widget("glucose")
        values["hematocrit"] = continuous_widget("hematocrit")

    submitted = st.form_submit_button("Calculate research estimate", type="primary", width="stretch")

if submitted:
    try:
        probability, imputed_fields = predict_probability(pipeline, values)
        st.session_state["prediction"] = {
            "probability": probability,
            "imputed_fields": imputed_fields,
        }
    except InputValidationError as exc:
        st.session_state.pop("prediction", None)
        st.error(str(exc))
    except Exception:
        st.session_state.pop("prediction", None)
        st.error(
            "The research prediction could not be completed. No input has been stored. "
            "Please verify the entries or contact the study team."
        )

if "prediction" in st.session_state:
    result = st.session_state["prediction"]
    probability = float(result["probability"])
    imputed_fields = list(result["imputed_fields"])

    st.divider()
    st.subheader("Research model estimate")
    st.markdown(
        f"""
        <div class="result-card">
          <div class="fine">Estimated probability of unfavorable 72-h SOFA-2 trajectory membership</div>
          <div class="probability">{probability:.3f} &nbsp; ({probability * 100:.1f}%)</div>
          <div class="fine">Unfavorable = Persistent-high or Worsening; Other = Low-stable or Improving.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if imputed_fields:
        labels = [INPUT_SCHEMA[name]["label"] for name in imputed_fields]
        st.info(
            "Unavailable continuous inputs were replaced by the corresponding medians fitted in the "
            "MIMIC-IV training set: " + ", ".join(labels) + ". These are imputed values, not measurements."
        )
    else:
        st.caption("No continuous input was missing; the frozen imputer did not replace any value.")
    st.warning(
        "No clinical risk category or treatment threshold is assigned. Do not interpret this probability "
        "as mortality risk or as a recommendation to start, withhold, or change treatment."
    )

st.divider()
st.subheader("Model performance and scope")
m1, m2 = st.columns(2, gap="large")
with m1:
    st.markdown(
        """
        <div class="scope-card">
          <b>MIMIC-IV held-out evaluation</b><br>
          N = 820; unfavorable trajectories = 125<br>
          AUROC 0.757 (95% CI 0.709–0.800)<br>
          Average precision 0.443; Brier score 0.110
        </div>
        """,
        unsafe_allow_html=True,
    )
with m2:
    st.markdown(
        """
        <div class="scope-card">
          <b>eICU-CRD cross-database evaluation</b><br>
          3,633 ICU records; 3,579 patients; 113 hospitals<br>
          AUROC 0.729 (95% CI 0.703–0.755)<br>
          Average precision 0.302; Brier score 0.096
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption(
    "These results evaluate prediction of frozen, transported trajectory labels. They do not validate the "
    "entire trajectory-discovery-plus-prediction workflow. The V2 model was developed after V1 test and "
    "eICU performance had been reviewed."
)

with st.expander("Global model interpretation from STEP22", expanded=False):
    shap_path = APP_DIR / "assets" / "MIMIC_Test_Global_SHAP_Importance.png"
    if shap_path.exists():
        st.image(str(shap_path), width="stretch")
    st.caption(
        "Global SHAP importance in the MIMIC-IV held-out set, reproduced from the completed STEP22 "
        "analysis. SHAP describes frozen-model behavior on the log-odds scale; it does not establish "
        "causal effects, treatment effects, or independent mortality associations."
    )

with st.expander("Research-use limitations and applicability", expanded=True):
    st.markdown(
        """
        - This local prototype is for research demonstration only. It is not approved for clinical diagnosis,
          treatment selection, patient triage, or autonomous decision-making.
        - The target is binary membership in a 0–72 h SOFA-2 trajectory phenotype. It is not mortality,
          survival, treatment response, or a four-class trajectory assignment.
        - Inputs end at 24 h, while the label summarizes the full 0–72 h trajectory. The output must not be
          described as predicting only newly developing deterioration after 24 h.
        - Development and evaluation were restricted to patients who later met the study's 72-h landmark
          eligibility criteria. Applicability to all patients newly admitted to an ICU has not been established.
        - Missing continuous inputs are replaced by MIMIC-IV training medians. Recording practices, missingness,
          treatment documentation, case mix, and cross-database transportability may affect predictions.
        - A value of 0 for an organ-support input means no qualifying use was recorded in the audited source;
          it does not prove that treatment was not given.
        - Decision-curve findings from STEP23 concerned hypothetical exploratory triage strategies only. No
          probability threshold has been clinically validated, and this page intentionally supplies none.
        """
    )

st.caption(
    "Local audited build · no patient records are stored by this page · the model file is loaded from a "
    "verified local path and is not included as a web upload."
)
