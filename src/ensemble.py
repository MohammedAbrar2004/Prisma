"""
Ensemble methods for PRISMA - Combining LightGBM and Prophet predictions
"""

import numpy as np
import pandas as pd
from typing import Dict, List


def create_ensemble_forecast(
    lgb_predictions: np.ndarray,
    prophet_predictions: np.ndarray,
    weights: Dict[str, float] = None
) -> np.ndarray:
    """
    Create ensemble forecast by combining LightGBM and Prophet predictions
    
    Args:
        lgb_predictions: Predictions from LightGBM model
        prophet_predictions: Predictions from Prophet model
        weights: Dictionary with 'lgb' and 'prophet' weights (default: equal weighting)
        
    Returns:
        Ensemble predictions
    """
    if weights is None:
        # Default: equal weighting
        weights = {'lgb': 0.6, 'prophet': 0.4}
    
    # Normalize weights
    total_weight = weights['lgb'] + weights['prophet']
    lgb_weight = weights['lgb'] / total_weight
    prophet_weight = weights['prophet'] / total_weight
    
    # Weighted average
    ensemble = lgb_weight * lgb_predictions + prophet_weight * prophet_predictions
    
    return ensemble


def adaptive_ensemble(
    lgb_predictions: np.ndarray,
    prophet_predictions: np.ndarray,
    lgb_metrics: Dict,
    prophet_metrics: Dict
) -> np.ndarray:
    """
    Create adaptive ensemble based on validation performance
    
    Args:
        lgb_predictions: Predictions from LightGBM model
        prophet_predictions: Predictions from Prophet model
        lgb_metrics: LightGBM validation metrics
        prophet_metrics: Prophet validation metrics
        
    Returns:
        Adaptive ensemble predictions
    """
    # Use validation RMSE to determine weights (inverse of error)
    lgb_rmse = lgb_metrics['validation']['rmse']
    prophet_rmse = prophet_metrics['validation']['rmse']
    
    # Inverse error weighting
    lgb_weight = (1 / lgb_rmse) if lgb_rmse > 0 else 1.0
    prophet_weight = (1 / prophet_rmse) if prophet_rmse > 0 else 1.0
    
    # Normalize
    total_weight = lgb_weight + prophet_weight
    lgb_weight = lgb_weight / total_weight
    prophet_weight = prophet_weight / total_weight
    
    print(f"   Adaptive ensemble weights:")
    print(f"      - LightGBM: {lgb_weight:.3f} (RMSE: {lgb_rmse:.2f})")
    print(f"      - Prophet: {prophet_weight:.3f} (RMSE: {prophet_rmse:.2f})")
    
    # Weighted average
    ensemble = lgb_weight * lgb_predictions + prophet_weight * prophet_predictions
    
    return ensemble

