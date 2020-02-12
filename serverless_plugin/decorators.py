import os
import sys

from functools import wraps

from cloudify.exceptions import NonRecoverableError
from cloudify.utils import exception_to_error_cause

from serverless_sdk import Serverless, CloudifyServerlessSDKError


def with_serverless(func):
    @wraps(func)
    def function(*args, **kwargs):
        ctx = kwargs['ctx']
        operation_name = ctx.operation.name
        provider_config = ctx.node.properties['provider_config']
        executable_path = ctx.node.properties['executable_path']
        service_path = ctx.node.properties['service_path']
        functions = ctx.node.properties['functions']
        variables = ctx.node.properties['variables']
        if not os.path.exists(executable_path):
            raise NonRecoverableError(
                "Serverless's executable not found in {0}. Please set the "
                "'executable_path' property accordingly.".format(
                    executable_path))
        serverless = Serverless(
            ctx.logger,
            provider_config,
            service_path,
            executable_path,
            functions,
            variables
        )
        kwargs['serverless'] = serverless
        try:
            func(*args, **kwargs)
        except CloudifyServerlessSDKError as error:
            _, _, tb = sys.exc_info()
            raise NonRecoverableError(
                'Failure while trying to run operation'
                '{0}: {1}'.format(operation_name, error.message),
                causes=[exception_to_error_cause(error, tb)])
    return function
