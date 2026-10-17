from __future__ import annotations

import hashlib
import os
import pickle
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import pandas as pd


APP_DIR = Path(__file__).resolve().parent
DEFAULT_MODEL_PATH = APP_DIR / "model" / "XGBoost_FINAL_TRAINING_ONLY_PIPELINE.pkl"
MODEL_PATH_ENV = "SOFA2_TRAUMA_MODEL_PATH"
EXPECTED_MODEL_SHA256 = "ef4917e9dd145e1699d2dac644798ac24fad8f2b67bc5a2fd80b2f2f12479bf1"

FEATURE_ORDER = [
    "platelet_count",
    "RRT_any_0_24h",
    "serum_creatinine",
    "BUN",
    "invasive_mechanical_ventilation_0_24h",
    "calcium",
    "vasopressor_any_0_24h",
    "WBC",
    "temperature",
    "age",
    "mean_arterial_pressure",
    "systolic_bp",
    "glucose",
    "hematocrit",
]

INPUT_SCHEMA: dict[str, dict[str, Any]] = {
    "platelet_count": {
        "label": "Platelet count",
        "type": "continuous",
        "unit": "×10⁹/L",
        "minimum": 1.0,
        "maximum": 999.0,
        "step": 1.0,
        "window": "Earliest valid value during 0–24 h",
        "group": "Hematological and laboratory measurements",
    },
    "RRT_any_0_24h": {
        "label": "Renal replacement therapy",
        "type": "binary",
        "unit": "0/1",
        "window": "Documented use during 0–24 h",
        "group": "Kidney function and support",
    },
    "serum_creatinine": {
        "label": "Serum creatinine",
        "type": "continuous",
        "unit": "mg/dL",
        "minimum": 0.1,
        "maximum": 11.23,
        "step": 0.1,
        "window": "Earliest valid value during 0–24 h",
        "group": "Kidney function and support",
    },
    "BUN": {
        "label": "Blood urea nitrogen",
        "type": "continuous",
        "unit": "mg/dL",
        "minimum": 1.0,
        "maximum": 300.0,
        "step": 1.0,
        "window": "Earliest valid value during 0–24 h",
        "group": "Kidney function and support",
    },
    "invasive_mechanical_ventilation_0_24h": {
        "label": "Invasive mechanical ventilation",
        "type": "binary",
        "unit": "0/1",
        "window": "Documented use during 0–24 h",
        "group": "Hemodynamics and respiratory support",
    },
    "calcium": {
        "label": "Total calcium",
        "type": "continuous",
        "unit": "mg/dL",
        "minimum": 2.0,
        "maximum": 20.0,
        "step": 0.1,
        "window": "Earliest valid value during 0–24 h",
        "group": "Hematological and laboratory measurements",
    },
    "vasopressor_any_0_24h": {
        "label": "Vasopressor use",
        "type": "binary",
        "unit": "0/1",
        "window": "Documented use during 0–24 h",
        "group": "Hemodynamics and respiratory support",
    },
    "WBC": {
        "label": "White blood cell count",
        "type": "continuous",
        "unit": "×10⁹/L",
        "minimum": 0.1,
        "maximum": 500.0,
        "step": 0.1,
        "window": "Earliest valid value during 0–24 h",
        "group": "Hematological and laboratory measurements",
    },
    "temperature": {
        "label": "Temperature",
        "type": "continuous",
        "unit": "°C",
        "minimum": 25.0,
        "maximum": 45.0,
        "step": 0.1,
        "window": "Earliest valid value during 0–6 h",
        "group": "Hemodynamics and respiratory support",
    },
    "age": {
        "label": "Age",
        "type": "continuous",
        "unit": "years",
        "minimum": 18.0,
        "maximum": 90.0,
        "step": 1.0,
        "window": "At ICU admission",
        "group": "Demographic characteristics",
        "note": "Under the frozen rule, age >89 years is encoded as 90; 90 is not an exact known age.",
    },
    "mean_arterial_pressure": {
        "label": "Mean arterial pressure",
        "type": "continuous",
        "unit": "mmHg",
        "minimum": 15.0,
        "maximum": 199.0,
        "step": 1.0,
        "window": "Earliest valid value during 0–6 h",
        "group": "Hemodynamics and respiratory support",
    },
    "systolic_bp": {
        "label": "Systolic blood pressure",
        "type": "continuous",
        "unit": "mmHg",
        "minimum": 20.0,
        "maximum": 300.0,
        "step": 1.0,
        "window": "Earliest valid value during 0–6 h",
        "group": "Hemodynamics and respiratory support",
    },
    "glucose": {
        "label": "Glucose",
        "type": "continuous",
        "unit": "mg/dL",
        "minimum": 10.0,
        "maximum": 2000.0,
        "step": 1.0,
        "window": "Earliest valid value during 0–24 h",
        "group": "Hematological and laboratory measurements",
    },
    "hematocrit": {
        "label": "Hematocrit",
        "type": "continuous",
        "unit": "%",
        "minimum": 5.0,
        "maximum": 80.0,
        "step": 0.1,
        "window": "Earliest valid value during 0–24 h",
        "group": "Hematological and laboratory measurements",
    },
}

TRAINING_MEDIANS = {
    "platelet_count": 189.0,
    "RRT_any_0_24h": 0.0,
    "serum_creatinine": 0.9,
    "BUN": 18.0,
    "invasive_mechanical_ventilation_0_24h": 0.0,
    "calcium": 8.4,
    "vasopressor_any_0_24h": 0.0,
    "WBC": 11.1,
    "temperature": 36.78,
    "age": 68.0,
    "mean_arterial_pressure": 85.0,
    "systolic_bp": 125.0,
    "glucose": 126.0,
    "hematocrit": 33.5,
}


class InputValidationError(ValueError):
    """Raised when input cannot be mapped to the frozen predictor."""


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def resolved_model_path() -> Path:
    override = os.environ.get(MODEL_PATH_ENV)
    return Path(override).expanduser().resolve() if override else DEFAULT_MODEL_PATH


def load_frozen_pipeline(path: Path | None = None) -> Any:
    model_path = Path(path) if path is not None else resolved_model_path()
    if not model_path.is_file():
        raise FileNotFoundError("The authorized frozen model asset is unavailable.")
    actual_hash = file_sha256(model_path)
    if actual_hash.lower() != EXPECTED_MODEL_SHA256:
        raise RuntimeError(
            "Frozen model SHA-256 mismatch. The application will not load an unverified model."
        )
    with model_path.open("rb") as stream:
        pipeline = pickle.load(stream)
    feature_names = list(getattr(pipeline, "feature_names_in_", []))
    if feature_names != FEATURE_ORDER:
        raise RuntimeError("Frozen pipeline feature order does not match the locked 14-variable order.")
    classes = np.asarray(getattr(pipeline, "classes_", []))
    if classes.tolist() != [0, 1]:
        raise RuntimeError("Frozen pipeline class order is not [0, 1].")
    return pipeline


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    try:
        return bool(pd.isna(value))
    except (TypeError, ValueError):
        return False


def validate_and_make_frame(
    values: Mapping[str, Any],
    unit_overrides: Mapping[str, str] | None = None,
) -> tuple[pd.DataFrame, list[str]]:
    extras = sorted(set(values) - set(FEATURE_ORDER))
    if extras:
        raise InputValidationError("Unexpected input fields: " + ", ".join(extras))

    row: dict[str, float] = {}
    imputed_fields: list[str] = []
    for feature in FEATURE_ORDER:
        spec = INPUT_SCHEMA[feature]
        value = values.get(feature)
        if unit_overrides and feature in unit_overrides:
            supplied_unit = str(unit_overrides[feature]).strip()
            if supplied_unit != spec["unit"]:
                raise InputValidationError(
                    f"{spec['label']}: expected unit {spec['unit']}, received {supplied_unit}."
                )

        if spec["type"] == "binary":
            if _is_missing(value):
                raise InputValidationError(
                    f"{spec['label']}: select whether use was documented during 0–24 h."
                )
            try:
                number = float(value)
            except (TypeError, ValueError) as exc:
                raise InputValidationError(f"{spec['label']}: enter 0 or 1.") from exc
            if not np.isfinite(number) or number not in (0.0, 1.0):
                raise InputValidationError(f"{spec['label']}: only 0 or 1 is accepted.")
            row[feature] = number
            continue

        if _is_missing(value):
            row[feature] = np.nan
            imputed_fields.append(feature)
            continue
        try:
            number = float(value)
        except (TypeError, ValueError) as exc:
            raise InputValidationError(f"{spec['label']}: enter a numeric value or leave it blank.") from exc
        if not np.isfinite(number):
            raise InputValidationError(f"{spec['label']}: the value must be finite.")
        if number < spec["minimum"] or number > spec["maximum"]:
            raise InputValidationError(
                f"{spec['label']}: {number:g} {spec['unit']} is outside the audited valid range "
                f"({spec['minimum']:g}–{spec['maximum']:g} {spec['unit']})."
            )
        row[feature] = number

    frame = pd.DataFrame([row], columns=FEATURE_ORDER, dtype=float)
    return frame, imputed_fields


def predict_probability(
    pipeline: Any,
    values: Mapping[str, Any],
    unit_overrides: Mapping[str, str] | None = None,
) -> tuple[float, list[str]]:
    frame, imputed_fields = validate_and_make_frame(values, unit_overrides=unit_overrides)
    probabilities = np.asarray(pipeline.predict_proba(frame), dtype=float)
    if probabilities.shape != (1, 2):
        raise RuntimeError(f"Unexpected probability output shape: {probabilities.shape}")
    probability = float(probabilities[0, 1])
    if not np.isfinite(probability) or not 0.0 <= probability <= 1.0:
        raise RuntimeError("The frozen model returned an invalid probability.")
    return probability, imputed_fields


def synthetic_example() -> dict[str, float]:
    """Non-patient demonstration values, based on frozen training medians."""
    return dict(TRAINING_MEDIANS)
