import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from acc_info_synthetic_data import account_info
from user_demo_synthetic_data import user_demographics


def generate_usage_data(user_demographics, account_info):
  user_ids = user_demographics['user_id'].tolist()
  features = ['file_sharing', 'file_editing', 'search', 'commenting']
  devices = ['desktop', 'mobile', 'tablet']

  # Generate usage data for each user
  data = []
  for user_id in user_ids:
    # Determine number of usage records for the user
    num_records = np.random.randint(10, 30)

    for _ in range(num_records):
      date = pd.to_datetime('2023-01-01') + pd.to_timedelta(np.random.randint(0, 365), unit='D')
      hour = np.random.randint(0, 24)
      day_of_week = date.weekday()

      # Adjust metrics based on time of day and day of week
      file_count = np.random.randint(10, 100) * (1 + 0.2 * np.sin(hour * np.pi / 12)) * (1 + 0.1 * (day_of_week < 5))
      file_size_total = np.random.randint(100, 10000) * (1 + 0.15 * np.sin(hour * np.pi / 12)) * (1 + 0.08 * (day_of_week < 5))
      storage_used = np.random.randint(1, 50) * (1 + 0.1 * np.sin(hour * np.pi / 12)) * (1 + 0.05 * (day_of_week < 5))
      share_count = np.random.randint(0, 10) * (1 + 0.1 * np.sin(hour * np.pi / 12)) * (1 + 0.05 * (day_of_week < 5))

      # Generate session data
      session_id = f"{user_id}_{date}_{np.random.randint(1, 10)}"
      session_start_time = pd.to_datetime(date) + pd.to_timedelta(hour, unit='h')
      session_end_time = session_start_time + pd.to_timedelta(np.random.randint(10, 60), unit='m')
      session_duration = (session_end_time - session_start_time).total_seconds()

      # Randomly select device type and feature used
      device_type = np.random.choice(devices)
      feature_used = np.random.choice(features)

      data.append([user_id, date, file_count, file_size_total, storage_used, share_count, device_type, feature_used, session_id, session_start_time, session_end_time, session_duration])

  df = pd.DataFrame(data, columns=['user_id', 'date', 'file_count', 'file_size_total', 'storage_used', 'share_count', 'device_type', 'feature_used', 'session_id', 'session_start_time', 'session_end_time', 'session_duration'])

  return df

# Example usage
# Assuming you have user_demographics and account_info DataFrames
usage_data = generate_usage_data(user_demographics, account_info)
usage_data.to_csv('usage_data.csv', index=False)