import pandas as pd
import numpy as np

def generate_user_demographics(num_users):
  # Define ranges and categories for each demographic
  age_range = (16, 80)
  genders = ['Male', 'Female', 'Other']
  locations = ['US', 'UK', 'Canada', 'Australia', 'India']
  occupations = ['Student', 'Professional', 'Manager', 'Entrepreneur', 'Retired']
  education_levels = ['High School', 'College', 'Graduate Degree']

  # Introduce age distribution based on population demographics
  age_distribution = [0.1, 0.2, 0.3, 0.2, 0.1, 0.1]  # Example distribution for age groups
  age_bins = [16, 25, 40, 55, 70, 80]
  ages = np.random.choice(age_bins, num_users, p=age_distribution)

  data = {
      'user_id': range(1, num_users + 1),
      'age': ages,
      'gender': np.random.choice(genders, num_users),
      'location': np.random.choice(locations, num_users),
      'occupation': np.random.choice(occupations, num_users),
      'education_level': np.random.choice(education_levels, num_users)
  }
  df = pd.DataFrame(data)
  return df

# Example usage
num_users = 10000
user_demographics = generate_user_demographics(num_users)
user_demographics.to_csv('user_demographics.csv', index=False)
