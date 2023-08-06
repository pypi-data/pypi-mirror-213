# -*- coding: utf-8 -*-

"""
AWS Lambda related automation.

For building layer and deployment package automation, please refer to
`aws_lambda_layer <https://github.com/MacHu-GWU/aws_lambda_layer-project>`_
project.
"""

import typing as T
import dataclasses
from pathlib_mate import Path


if T.TYPE_CHECKING:
    from .ops import PyProjectOps


@dataclasses.dataclass
class PyProjectAWSLambda:
    """
    Namespace class for AWS Lambda related automation.
    """

    @property
    def dir_build_lambda(self: "PyProjectOps") -> Path:
        """
        The AWS Lambda artifacts build folder.

        Example: ``${dir_project_root}/build/lambda``
        """
        return self.dir_build.joinpath("lambda")

    @property
    def dir_build_lambda_python(self) -> Path:
        """
        The AWS Lambda layer build folder. This folder contains the dependencies.

        Example: ``${dir_project_root}/build/lambda/python``
        """
        return self.dir_build_lambda.joinpath("python")

    @property
    def path_build_lambda_bin_aws(self) -> Path:
        """
        This is the AWS CLI executable path in Lambda layer.

        Example: ``${dir_project_root}/build/lambda/python/aws``
        """
        return self.dir_build_lambda_python.joinpath("aws")

    @property
    def path_build_lambda_source_zip(self) -> Path:
        """
        The AWS Lambda source code deployment package zip file path.

        Example: ``${dir_project_root}/build/lambda/source.zip``
        """
        return self.dir_build_lambda.joinpath("source.zip")

    @property
    def path_build_lambda_layer_zip(self) -> Path:
        """
        The AWS Lambda layer zip file path.

        Example: ``${dir_project_root}/build/lambda/layer.zip``
        """
        return self.dir_build_lambda.joinpath("layer.zip")

    @property
    def dir_lambda_app(self: "PyProjectOps") -> Path:
        """
        The AWS Lambda app handler file and Lambda related code directory.

        Example: ``${dir_project_root}/lambda_app``
        """
        return self.dir_project_root.joinpath("lambda_app")

    @property
    def path_chalice_config(self) -> Path:
        """
        The AWS Chalice framework's config file path.

        Example: ``${dir_project_root}/lambda_app/.chalice/config.json``

        See: https://aws.github.io/chalice/topics/configfile.html
        """
        return self.dir_lambda_app.joinpath(".chalice", "config.json")

    @property
    def dir_lambda_app_vendor(self) -> Path:
        """
        The vendor folder for AWS Chalice framework's packaging.

        Example: ``${dir_project_root}/lambda_app/vendor``

        See: https://aws.github.io/chalice/topics/packaging.html
        """
        return self.dir_lambda_app.joinpath("vendor")

    @property
    def dir_lambda_app_deployed(self) -> Path:
        """
        The generated ``deployed.json`` file for AWS Chalice framework's.

        Example: ``${dir_project_root}/lambda_app/.chalice/deployed``
        """
        return self.dir_lambda_app.joinpath(".chalice", "deployed")

    @property
    def path_lambda_update_chalice_config_script(self) -> Path:
        """
        Example: ``${dir_project_root}/lambda_app/update_chalice_config.py``
        """
        return self.dir_lambda_app.joinpath("update_chalice_config.py")

    @property
    def path_lambda_app_py(self) -> Path:
        """
        The app.py file for AWS Chalice framework.

        Example: ``${dir_project_root}/lambda_app/app.py``
        """
        return self.dir_lambda_app.joinpath("app.py")

    @property
    def path_lambda_function_py(self) -> Path:
        """
        The lambda_function.py handler file for AWS Lambda, if you are not using
        framework.

        Example: ``${dir_project_root}/lambda_app/app.py``
        """
        return self.dir_lambda_app.joinpath("lambda_function.py")
