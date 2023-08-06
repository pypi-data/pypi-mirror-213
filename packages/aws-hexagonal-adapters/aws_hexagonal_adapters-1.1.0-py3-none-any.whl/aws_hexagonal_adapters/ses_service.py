# -*- coding: utf-8 -*-
"""Simplify operations against AWS Simple Email Service using AWS Python SDK
boto3."""
import os
import boto3
from botocore.exceptions import ClientError
from typing import Optional

# noinspection PyPackageRequirements
from aws_lambda_powertools import Logger

LOGGER = Logger(sampling_rate=float(os.environ["LOG_SAMPLING_RATE"]), level=os.environ["LOG_LEVEL"])


class SESService:
    """Simplify sending emails - text and html with attachment via AWS Simple Email Service."""

    def __init__(self, region_name="eu-west-1"):
        """Initialize default parameters for AWS Simple Email Service.

        :param region_name: the AWS region name, default eu-west-1
        """
        self.__ses = boto3.client("ses", region_name=region_name)

    def send_email(
        self, email_body_text: str, email_body_html: str, destination: str, sender: str, subject: str
    ) -> bool:
        """Send email without attachment.

        :param destination: destination email address - recipient
        :param sender: sender email address
        :param subject: email subject
        :param email_body_text: email message in text format
        :param email_body_html: email message in html format
        :return: False/True
        """
        charset = "UTF-8"

        try:
            response = self.__ses.send_email(
                Destination={"ToAddresses": [destination]},
                Message={
                    "Body": {
                        "Html": {"Charset": charset, "Data": email_body_html},
                        "Text": {"Charset": charset, "Data": email_body_text},
                    },
                    "Subject": {"Charset": charset, "Data": subject},
                },
                Source=sender,
            )
            LOGGER.info(f"Email response: {response}")

            if response.get("ResponseMetadata").get("HTTPStatusCode") != 200:
                LOGGER.error(f"Message not sent due to: {response}")
                raise ValueError(f"Message not sent due to: {response}")
            LOGGER.info(f"Email sent! Message ID: {response['MessageId']}")
        except ClientError as e:
            LOGGER.error(e.response["Error"]["Message"])
            raise

        return True

    # pylint: disable=C0415
    def send_raw_email(
        self,
        email_body_html: str,
        destinations: list,
        sender: str,
        subject: str,
        attachment_list: Optional[list] = None,
        picture_list: Optional[list] = None,
    ) -> bool:
        """Send email message with attachment.

        :param destinations: destination list email address - recipients
        :param sender: sender email address
        :param subject: email subject
        :param picture_list:
        :param email_body_html: email message in html format
        :param attachment_list: list of strings pointing to files in local file system
        :return: False/True
        """
        from email.mime.text import MIMEText
        from email.mime.application import MIMEApplication
        from email.mime.image import MIMEImage
        from email.mime.multipart import MIMEMultipart

        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = ", ".join(destinations)

        part = MIMEText(email_body_html, "html")
        message.attach(part)

        # attachment
        if attachment_list:
            for attachment in attachment_list:
                attachment_name = attachment.split("/")[-1]
                with open(attachment, "rb") as file:
                    part = MIMEApplication(file.read())  # type: ignore
                part.add_header("Content-Disposition", "attachment", filename=attachment_name)
                message.attach(part)

        # picture attachment
        if picture_list:
            for picture in picture_list:
                picture_name = picture.split("/")[-1]
                with open(picture, "rb") as file:
                    part = MIMEImage(file.read(), name=picture_name)  # type: ignore
                message.attach(part)

        try:
            response = self.__ses.send_raw_email(
                Source=message["From"],
                Destinations=destinations,
                RawMessage={"Data": message.as_string()},
            )

            LOGGER.info(f"Response RAW email: {response}")

            if response.get("ResponseMetadata").get("HTTPStatusCode") != 200:
                LOGGER.error(f"Message not sent due to: {response}")
                raise ValueError(f"Message not sent due to: {response}")
            LOGGER.info(f"Email sent! Message ID: {response['MessageId']}")
        except ClientError as e:
            LOGGER.error(e.response["Error"]["Message"])
            raise

        return True
