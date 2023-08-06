import os

from azure.identity import ClientSecretCredential
from msgraph.core import GraphClient


class Graph:
    user_client: GraphClient
    client_credential: ClientSecretCredential
    app_client: GraphClient

    def ensure_graph_for_app_only_auth(self):
        if not hasattr(self, "client_credential"):
            client_id = os.environ["MAIL_CLIENT_ID"]
            tenant_id = os.environ["MAIL_TENANT_ID"]
            client_secret = os.environ["MAIL_CLIENT_SECRET"]

            self.client_credential = ClientSecretCredential(tenant_id, client_id, client_secret)

        if not hasattr(self, "app_client"):
            self.app_client = GraphClient(
                credential=self.client_credential, scopes=["https://graph.microsoft.com/.default"]
            )
