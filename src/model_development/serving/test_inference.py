# Databricks notebook source
# MAGIC %run /Repos/michael.henzl@datasentics.com/daipe_mlops/bootstrap/bootstrap_base

# COMMAND ----------

from mlops_test import test_api
import pandas as pd

# COMMAND ----------

test = test_api.TestAPI()

# COMMAND ----------

test.deploy_code()

# COMMAND ----------
'''
When your API is deployed you can send request
to it with your own custom data with method test_api()

test.test_api(df, '<your_api_address>')
'''

# COMMAND ----------



