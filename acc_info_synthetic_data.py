import pandas as pd
import numpy as np

from user_demo_synthetic_data import user_demographics


def generate_account_info(user_demographics):
  # Define subscription types, plan levels, and payment methods
  subscription_types = ['Free', 'Paid']
  plan_levels = ['Basic', 'Plus', 'Essentials', 'Business', 'Business Plus']
  payment_methods = ['Credit Card', 'PayPal']

  user_ids = user_demographics['user_id'].tolist()
  data = {
      'user_id': user_ids,
      'account_creation_date': pd.to_datetime('2023-01-01') + pd.to_timedelta(np.random.randint(0, 365, len(user_ids)), unit='D'),
      'subscription_type': np.random.choice(subscription_types, len(user_ids)),
      'plan_level': np.random.choice(plan_levels, len(user_ids)),
      'payment_method': np.random.choice(payment_methods, len(user_ids))
  }

  # Introduce churn probability based on plan level
  churn_probs = {'Basic': 0.1, 'Plus': 0.09 , 'Essentials': 0.05, 'Business': 0.03, 'Business Plus': 0.01}
  df = pd.DataFrame(data)

  # Introduce subscription duration based on churn probability
  subscription_durations = []
  for _, row in df.iterrows():
    churn_prob = churn_probs[row['plan_level']]
    lifetime = np.random.geometric(churn_prob)
    subscription_duration = min(lifetime, 36)  # Maximum subscription duration of 3 years
    df.at[_, 'account_creation_date'] = pd.to_datetime('2023-01-01') - pd.to_timedelta(subscription_duration, unit='D')

  return df

# Example usage
account_info = generate_account_info(user_demographics)
account_info.to_csv('account_info.csv', index=False)
