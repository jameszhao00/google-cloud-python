# Copyright 2017, Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import collections
import sys
import textwrap

from google.api import http_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.iam.v1.logging import audit_data_pb2
from google.protobuf import descriptor_pb2
from google.protobuf import duration_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import timestamp_pb2

from google.api_core.protobuf_helpers import get_messages
from google.cloud.pubsub_v1.proto import pubsub_pb2


# Define the default values for batching.
#
# This class is used when creating a publisher or subscriber client, and
# these settings can be altered to tweak Pub/Sub behavior.
# The defaults should be fine for most use cases.
BatchSettings = collections.namedtuple(
    "BatchSettings", ["max_bytes", "max_latency", "max_messages"]
)
BatchSettings.__new__.__defaults__ = (
    1000 * 1000 * 10,  # max_bytes: documented "10 MB", enforced 10000000
    0.05,  # max_latency: 0.05 seconds
    1000,  # max_messages: 1,000
)

if sys.version_info >= (3, 5):
    BatchSettings.__doc__ = "The settings for batch publishing the messages."
    BatchSettings.max_bytes.__doc__ = (
        "The maximum total size of the messages to collect before automatically "
        "publishing the batch."
    )
    BatchSettings.max_latency.__doc__ = (
        "The maximum number of seconds to wait for additional messages before "
        "automatically publishing the batch."
    )
    BatchSettings.max_messages.__doc__ = (
        "The maximum number of messages to collect before automatically "
        "publishing the batch."
    )


# Define the type class and default values for flow control settings.
#
# This class is used when creating a publisher or subscriber client, and
# these settings can be altered to tweak Pub/Sub behavior.
# The defaults should be fine for most use cases.
FlowControl = collections.namedtuple(
    "FlowControl",
    [
        "max_bytes",
        "max_messages",
        "resume_threshold",
        "max_requests",
        "max_request_batch_size",
        "max_request_batch_latency",
        "max_lease_duration",
    ],
)
FlowControl.__new__.__defaults__ = (
    100 * 1024 * 1024,  # max_bytes: 100mb
    100,  # max_messages: 100
    0.8,  # resume_threshold: 80%
    100,  # max_requests: 100
    100,  # max_request_batch_size: 100
    0.01,  # max_request_batch_latency: 0.01s
    2 * 60 * 60,  # max_lease_duration: 2 hours.
)

if sys.version_info >= (3, 5):
    FlowControl.__doc__ = (
        "The settings for controlling the rate at which messages are pulled "
        "with an asynchronous subscription."
    )
    FlowControl.max_bytes.__doc__ = (
        "The maximum total size of received - but not yet processed - messages "
        "before pausing the message stream."
    )
    FlowControl.max_messages.__doc__ = (
        "The maximum number of received - but not yet processed - messages before "
        "pausing the message stream."
    )
    FlowControl.resume_threshold.__doc__ = textwrap.dedent(
        """
        The relative threshold of the ``max_bytes`` and ``max_messages`` limits
        below which to resume the message stream. Must be a positive number not
        greater than ``1.0``.

        .. note::
            .. deprecated:: 0.44.0
                Will be removed in future versions."""
    )
    FlowControl.max_requests.__doc__ = textwrap.dedent(
        """
        Currently not in use.

        .. note::
            .. deprecated:: 0.44.0
                Will be removed in future versions."""
    )
    FlowControl.max_request_batch_size.__doc__ = textwrap.dedent(
        """
        The maximum number of requests scheduled by callbacks to process and
        dispatch at a time.

        .. note::
            .. deprecated:: 0.44.0
                Will be removed in future versions."""
    )
    FlowControl.max_request_batch_latency.__doc__ = textwrap.dedent(
        """
        The maximum amount of time in seconds to wait for additional request
        items before processing the next batch of requests.

        .. note::
            .. deprecated:: 0.44.0
                Will be removed in future versions."""
    )
    FlowControl.max_lease_duration.__doc__ = (
        "The maximum amount of time in seconds to hold a lease on a message "
        "before dropping it from the lease management."
    )


_shared_modules = [
    http_pb2,
    iam_policy_pb2,
    policy_pb2,
    audit_data_pb2,
    descriptor_pb2,
    duration_pb2,
    empty_pb2,
    field_mask_pb2,
    timestamp_pb2,
]

_local_modules = [pubsub_pb2]


names = ["BatchSettings", "FlowControl"]


for module in _shared_modules:
    for name, message in get_messages(module).items():
        setattr(sys.modules[__name__], name, message)
        names.append(name)

for module in _local_modules:
    for name, message in get_messages(module).items():
        message.__module__ = "google.cloud.pubsub_v1.types"
        setattr(sys.modules[__name__], name, message)
        names.append(name)


__all__ = tuple(sorted(names))
