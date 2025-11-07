#!/bin/bash
# PRISMA Pipeline Demo Script
# This script demonstrates the complete PRISMA forecasting pipeline

echo "========================================================================"
echo "  PRISMA - Predictive Resource Intelligence & Supply Chain Management"
echo "  Terminal-Only ML Pipeline for Demand Forecasting"
echo "========================================================================"
echo ""

# Check if data exists
if [ ! -f "data/prisma_dataset.csv" ]; then
    echo "ERROR: Dataset not found at data/prisma_dataset.csv"
    echo "Please ensure the dataset is in the correct location."
    exit 1
fi

echo "Step 1: Training the forecasting models..."
echo "--------------------------------------------------------------------"
python src/cli.py train --data data/prisma_dataset.csv
echo ""

# Check if training was successful
if [ ! -d "saved_models" ]; then
    echo "ERROR: Training failed - saved_models directory not found"
    exit 1
fi

echo "Step 2: Creating recent history for prediction..."
echo "--------------------------------------------------------------------"
python -c "
import pandas as pd
df = pd.read_csv('data/prisma_dataset.csv')
df['date'] = pd.to_datetime(df['date'])
recent = df[df['date'] >= '2024-01-01']
recent.to_csv('data/recent_history.csv', index=False)
print(f'Created recent_history.csv with {len(recent)} rows')
"
echo ""

echo "Step 3: Generating 14-day forecast..."
echo "--------------------------------------------------------------------"
python src/cli.py predict --input data/recent_history.csv --horizon 14
echo ""

echo "Step 4: Generating 30-day forecast..."
echo "--------------------------------------------------------------------"
python src/cli.py predict --input data/recent_history.csv --horizon 30
echo ""

echo "========================================================================"
echo "  DEMO COMPLETED SUCCESSFULLY!"
echo "========================================================================"
echo ""
echo "Generated files:"
echo "  - saved_models/lightgbm_model.txt"
echo "  - saved_models/encoders.pkl"
echo "  - saved_models/feature_names.json"
echo "  - forecast_*_14d.json"
echo "  - forecast_*_14d.csv"
echo "  - forecast_*_30d.json"
echo "  - forecast_*_30d.csv"
echo ""
echo "Next steps:"
echo "  - Review forecast JSON files for predictions"
echo "  - Import CSV files into your analysis tools"
echo "  - Integrate with your supply chain management system"
echo ""

