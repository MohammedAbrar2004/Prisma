# PRISMA Pipeline Demo Script (PowerShell)
# This script demonstrates the complete PRISMA forecasting pipeline

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  PRISMA - Predictive Resource Intelligence & Supply Chain Management" -ForegroundColor Cyan
Write-Host "  Terminal-Only ML Pipeline for Demand Forecasting" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if data exists
if (-not (Test-Path "data/prisma_dataset.csv")) {
    Write-Host "ERROR: Dataset not found at data/prisma_dataset.csv" -ForegroundColor Red
    Write-Host "Please ensure the dataset is in the correct location."
    exit 1
}

Write-Host "Step 1: Training the forecasting models..." -ForegroundColor Yellow
Write-Host "--------------------------------------------------------------------"
python src/cli.py train --data data/prisma_dataset.csv
Write-Host ""

# Check if training was successful
if (-not (Test-Path "saved_models")) {
    Write-Host "ERROR: Training failed - saved_models directory not found" -ForegroundColor Red
    exit 1
}

Write-Host "Step 2: Creating recent history for prediction..." -ForegroundColor Yellow
Write-Host "--------------------------------------------------------------------"
python -c "import pandas as pd; df = pd.read_csv('data/prisma_dataset.csv'); df['date'] = pd.to_datetime(df['date']); recent = df[df['date'] >= '2024-01-01']; recent.to_csv('data/recent_history.csv', index=False); print(f'Created recent_history.csv with {len(recent)} rows')"
Write-Host ""

Write-Host "Step 3: Generating 14-day forecast..." -ForegroundColor Yellow
Write-Host "--------------------------------------------------------------------"
python src/cli.py predict --input data/recent_history.csv --horizon 14
Write-Host ""

Write-Host "Step 4: Generating 30-day forecast..." -ForegroundColor Yellow
Write-Host "--------------------------------------------------------------------"
python src/cli.py predict --input data/recent_history.csv --horizon 30
Write-Host ""

Write-Host "========================================================================" -ForegroundColor Green
Write-Host "  DEMO COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Generated files:" -ForegroundColor Cyan
Write-Host "  - saved_models/lightgbm_model.txt"
Write-Host "  - saved_models/encoders.pkl"
Write-Host "  - saved_models/feature_names.json"
Write-Host "  - forecast_*_14d.json"
Write-Host "  - forecast_*_14d.csv"
Write-Host "  - forecast_*_30d.json"
Write-Host "  - forecast_*_30d.csv"
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  - Review forecast JSON files for predictions"
Write-Host "  - Import CSV files into your analysis tools"
Write-Host "  - Integrate with your supply chain management system"
Write-Host ""

