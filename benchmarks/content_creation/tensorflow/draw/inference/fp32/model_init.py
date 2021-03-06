#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: EPL-2.0
#


import os
import sys
from common.base_model_init import BaseModelInitializer
from common.base_model_init import set_env_var


class ModelInitializer(BaseModelInitializer):
    """ Model initializer for the DRAW model """

    def __init__(self, args, custom_args=[], platform_util=None):
        self.args = args
        self.custom_args = custom_args
        self.platform_util = platform_util

        # Set KMP env vars, if they haven't already been set
        self.set_kmp_vars()
        set_env_var("KMP_HW_SUBSET", "1T")

        if self.args.accuracy_only:
            print("Accuracy testing for DRAW inference is not supported yet.")
            sys.exit(1)

        # Set the num_inter_threads and num_intra_threads
        self.set_default_inter_intra_threads(self.platform_util)

        # Create the command prefix with numactl and executing the script
        script_path = os.path.join(self.args.intelai_models, self.args.mode,
                                   self.args.precision, "draw_inf.py")
        self.command_prefix = self.get_numactl_command(args.socket_id) + \
            " python {} ".format(script_path)

        # Add additional args to the command
        self.command_prefix += "--cp {} --num_inter_threads {} " \
                               "--num_intra_threads {} --bs {} --dl {} " \
                               "--nw 100 --nb 200".\
            format(self.args.checkpoint, self.args.num_inter_threads,
                   self.args.num_intra_threads, self.args.batch_size,
                   self.args.data_location)

    def run(self):
        self.run_command(self.command_prefix)
