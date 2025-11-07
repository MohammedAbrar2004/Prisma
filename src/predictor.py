"""
Prediction pipeline for PRISMA - Generate iterative future forecasts
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Union, Optional
from datetime import timedelta
import lightgbm as lgb
from prophet import Prophet
from sklearn.preprocessing import LabelEncoder
import json
import warnings

from data_utils import TIME_COLUMN, TARGET_COLUMN, get_feature_columns, preprocess_data
from features import prepare_features, create_calendar_features
from ensemble import create_ensemble_forecast

warnings.filterwarnings('ignore')


def generate_iterative_forecast(
    df: pd.DataFrame,
    lgb_model: lgb.Booster,
    prophet_model: Union[Prophet, Dict[str, Prophet]],
    encoders: Dict[str, LabelEncoder],
    feature_names: List[str],
    horizon: int = 30,
    series_col: Optional[str] = None,
    series_value: Optional[str] = None
) -> List[Dict]:
    """
    Generate iterative future demand forecasts
    Uses predictions as features for subsequent predictions

    Args:
        df: Historical data (recent history)
        lgb_model: Trained LightGBM model
        prophet_model: Trained Prophet model (single or dict of per-series models)
        encoders: Label encoders for categorical features
        feature_names: List of feature names
        horizon: Number of days to forecast
        series_col: Column name for series (e.g., 'material')
        series_value: Specific series value to forecast

    Returns:
        List of prediction dictionaries
    """
    print(f"   Generating iterative forecasts for {horizon} days...")

    # Make a copy to avoid modifying original
    df_work = df.copy()

    # Ensure date column is datetime
    df_work[TIME_COLUMN] = pd.to_datetime(df_work[TIME_COLUMN])

    # Get the last date in the dataset
    last_date = df_work[TIME_COLUMN].max()
    print(f"   Last date in data: {last_date}")

    # Generate future dates
    future_dates = pd.date_range(
        start=last_date + timedelta(days=1),
        periods=horizon,
        freq='D'
    )
    print(f"   Forecast period: {future_dates[0]} to {future_dates[-1]}")

    # Select appropriate Prophet model
    prophet_model_to_use = None
    if prophet_model is not None:
        if isinstance(prophet_model, dict):
            if series_value and series_value in prophet_model:
                prophet_model_to_use = prophet_model[series_value]
                print(f"   Using Prophet model for series: {series_value}")
            else:
                # Use first available model as fallback
                prophet_model_to_use = list(prophet_model.values())[0]
                print(f"   Using fallback Prophet model")
        else:
            prophet_model_to_use = prophet_model
            print(f"   Using global Prophet model")

    # Prophet predictions (all at once)
    if prophet_model_to_use is not None:
        print(f"   Generating Prophet forecasts...")
        prophet_future = pd.DataFrame({'ds': future_dates})
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            prophet_forecast = prophet_model_to_use.predict(prophet_future)
        prophet_predictions = prophet_forecast['yhat'].values
        prophet_lower = prophet_forecast['yhat_lower'].values
        prophet_upper = prophet_forecast['yhat_upper'].values
        print(f"   ✓ Prophet forecasts generated")
    else:
        print(f"   ⚠️  Prophet model not available, using LightGBM only")
        # Create dummy Prophet predictions (will use LightGBM only)
        prophet_predictions = np.zeros(horizon)
        prophet_lower = np.zeros(horizon)
        prophet_upper = np.zeros(horizon)

    # LightGBM iterative predictions
    print(f"   Generating iterative LightGBM forecasts...")
    lgb_predictions = []

    # Get the last N rows for lag feature computation
    history_df = df_work.copy()

    for i, future_date in enumerate(future_dates):
        # Create future row based on last known values
        future_row = history_df.iloc[-1:].copy()
        future_row[TIME_COLUMN] = future_date

        # Update calendar features
        future_row['day_of_week'] = future_date.dayofweek
        future_row['month'] = future_date.month
        future_row['is_weekend'] = 1 if future_date.dayofweek >= 5 else 0
        future_row['day_of_month'] = future_date.day
        future_row['quarter'] = (future_date.month - 1) // 3 + 1
        future_row['week_of_year'] = future_date.isocalendar().week

        # Update year, month, quarter, week if they exist
        if 'year' in future_row.columns:
            future_row['year'] = future_date.year

        # Compute lag features from history
        # Lag 1: previous day's prediction (or last known value)
        if i == 0:
            lag_1_value = history_df[TARGET_COLUMN].iloc[-1]
        else:
            lag_1_value = lgb_predictions[-1]

        # Lag 7, 14, 30: from history or previous predictions
        if 'quantity_lag_1' in future_row.columns:
            future_row['quantity_lag_1'] = lag_1_value

        if 'quantity_lag_7' in future_row.columns:
            if i < 7:
                future_row['quantity_lag_7'] = history_df[TARGET_COLUMN].iloc[-(7-i)]
            else:
                future_row['quantity_lag_7'] = lgb_predictions[i-7]

        if 'quantity_lag_14' in future_row.columns:
            if i < 14:
                idx = max(0, len(history_df) - (14-i))
                future_row['quantity_lag_14'] = history_df[TARGET_COLUMN].iloc[idx]
            else:
                future_row['quantity_lag_14'] = lgb_predictions[i-14]

        if 'quantity_lag_30' in future_row.columns:
            if i < 30:
                idx = max(0, len(history_df) - (30-i))
                future_row['quantity_lag_30'] = history_df[TARGET_COLUMN].iloc[idx]
            else:
                future_row['quantity_lag_30'] = lgb_predictions[i-30]

        # Compute rolling features
        # Use recent history + predictions so far
        recent_values = list(history_df[TARGET_COLUMN].tail(30).values) + lgb_predictions

        if 'quantity_rolling_mean_7' in future_row.columns:
            future_row['quantity_rolling_mean_7'] = np.mean(recent_values[-(7+i):len(recent_values)])

        if 'quantity_rolling_mean_14' in future_row.columns:
            future_row['quantity_rolling_mean_14'] = np.mean(recent_values[-(14+i):len(recent_values)])

        if 'quantity_rolling_mean_30' in future_row.columns:
            future_row['quantity_rolling_mean_30'] = np.mean(recent_values[-(30+i):len(recent_values)])

        if 'quantity_rolling_std_7' in future_row.columns:
            future_row['quantity_rolling_std_7'] = np.std(recent_values[-(7+i):len(recent_values)])

        if 'quantity_rolling_std_14' in future_row.columns:
            future_row['quantity_rolling_std_14'] = np.std(recent_values[-(14+i):len(recent_values)])

        if 'quantity_rolling_std_30' in future_row.columns:
            future_row['quantity_rolling_std_30'] = np.std(recent_values[-(30+i):len(recent_values)])

        # Prepare features for this single prediction
        # Set target to 0 (placeholder)
        future_row[TARGET_COLUMN] = 0

        # Extract features in the correct order
        X_future_row = []
        for feat in feature_names:
            if feat in future_row.columns:
                val = future_row[feat].values[0]
                # Handle categorical encoding
                if feat in encoders:
                    # Already encoded during data prep
                    X_future_row.append(val)
                else:
                    X_future_row.append(val)
            else:
                X_future_row.append(0)  # Missing feature

        X_future_row = np.array(X_future_row).reshape(1, -1)

        # Make prediction
        pred = lgb_model.predict(X_future_row)[0]
        pred = max(0, pred)  # Ensure non-negative
        lgb_predictions.append(pred)

    lgb_predictions = np.array(lgb_predictions)
    print(f"   ✓ LightGBM iterative forecasts generated")

    # Ensemble predictions
    print(f"   Creating ensemble forecasts...")
    if prophet_model_to_use is not None:
        ensemble_predictions = create_ensemble_forecast(
            lgb_predictions,
            prophet_predictions,
            weights={'lgb': 0.6, 'prophet': 0.4}
        )
    else:
        # Use LightGBM only
        ensemble_predictions = lgb_predictions
        print(f"   Using LightGBM predictions only (Prophet not available)")
    print(f"   ✓ Ensemble forecasts created")

    # Format output
    predictions = []
    for i, date in enumerate(future_dates):
        pred_dict = {
            'date': date.strftime('%Y-%m-%d'),
            'y_hat': float(ensemble_predictions[i]),
            'y_lower': float(max(0, prophet_lower[i])),
            'y_upper': float(prophet_upper[i]),
            'lgb_prediction': float(lgb_predictions[i]),
            'prophet_prediction': float(prophet_predictions[i])
        }
        predictions.append(pred_dict)

    # Print summary statistics
    print(f"\n   📊 Forecast Summary:")
    print(f"      Mean predicted quantity: {np.mean(ensemble_predictions):.2f}")
    print(f"      Min predicted quantity: {np.min(ensemble_predictions):.2f}")
    print(f"      Max predicted quantity: {np.max(ensemble_predictions):.2f}")
    print(f"      Total predicted demand: {np.sum(ensemble_predictions):.2f}")

    return predictions



def format_forecast_json(
    predictions: List[Dict],
    df: pd.DataFrame,
    horizon: int,
    series_col: Optional[str] = None,
    series_value: Optional[str] = None
) -> Dict:
    """
    Format predictions as JSON output

    Args:
        predictions: List of prediction dictionaries
        df: Original dataframe (for metadata)
        horizon: Forecast horizon
        series_col: Series column name
        series_value: Series value

    Returns:
        Formatted JSON dictionary
    """
    # Extract metadata from dataframe
    metadata = {}

    if series_col and series_col in df.columns:
        if series_value is not None:
            # Convert to native Python type
            if isinstance(series_value, (np.integer, np.floating)):
                metadata[series_col] = int(series_value)
            else:
                metadata[series_col] = str(series_value)
        else:
            val = df[series_col].iloc[-1]
            if isinstance(val, (np.integer, np.floating)):
                metadata[series_col] = int(val)
            else:
                metadata[series_col] = str(val)

    # Check for other identifying columns
    for col in ['project_id', 'region', 'supplier']:
        if col in df.columns:
            val = df[col].iloc[-1]
            if isinstance(val, (np.integer, np.floating)):
                metadata[col] = int(val)
            else:
                metadata[col] = str(val)

    # Build output JSON
    output = {
        'metadata': metadata,
        'horizon_days': horizon,
        'forecast_start': predictions[0]['date'],
        'forecast_end': predictions[-1]['date'],
        'total_predicted_demand': float(sum(p['y_hat'] for p in predictions)),
        'forecast': [
            {
                'date': p['date'],
                'y_hat': round(p['y_hat'], 2),
                'y_lower': round(p['y_lower'], 2),
                'y_upper': round(p['y_upper'], 2)
            }
            for p in predictions
        ]
    }

    return output


def save_forecast_csv(
    predictions: List[Dict],
    output_path: str,
    include_components: bool = True
):
    """
    Save forecast to CSV file

    Args:
        predictions: List of prediction dictionaries
        output_path: Path to save CSV
        include_components: Include LightGBM and Prophet components
    """
    # Convert to DataFrame
    if include_components:
        df = pd.DataFrame(predictions)
    else:
        df = pd.DataFrame([
            {
                'date': p['date'],
                'y_hat': p['y_hat'],
                'y_lower': p['y_lower'],
                'y_upper': p['y_upper']
            }
            for p in predictions
        ])

    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"   ✓ Forecast saved to: {output_path}")


def print_forecast_table(predictions: List[Dict], max_rows: int = 10):
    """
    Print forecast as formatted table

    Args:
        predictions: List of prediction dictionaries
        max_rows: Maximum rows to display
    """
    print("\n" + "="*80)
    print("📅 FORECAST TABLE")
    print("="*80)

    print(f"\n{'Date':<12} {'Predicted':<12} {'Lower':<12} {'Upper':<12} {'Range':<12}")
    print("-"*80)

    # Show first few rows
    for i, pred in enumerate(predictions[:max_rows]):
        date = pred['date']
        y_hat = pred['y_hat']
        y_lower = pred['y_lower']
        y_upper = pred['y_upper']
        range_val = y_upper - y_lower

        print(f"{date:<12} {y_hat:<12.2f} {y_lower:<12.2f} {y_upper:<12.2f} {range_val:<12.2f}")

    # Show ellipsis if truncated
    if len(predictions) > max_rows:
        print(f"... ({len(predictions) - max_rows} more rows)")
        print("-"*80)

        # Show last row
        pred = predictions[-1]
        date = pred['date']
        y_hat = pred['y_hat']
        y_lower = pred['y_lower']
        y_upper = pred['y_upper']
        range_val = y_upper - y_lower

        print(f"{date:<12} {y_hat:<12.2f} {y_lower:<12.2f} {y_upper:<12.2f} {range_val:<12.2f}")

    print("="*80)


