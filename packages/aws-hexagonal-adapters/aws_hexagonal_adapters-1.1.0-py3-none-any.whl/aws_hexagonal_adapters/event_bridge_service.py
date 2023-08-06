# -*- coding: utf-8 -*-
"""Abstraction layer on top of AWS Event Bridge."""
import os
import boto3

# noinspection PyPackageRequirements
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

LOGGER = Logger(sampling_rate=float(os.environ["LOG_SAMPLING_RATE"]), level=os.environ["LOG_LEVEL"])


class EventsService:
    """Main class to handle AWS EventBridge communication."""

    def __init__(self, event_bus_name, region_name: str):
        """Initialize default class variables - boto3 client for events.

        :param event_bus_name: The AWS Event Bus name.
        """
        self.__client = boto3.client("events", region_name=region_name)
        self.event_bus_name = event_bus_name

    def put_event(self, item: dict):
        """Put json event to the Event Bridge Bus.

        :param item: json data
        :return:
        """
        try:
            item["EventBusName"] = self.event_bus_name

            self.__client.put_events(Entries=[item])
        except ClientError as error:
            LOGGER.error(f"Failed to put event: {repr(error)} into EventBridge: {self.event_bus_name}")
            raise
