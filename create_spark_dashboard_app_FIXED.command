#!/bin/bash
# Spark Dashboard Launcher with auto-directory detection and permission instructions

APP_DIR="$HOME/Desktop/Spark App"
SCRIPT_NAME="spark_dashboard_app.py"

# Check if script file exists
if [ ! -f "$APP_DIR/$SCRIPT_NAME" ]; then
  echo "⚠️ Could not find the script: $SCRIPT_NAME in $APP_DIR"
  echo "Make sure you've placed the Streamlit file correctly!"
  exit 1
fi

# Launch the Streamlit dashboard
echo "🚀 Launching Spark Dashboard..."
streamlit run "$APP_DIR/$SCRIPT_NAME"
