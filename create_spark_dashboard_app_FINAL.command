#!/bin/bash
# Spark Dashboard Launcher (FINAL version with user's specific path)

APP_PATH="/Users/joebudds/Desktop/Spark App/spark_dashboard_app.py"

# Check if the Streamlit file exists
if [ ! -f "$APP_PATH" ]; then
  echo "⚠️ Could not find the dashboard at: $APP_PATH"
  echo "Please make sure the file is saved in the right location."
  exit 1
fi

# Launch the dashboard
echo "🚀 Launching Spark Dashboard from $APP_PATH..."
streamlit run "$APP_PATH"
