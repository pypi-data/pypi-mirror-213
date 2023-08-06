# -*- coding: utf-8 -*-
"""Wrapper around default AWS SDK for using Systems Manager Parameter Store."""
import os
from typing import Union
import boto3
from botocore.exceptions import ClientError

# noinspection PyPackageRequirements
from aws_lambda_powertools import Logger

LOGGER = Logger(sampling_rate=float(os.environ["LOG_SAMPLING_RATE"]), level=os.environ["LOG_LEVEL"])


class SSMService:
    """Wrapper around default AWS SDK for using Systems Manager Parameter
    Store."""

    def __init__(self, region_name: str = "eu-west-1"):
        """Class init.

        :param region_name: The AWS region name which contain SSM Parameter store keys.
        """
        self.__ssm = boto3.client("ssm", region_name=region_name)

    def get_parameter(self, parameter: str, with_decryption: bool = True) -> Union[str, None]:
        """Get single value from the AWS SSM parameter store key.

        :param parameter: The name of AWS SSM parameter store key
        :param with_decryption: Default true to encrypt parameter store key via the AWS KMS key
        :return: the parameter store key value or None if key can't be gathered
        """
        try:
            response = self.__ssm.get_parameter(Name=parameter, WithDecryption=with_decryption)
            LOGGER.info(f"Got param {parameter} from ssm")
            return response["Parameter"]["Value"]
        except ClientError:
            LOGGER.error(
                f"Failed to get SSM param {parameter}",
            )
            raise

    def get_parameters(self, parameters: list, with_decryption: bool = True) -> list:
        """Get multiple SSM parameter store keys.

        :param parameters: list of SSM parameter store keys
        :param with_decryption:
        :return: list of the AWS SSM parameter store keys value
        """
        return [self.get_parameter(x, with_decryption) for x in parameters]

    def get_parameters_dict(self, parameters, with_decryption: bool = True) -> dict:
        """Create dictionary with key as the ssm parameter store name and value
        as it's key.

        :param parameters:
        :param with_decryption: default true to encrypt ssm parameters via kms key
        :return: Return dictionary of multiple ssm parameter store entries
        """
        try:
            LOGGER.info(f"Getting params {parameters} from ssm")
            ssm_parameters = []
            parameters = parameters.copy()
            while len(parameters) > 0:
                params = parameters[:10]
                del parameters[:10]
                ssm_parameters.extend(
                    self.__ssm.get_parameters(Names=params, WithDecryption=with_decryption)["Parameters"]
                )

            return {param["Name"]: param["Value"] for param in ssm_parameters}
        except ClientError:
            LOGGER.error(
                f"Failed to get SSM params {parameters}",
            )
            raise

    def delete_parameter(self, parameter_name: str):
        """Delete parameter.

        :param parameter_name:
        :return:
        """
        try:
            LOGGER.info(f"Deleting parameter for {parameter_name}")
            self.__ssm.delete_parameter(Name=parameter_name)
        except Exception as error:
            LOGGER.error(f"Failed to delete SSM parameter {parameter_name} {error}")
            raise

    def create_parameter(
        self,
        parameter_name: str,
        description: str,
        key_id: str,
        value: str,
        parameter_type: str = "SecureString",
    ):
        """Create encrypted parameter in SSM.

        :param parameter_name: parameter path
        :param description:
        :param key_id:
        :param value:
        :param parameter_type: String or SecureString, default SecureString
        :return:
        """
        try:
            LOGGER.info(f"Creating parameter for {parameter_name}")
            self.__ssm.put_parameter(
                Name=parameter_name,
                Description=description,
                Value=value,
                Type=parameter_type,
                KeyId=key_id,
                Overwrite=True,
            )
        except Exception as error:
            LOGGER.error(f"Failed to create SSM parameter {parameter_name} {error}")
            raise
