"""
Evaluation utilities for PRISMA - Metrics and reporting
"""

import numpy as np
import pandas as pd
from typing import Dict, List
import lightgbm as lgb


def print_metrics(
    lgb_metrics: Dict,
    prophet_metrics: Dict,
    lgb_model: lgb.Booster,
    feature_names: List[str],
    top_n: int = 10
):
    """
    Print comprehensive model evaluation metrics

    Args:
        lgb_metrics: LightGBM metrics dictionary
        prophet_metrics: Prophet metrics dictionary
        lgb_model: Trained LightGBM model
        feature_names: List of feature names
        top_n: Number of top features to display
    """
    print("\n" + "="*70)
    print("📊 MODEL EVALUATION SUMMARY")
    print("="*70)

    # LightGBM metrics
    print("\n🌳 LightGBM Performance:")
    print("-" * 70)
    print(f"{'Metric':<20} {'Train':<20} {'Validation':<20}")
    print("-" * 70)

    for metric in ['mae', 'rmse', 'mape', 'r2']:
        if metric in lgb_metrics['train']:
            train_val = lgb_metrics['train'][metric]
            val_val = lgb_metrics['validation'][metric]

            if metric == 'mape':
                print(f"{metric.upper():<20} {train_val:<20.2f}% {val_val:<20.2f}%")
            elif metric == 'r2':
                print(f"{metric.upper():<20} {train_val:<20.4f} {val_val:<20.4f}")
            else:
                print(f"{metric.upper():<20} {train_val:<20.2f} {val_val:<20.2f}")

    # Prophet metrics
    print("\n📈 Prophet Performance:")
    print("-" * 70)

    # Check if per-series or global
    if 'num_series' in prophet_metrics:
        print(f"   Per-series models: {prophet_metrics['num_series']} series")
        print(f"   Metrics averaged across all series:")
        print("-" * 70)
        print(f"{'Metric':<20} {'Validation (Avg)':<20}")
        print("-" * 70)

        for metric in ['mae', 'rmse', 'mape']:
            if metric in prophet_metrics['validation']:
                val_val = prophet_metrics['validation'][metric]
                if metric == 'mape':
                    print(f"{metric.upper():<20} {val_val:<20.2f}%")
                else:
                    print(f"{metric.upper():<20} {val_val:<20.2f}")
    else:
        print(f"{'Metric':<20} {'Train':<20} {'Validation':<20}")
        print("-" * 70)

        for metric in ['mae', 'rmse', 'mape', 'r2']:
            if metric in prophet_metrics['train']:
                train_val = prophet_metrics['train'][metric]
                val_val = prophet_metrics['validation'][metric]

                if metric == 'mape':
                    print(f"{metric.upper():<20} {train_val:<20.2f}% {val_val:<20.2f}%")
                elif metric == 'r2':
                    print(f"{metric.upper():<20} {train_val:<20.4f} {val_val:<20.4f}")
                else:
                    print(f"{metric.upper():<20} {train_val:<20.2f} {val_val:<20.2f}")

    # Feature importance (already printed in models.py, but show summary here)
    print(f"\n🎯 Top {top_n} Feature Importances (LightGBM):")
    print("-" * 70)

    importance = lgb_model.feature_importance(importance_type='gain')
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': importance
    }).sort_values('importance', ascending=False)

    print(f"{'Rank':<6} {'Feature':<40} {'Importance':<15}")
    print("-" * 70)

    for idx, row in feature_importance.head(top_n).iterrows():
        rank = feature_importance.index.get_loc(idx) + 1
        print(f"{rank:<6} {row['feature']:<40} {row['importance']:<15,.0f}")

    print("="*70)


def calculate_forecast_metrics(
    actual: np.ndarray,
    predicted: np.ndarray
) -> Dict[str, float]:
    """
    Calculate forecast accuracy metrics
    
    Args:
        actual: Actual values
        predicted: Predicted values
        
    Returns:
        Dictionary of metrics
    """
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    r2 = r2_score(actual, predicted)
    
    # MAPE (Mean Absolute Percentage Error)
    # Avoid division by zero
    mask = actual != 0
    mape = np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask])) * 100 if mask.any() else 0
    
    return {
        'mae': mae,
        'rmse': rmse,
        'r2': r2,
        'mape': mape
    }

