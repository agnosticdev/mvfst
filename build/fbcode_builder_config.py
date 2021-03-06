#!/usr/bin/env python

# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

'fbcode_builder steps to build & test mvfst'

import specs.gmock as gmock
import specs.folly as folly
import specs.fizz as fizz

from shell_quoting import ShellQuoted


def fbcode_builder_spec(builder):
    builder.add_option(
        'mvfst/_build:cmake_defines',
        {
            'BUILD_SHARED_LIBS': 'OFF',
            'BUILD_TESTS': 'ON',
        }
    )
    return {
        'depends_on': [gmock, folly, fizz],
        'steps': [
            builder.fb_github_cmake_install('mvfst/_build', '..', 'facebookincubator'),
            builder.step(
                'Run mvfst tests', [
                    builder.run(
                        ShellQuoted('ctest --output-on-failure -j {n}')
                        .format(n=builder.option('make_parallelism'), )
                    )
                ]
            ),
        ]
    }


config = {
    'github_project': 'facebookincubator/mvfst',
    'fbcode_builder_spec': fbcode_builder_spec,
}
