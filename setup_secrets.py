"""
One-time setup script: creates the Databricks secret scope and stores the
Massive API key. Run this locally (with the Databricks CLI configured) or
from a notebook - never commit the resulting secret value anywhere.

Usage:
    python setup_secrets.py
"""
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import workspace
import getpass

w = WorkspaceClient()

# w.secrets.create_scope(scope="massive")
# w.secrets.put_secret(
#     scope="massive",
#     key="api-key",
#     string_value=getpass.getpass("Paste your Massive API key: ")
# )

# Create the lakebase-secrets scope (comment out if already created)
# w.secrets.create_scope(scope="lakebase-secrets")

# Store the Lakebase connection URL (host)
w.secrets.put_secret(
    scope="lakebase-secrets",
    key="lakebase-host",
    string_value=input("Enter your Lakebase host (e.g., ep-xxx.database.region.cloud.databricks.com): ")
)

print("✅ Lakebase host stored!")

# Store the Lakebase role password
w.secrets.put_secret(
    scope="lakebase-secrets",
    key="lakebase-password",
    string_value=getpass.getpass("Enter your Lakebase role password: ")
)

print("✅ Secrets created successfully!")
print("Secret scope: lakebase-secrets")
print("Secret keys: lakebase-host, lakebase-password")

# Grant read access to all users
w.secrets.put_acl(
    scope="lakebase-secrets",
    principal="users",
    permission=workspace.AclPermission.READ,
)

print("✅ ACL permissions set!")

# w.secrets.put_acl(
#     scope="massive",
#     principal="users",
#     permission=workspace.AclPermission.READ,
# )

