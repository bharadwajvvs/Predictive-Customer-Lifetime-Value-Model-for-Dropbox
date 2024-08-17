import pandas as pd
import numpy as np

from acc_info_synthetic_data import account_info
from user_demo_synthetic_data import user_demographics


def generate_customer_support(user_demographics, account_info):
  user_ids = user_demographics['user_id'].tolist()
  issue_types = ['Technical', 'Billing', 'Account', 'Other']

  # Generate random number of interactions per user
  num_interactions = np.random.randint(0, 5, len(user_ids))

  data = []
  for i, user_id in enumerate(user_ids):
    for j in range(num_interactions[i]):
      interaction_id = f"{user_id}_{j+1}"
      interaction_date = pd.to_datetime('2023-01-01') + pd.to_timedelta(np.random.randint(0, 365, 1), unit='D')
      issue_type = np.random.choice(issue_types)
      resolution_time = np.random.randint(10, 120)  # Random resolution time in minutes

      data.append([interaction_id, user_id, interaction_date, issue_type, resolution_time])

  df = pd.DataFrame(data, columns=['interaction_id', 'user_id', 'interaction_date', 'issue_type', 'resolution_time'])

  # Merge with account_info to get plan level
  df = df.merge(account_info[['user_id', 'subscription_type', 'plan_level']], on='user_id', how='left')

  # Correlate interaction volume with subscription type and plan level
  interaction_probs = {'Free': 0.2, 'Paid': {'Basic': 0.1, 'Plus': 0.08, 'Essentials': 0.06, 'Business': 0.04, 'Business Plus': 0.02}}

  def get_interaction_prob(row):
    if row['subscription_type'] == 'Free':
      return interaction_probs['Free']
    else:
      return interaction_probs['Paid'][row['plan_level']]

  df['interaction_prob'] = df.apply(get_interaction_prob, axis=1)
  df['keep'] = np.random.uniform(size=len(df)) < df['interaction_prob']
  df = df[df['keep'] == True].drop(columns=['interaction_prob', 'keep'])

  return df

# Example usage
# Assuming you have user_demographics and account_info DataFrames
customer_support = generate_customer_support(user_demographics, account_info)
customer_support.to_csv('customer_support.csv', index=False)
