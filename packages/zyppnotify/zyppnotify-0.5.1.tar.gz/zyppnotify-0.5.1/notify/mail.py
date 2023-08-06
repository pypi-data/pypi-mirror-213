import base64
import logging
import os
from urllib import request

import pandas as pd

from notify.msgraph import Graph
from notify.utils import check_environment_variables, dataframe_to_html


class NotifyMail:
    def __init__(
        self,
        to: str,
        subject: str,
        message: str,
        cc: str = None,
        bcc: str = None,
        files: dict = None,
        df: pd.DataFrame = pd.DataFrame(),
    ):
        """
        This function sends an e-mail from Microsoft Exchange server

        Parameters
        ----------
        to: str
            the e-mail adress to send email to
        subject: str
            subject of the message
        message:
            HTML or plain text content of the message
        cc: str
            e-mail address to add as cc
        bcc: str
            e-mail address to add as bcc
        files: str, list
            Path(s) to file(s) to add as attachment
        df: pd.DataFrame
            dataframe that needs to be added to the HTML message.
        """

        check_environment_variables(["EMAIL_USER", "MAIL_TENANT_ID", "MAIL_CLIENT_ID", "MAIL_CLIENT_SECRET"])
        self.sender = os.environ.get("EMAIL_USER")
        self.to = to.replace(";", ",")
        self.cc = cc.replace(";", ",") if cc is not None else cc
        self.bcc = bcc.replace(";", ",") if bcc is not None else bcc
        self.subject = subject
        self.message = message
        self.files = [files] if isinstance(files, str) else files
        self.df = df
        self.graph = Graph()
        self.graph.ensure_graph_for_app_only_auth()

    @staticmethod
    def read_file_content(path):
        if path.startswith("http") or path.startswith("www"):
            with request.urlopen(path) as download:
                content = base64.b64encode(download.read())
        else:
            with open(path, "rb") as f:
                content = base64.b64encode(f.read())

        return content

    def send_email(self):
        """
        This function sends an e-mail from Microsoft Exchange server

        Returns
        -------
        response: requests.Response
        """
        endpoint = f"https://graph.microsoft.com/v1.0/users/{self.sender}/sendMail"

        msg = {
            "Message": {
                "Subject": self.subject,
                "Body": {"ContentType": "HTML", "Content": self.message},
                "ToRecipients": [{"EmailAddress": {"Address": to.strip()}} for to in self.to.split(",")],
            },
            "SaveToSentItems": "true",
        }

        if self.cc:
            msg["Message"]["CcRecipients"] = [{"EmailAddress": {"Address": cc.strip()}} for cc in self.cc.split(",")]
        if self.bcc:
            msg["Message"]["BccRecipients"] = [
                {"EmailAddress": {"Address": bcc.strip()}} for bcc in self.bcc.split(",")
            ]

        # add html table (if table less than 30 records)
        if self.df.shape[0] in range(1, 31):
            html_table = dataframe_to_html(df=self.df)
        elif self.df.shape[0] > 30:
            logging.warning(f"Only first 30 records will be added. ({self.df.shape[0]} > the limit of 30).")
            html_table = dataframe_to_html(df=self.df.head(n=30))
        else:
            html_table = ""  # no data in dataframe (0 records)

        msg["Message"]["Body"]["Content"] += html_table

        if self.files:
            # There might be a more safe way to check if a string is an url, but for our purposes, this suffices.
            attachments = list()
            for name, path in self.files.items():
                content = self.read_file_content(path)
                attachments.append(
                    {
                        "@odata.type": "#microsoft.graph.fileAttachment",
                        "ContentBytes": content.decode("utf-8"),
                        "Name": name,
                    }
                )

            msg["Message"]["Attachments"] = attachments

        response = self.graph.app_client.post(endpoint, json=msg)
        return response
