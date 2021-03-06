# Copyright (c) 2020 Cloudify Platform Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from cloudify.decorators import operation
from cloudify.exceptions import NonRecoverableError

from decorators import with_serverless


def _download_handlers(ctx, handler_path, target_path):
    ctx.download_resource(handler_path, target_path)


@operation
@with_serverless
def create(ctx, serverless, **_):
    serverless.create()


@operation
@with_serverless
def configure(ctx, serverless, **_):
    for function in serverless.functions:
        if not function.get('path'):
            raise NonRecoverableError('Function patt does not exist')

        filename = function['path'].split('/')[-1]
        _download_handlers(
            ctx,
            function['path'],
            os.path.join(serverless.serverless_base_dir, filename)
        )

    serverless.configure()


@operation
@with_serverless
def start(ctx, serverless, **_):
    serverless.deploy()


@operation
@with_serverless
def stop(ctx, serverless, **_):
    serverless.destroy()


@operation
@with_serverless
def delete(ctx, serverless, **_):
    serverless.clean()


@operation
@with_serverless
def invoke(ctx, serverless, functions):
    for function in functions:
        serverless.invoke(function)
