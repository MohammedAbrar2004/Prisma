"""
Model persistence for PRISMA - Save and load trained models
"""

import joblib
import json
from pathlib import Path
from typing import Dict, List, Tuple
import lightgbm as lgb
from prophet import Prophet
from sklearn.preprocessing import LabelEncoder


def save_models(
    lgb_model: lgb.Booster,
    prophet_model: Prophet,
    encoders: Dict[str, LabelEncoder],
    feature_names: List[str],
    output_dir: Path
):
    """
    Save trained models and artifacts
    
    Args:
        lgb_model: Trained LightGBM model
        prophet_model: Trained Prophet model
        encoders: Dictionary of label encoders
        feature_names: List of feature names
        output_dir: Directory to save models
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"   Saving models to {output_dir}/")
    
    # Save LightGBM model
    lgb_path = output_dir / 'lightgbm_model.txt'
    lgb_model.save_model(str(lgb_path))
    print(f"   ✓ LightGBM model saved: {lgb_path.name}")
    
    # Save Prophet model
    prophet_path = output_dir / 'prophet_model.pkl'
    joblib.dump(prophet_model, prophet_path)
    print(f"   ✓ Prophet model saved: {prophet_path.name}")
    
    # Save encoders
    encoders_path = output_dir / 'encoders.pkl'
    joblib.dump(encoders, encoders_path)
    print(f"   ✓ Encoders saved: {encoders_path.name}")
    
    # Save feature names
    features_path = output_dir / 'feature_names.json'
    with open(features_path, 'w') as f:
        json.dump(feature_names, f, indent=2)
    print(f"   ✓ Feature names saved: {features_path.name}")
    
    # Save metadata
    metadata = {
        'n_features': len(feature_names),
        'model_type': 'LightGBM + Prophet Ensemble',
        'saved_at': str(Path.cwd())
    }
    metadata_path = output_dir / 'metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"   ✓ Metadata saved: {metadata_path.name}")


def load_models(
    model_dir: Path
) -> Tuple[lgb.Booster, Prophet, Dict[str, LabelEncoder], List[str]]:
    """
    Load trained models and artifacts
    
    Args:
        model_dir: Directory containing saved models
        
    Returns:
        Tuple of (lgb_model, prophet_model, encoders, feature_names)
    """
    model_dir = Path(model_dir)
    
    if not model_dir.exists():
        raise FileNotFoundError(f"Model directory not found: {model_dir}")
    
    print(f"   Loading models from {model_dir}/")
    
    # Load LightGBM model
    lgb_path = model_dir / 'lightgbm_model.txt'
    if not lgb_path.exists():
        raise FileNotFoundError(f"LightGBM model not found: {lgb_path}")
    lgb_model = lgb.Booster(model_file=str(lgb_path))
    print(f"   ✓ LightGBM model loaded")
    
    # Load Prophet model
    prophet_path = model_dir / 'prophet_model.pkl'
    if not prophet_path.exists():
        raise FileNotFoundError(f"Prophet model not found: {prophet_path}")
    prophet_model = joblib.load(prophet_path)
    print(f"   ✓ Prophet model loaded")
    
    # Load encoders
    encoders_path = model_dir / 'encoders.pkl'
    if not encoders_path.exists():
        raise FileNotFoundError(f"Encoders not found: {encoders_path}")
    encoders = joblib.load(encoders_path)
    print(f"   ✓ Encoders loaded")
    
    # Load feature names
    features_path = model_dir / 'feature_names.json'
    if not features_path.exists():
        raise FileNotFoundError(f"Feature names not found: {features_path}")
    with open(features_path, 'r') as f:
        feature_names = json.load(f)
    print(f"   ✓ Feature names loaded ({len(feature_names)} features)")
    
    return lgb_model, prophet_model, encoders, feature_names

