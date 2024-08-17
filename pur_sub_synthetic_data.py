import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from acc_info_synthetic_data import account_info
from user_demo_synthetic_data import user_demographics


def generate_subscription_data(user_demographics, account_info):
  user_ids = user_demographics['user_id'].tolist()
  plan_levels = ['Basic', 'Plus', 'Essentials', 'Business', 'Business Plus']
  payment_methods = ['Credit Card', 'PayPal']

  data = []
  for user_id in user_ids:
    # Determine if user has a subscription
    if np.random.rand() > 0.3:  # 70% chance of having a subscription
      subscription_start_date = pd.to_datetime('2023-01-01') + pd.to_timedelta(np.random.randint(0, 365), unit='D')
      plan_level = np.random.choice(plan_levels)
      payment_method = np.random.choice(payment_methods)
      subscription_length = np.random.randint(1, 24)  # Subscription length in months
      subscription_end_date = subscription_start_date + pd.DateOffset(months=subscription_length)

      # Generate potential upgrades, downgrades, and cancellations (simplified for now)
      upgrade_date = None
      downgrade_date = None
      cancellation_date = None
      if np.random.rand() < 0.1:  # 10% chance of upgrade
        upgrade_date = subscription_start_date + pd.DateOffset(months=np.random.randint(1, 12))
      if np.random.rand() < 0.1:  # 10% chance of downgrade
        downgrade_date = subscription_start_date + pd.DateOffset(months=np.random.randint(1, 12))
      if np.random.rand() < 0.1:  # 10% chance of cancellation
          cancellation_date = subscription_start_date + pd.DateOffset(months=np.random.randint(0, subscription_length))

      data.append([user_id, subscription_start_date, subscription_end_date, plan_level, payment_method, 0, upgrade_date, downgrade_date, cancellation_date])

  df = pd.DataFrame(data, columns=['user_id', 'subscription_start_date', 'subscription_end_date', 'plan_level', 'payment_method', 'revenue_generated', 'upgrade_date', 'downgrade_date', 'cancellation_date'])

  # Calculate revenue based on plan level and subscription duration
  def calculate_revenue(row):
    plan_prices = {'Basic': 10, 'Plus': 20, 'Essentials': 30, 'Business': 50, 'Business Plus': 100}
    months = (row['subscription_end_date'] - row['subscription_start_date']).days / 30
    return plan_prices[row['plan_level']] * months

  df['revenue_generated'] = df.apply(calculate_revenue, axis=1)

  return df

def generate_in_app_purchase_data(user_demographics, account_info):
  user_ids = user_demographics['user_id'].tolist()
  product_types = ['in_app_currency', 'consumable', 'non_consumable']

  data = []
  for user_id in user_ids:
    # Determine number of in-app purchases
    num_purchases = np.random.randint(0, 5)

    for _ in range(num_purchases):
      purchase_date = pd.to_datetime('2023-01-01') + pd.to_timedelta(np.random.randint(0, 365), unit='D')
      product_type = np.random.choice(product_types)
      purchase_amount = np.random.uniform(0.99, 99.99)

      data.append([user_id, purchase_date, product_type, purchase_amount])

  df = pd.DataFrame(data, columns=['user_id', 'purchase_date', 'product_type', 'purchase_amount'])

  return df

# Example usage
# Assuming you have user_demographics and account_info DataFrames
subscription_data = generate_subscription_data(user_demographics, account_info)
in_app_purchase_data = generate_in_app_purchase_data(user_demographics, account_info)

subscription_data.to_csv('subscription_data.csv', index=False)
in_app_purchase_data.to_csv('in_app_purchase_data.csv', index=False)
