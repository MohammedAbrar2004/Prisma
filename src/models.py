"""
Model training for PRISMA - LightGBM (global) and Prophet (per-series)
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, List, Optional, Union
import lightgbm as lgb
from prophet import Prophet
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings

from data_utils import TARGET_COLUMN, TIME_COLUMN

# Suppress Prophet warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', message='.*initial.*')


def calculate_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate Mean Absolute Percentage Error

    Args:
        y_true: True values
        y_pred: Predicted values

    Returns:
        MAPE value
    """
    # Avoid division by zero
    mask = y_true != 0
    if not mask.any():
        return 0.0

    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


def train_lightgbm(
    X: np.ndarray, 
    y: np.ndarray, 
    feature_names: List[str],
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[lgb.Booster, Dict]:
    """
    Train LightGBM model for demand forecasting
    
    Args:
        X: Feature matrix
        y: Target values
        feature_names: List of feature names
        test_size: Proportion of data for validation
        random_state: Random seed
        
    Returns:
        Tuple of (trained model, metrics dictionary)
    """
    print(f"   Training LightGBM with {X.shape[0]} samples, {X.shape[1]} features...")
    
    # Split data
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=test_size, random_state=random_state, shuffle=False
    )
    
    print(f"   Train set: {X_train.shape[0]} samples")
    print(f"   Validation set: {X_val.shape[0]} samples")
    
    # Create LightGBM datasets
    train_data = lgb.Dataset(X_train, label=y_train, feature_name=feature_names)
    val_data = lgb.Dataset(X_val, label=y_val, feature_name=feature_names, reference=train_data)
    
    # LightGBM parameters
    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'boosting_type': 'gbdt',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': -1,
        'seed': random_state
    }
    
    print(f"   Training with parameters:")
    for key, value in params.items():
        print(f"      - {key}: {value}")
    
    # Train model
    model = lgb.train(
        params,
        train_data,
        num_boost_round=500,
        valid_sets=[train_data, val_data],
        valid_names=['train', 'valid'],
        callbacks=[
            lgb.early_stopping(stopping_rounds=50, verbose=False),
            lgb.log_evaluation(period=0)  # Suppress iteration logs
        ]
    )
    
    print(f"   ✓ Training completed in {model.best_iteration} iterations")
    
    # Make predictions
    y_train_pred = model.predict(X_train, num_iteration=model.best_iteration)
    y_val_pred = model.predict(X_val, num_iteration=model.best_iteration)
    
    # Calculate metrics including MAPE
    metrics = {
        'train': {
            'mae': mean_absolute_error(y_train, y_train_pred),
            'rmse': np.sqrt(mean_squared_error(y_train, y_train_pred)),
            'r2': r2_score(y_train, y_train_pred),
            'mape': calculate_mape(y_train, y_train_pred)
        },
        'validation': {
            'mae': mean_absolute_error(y_val, y_val_pred),
            'rmse': np.sqrt(mean_squared_error(y_val, y_val_pred)),
            'r2': r2_score(y_val, y_val_pred),
            'mape': calculate_mape(y_val, y_val_pred)
        }
    }

    print(f"\n   📊 LightGBM Validation Metrics:")
    print(f"      MAE:  {metrics['validation']['mae']:.2f}")
    print(f"      RMSE: {metrics['validation']['rmse']:.2f}")
    print(f"      MAPE: {metrics['validation']['mape']:.2f}%")
    print(f"      R²:   {metrics['validation']['r2']:.4f}")

    # Print top 10 feature importances
    print(f"\n   🔍 Top 10 Feature Importances:")
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importance(importance_type='gain')
    }).sort_values('importance', ascending=False)

    for idx, row in importance_df.head(10).iterrows():
        print(f"      {idx+1:2d}. {row['feature']:30s} - {row['importance']:,.0f}")

    return model, metrics


def train_prophet(
    df: pd.DataFrame,
    test_size: float = 0.2,
    series_col: Optional[str] = None
) -> Tuple[Union[Prophet, Dict[str, Prophet]], Dict]:
    """
    Train Prophet model(s) for time series forecasting
    - If series_col is None or only 1 series: trains single global Prophet model
    - If multiple series exist: trains per-series Prophet models

    Args:
        df: DataFrame with date and target columns
        test_size: Proportion of data for validation
        series_col: Column name for series grouping (e.g., 'material', 'product')

    Returns:
        Tuple of (trained model(s), metrics dictionary)
    """
    # Check if we should train per-series models
    # NOTE: Per-series training disabled due to Prophet optimization issues
    # Using global model for stability
    if False and series_col and series_col in df.columns:
        unique_series = df[series_col].nunique()

        if unique_series > 1:
            print(f"   Training {unique_series} per-series Prophet models for '{series_col}'...")
            return train_prophet_per_series(df, series_col, test_size)

    # Train single global Prophet model
    if series_col and series_col in df.columns:
        print(f"   Training global Prophet model (detected {df[series_col].nunique()} series in '{series_col}')...")
    else:
        print(f"   Training global Prophet model with {len(df)} time points...")

    # Prepare data for Prophet (requires 'ds' and 'y' columns)
    prophet_df = pd.DataFrame({
        'ds': pd.to_datetime(df[TIME_COLUMN]),
        'y': df[TARGET_COLUMN]
    })

    # Split data
    split_idx = int(len(prophet_df) * (1 - test_size))
    train_df = prophet_df.iloc[:split_idx]
    val_df = prophet_df.iloc[split_idx:]

    print(f"   Train set: {len(train_df)} time points")
    print(f"   Validation set: {len(val_df)} time points")

    # Initialize and train Prophet
    model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=True,
        changepoint_prior_scale=0.05,
        seasonality_prior_scale=10.0,
        interval_width=0.95
    )

    print(f"   Fitting Prophet model...")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model.fit(train_df)
    print(f"   ✓ Prophet model fitted")

    # Make predictions
    train_forecast = model.predict(train_df)
    val_forecast = model.predict(val_df)

    # Calculate metrics including MAPE
    metrics = {
        'train': {
            'mae': mean_absolute_error(train_df['y'], train_forecast['yhat']),
            'rmse': np.sqrt(mean_squared_error(train_df['y'], train_forecast['yhat'])),
            'r2': r2_score(train_df['y'], train_forecast['yhat']),
            'mape': calculate_mape(train_df['y'].values, train_forecast['yhat'].values)
        },
        'validation': {
            'mae': mean_absolute_error(val_df['y'], val_forecast['yhat']),
            'rmse': np.sqrt(mean_squared_error(val_df['y'], val_forecast['yhat'])),
            'r2': r2_score(val_df['y'], val_forecast['yhat']),
            'mape': calculate_mape(val_df['y'].values, val_forecast['yhat'].values)
        }
    }

    print(f"\n   📊 Prophet Validation Metrics:")
    print(f"      MAE:  {metrics['validation']['mae']:.2f}")
    print(f"      RMSE: {metrics['validation']['rmse']:.2f}")
    print(f"      MAPE: {metrics['validation']['mape']:.2f}%")
    print(f"      R²:   {metrics['validation']['r2']:.4f}")

    return model, metrics


def train_prophet_per_series(
    df: pd.DataFrame,
    series_col: str,
    test_size: float = 0.2
) -> Tuple[Dict[str, Prophet], Dict]:
    """
    Train separate Prophet models for each series

    Args:
        df: DataFrame with date, target, and series columns
        series_col: Column name for series grouping
        test_size: Proportion of data for validation

    Returns:
        Tuple of (dictionary of models, aggregated metrics)
    """
    models = {}
    all_metrics = []

    unique_series = df[series_col].unique()
    print(f"   Training Prophet for {len(unique_series)} series...")

    for series_name in unique_series:
        # Filter data for this series
        series_df = df[df[series_col] == series_name].copy()

        if len(series_df) < 10:  # Skip series with too few data points
            print(f"      ⚠ Skipping '{series_name}' - insufficient data ({len(series_df)} points)")
            continue

        # Prepare Prophet data
        prophet_df = pd.DataFrame({
            'ds': pd.to_datetime(series_df[TIME_COLUMN]),
            'y': series_df[TARGET_COLUMN]
        })

        # Split data
        split_idx = int(len(prophet_df) * (1 - test_size))
        train_df = prophet_df.iloc[:split_idx]
        val_df = prophet_df.iloc[split_idx:]

        # Train model
        model = Prophet(
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=False,
            changepoint_prior_scale=0.05,
            interval_width=0.95
        )

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model.fit(train_df)

        models[series_name] = model

        # Calculate metrics
        val_forecast = model.predict(val_df)
        series_metrics = {
            'mae': mean_absolute_error(val_df['y'], val_forecast['yhat']),
            'rmse': np.sqrt(mean_squared_error(val_df['y'], val_forecast['yhat'])),
            'mape': calculate_mape(val_df['y'].values, val_forecast['yhat'].values)
        }
        all_metrics.append(series_metrics)

        print(f"      ✓ '{series_name}' - MAE: {series_metrics['mae']:.2f}, RMSE: {series_metrics['rmse']:.2f}")

    # Aggregate metrics
    avg_metrics = {
        'validation': {
            'mae': np.mean([m['mae'] for m in all_metrics]),
            'rmse': np.mean([m['rmse'] for m in all_metrics]),
            'mape': np.mean([m['mape'] for m in all_metrics]),
            'r2': 0.0  # Not meaningful for aggregated per-series models
        },
        'train': {
            'mae': 0.0,
            'rmse': 0.0,
            'mape': 0.0,
            'r2': 0.0
        },
        'num_series': len(models)
    }

    print(f"\n   📊 Prophet Per-Series Validation Metrics (averaged across {len(models)} series):")
    print(f"      MAE:  {avg_metrics['validation']['mae']:.2f}")
    print(f"      RMSE: {avg_metrics['validation']['rmse']:.2f}")
    print(f"      MAPE: {avg_metrics['validation']['mape']:.2f}%")

    return models, avg_metrics

