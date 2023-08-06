

import os

# Cloud provider to use (AWS or GCP) - defaults to AWS
cloud_provider= os.getenv("CLOUD_PROVIDER", "AWS")

# AWS account credentials
aws_access_key_id= os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key= os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region= os.getenv("AWS_REGION")

# GCP token source (custom for json key based access) - by defaults uses workload identity federation
gcp_token_source= os.getenv("GCP_TOKEN_SOURCE")
# GCP Service account credentials
gcp_service_account_key_json= os.getenv("GCP_SERVICE_ACCOUNT_KEY_JSON")

