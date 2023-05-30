#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import glob
import string
import argparse
import platform
import itertools
import subprocess
import numpy as np
from pathos.helpers import mp
from pathos.pools import ProcessPool, ThreadPool, SerialPool, ParallelPool

sys.path.append(".")

parser = argparse.ArgumentParser()
parser.add_argument("--begin_id", type=int, default=0)
parser.add_argument("--end_id", type=int, default=None)
parser.add_argument("--split_num", type=int, default=1)
parser.add_argument("--node_num", type=int, default=None)
parser.add_argument("--debug", action="store_true")
parser.add_argument("--show_std", action="store_true")
# experimental options
parser.add_argument("--target_wav_files", type=str, nargs='*', required=True)
parser.add_argument("--bucket_name", type=str, default="audio-recorder")
parser.add_argument("--languages", type=str, nargs='*')

args, unknown = parser.parse_known_args()

def for_each(func, args_list, expand=False, verbose=True):
    # wrapping functions
    def _func_wrapper(task_id, args):
        if verbose:
            print("\x1b[32mNo.{}'s task begin\x1b[0m".format(task_id + 1))
        if expand:
            return func(*args)
        else:
            return func(args)
    # main processes
    return [_func_wrapper(_id, args) for _id, args in enumerate(args_list)]


def multi_process(func, args_list, nodes=None, expand=False,
                  verbose=True, append_id=False):
    # wrapping functions
    def _func_wrapper(args):
        cp = mp.current_process()
        if verbose:
            print("\x1b[32mNo.{}'s task begin\x1b[0m".format(args[0] + 1))
        if expand:
            if append_id:
                return func(*args[1], worker_id=cp._identity)
            else:
                return func(*args[1])
        else:
            if append_id:
                return func(args[1], worker_id=cp._identity)
            else:
                return func(args[1])
    # main processes
    with ProcessPool(nodes=nodes) as p:
        try:
            res = p.amap(_func_wrapper, enumerate(args_list))
            return res.get()
        except Exception as err_msg:
            print(err_msg)
            p.terminate()
        except KeyboardInterrupt:
            p.terminate()

if __name__ == '__main__':
    def _run(_id, lang, target, worker_id=None):
        cmd = "python src/script/base/speech2textTranscript.py "
        cmd += "--input_file {} ".format(target)
        cmd += "--bucket_name {} ".format(args.bucket_name)
        cmd += "--language {} ".format(lang)
        cmd += " ".join(unknown) + " "
        print("[{}] : {}".format(_id, cmd))

        if not args.debug:
            std = None if args.show_std else subprocess.DEVNULL
            subprocess.call(
                cmd.split(), stdout=std, stderr=std)

    language_list = args.languages
    target_list = args.target_wav_files

    arg_list = list(itertools.product(language_list, target_list))
    arg_list = [(_id,) + _ for _id, _ in enumerate(arg_list)]
    arg_list = arg_list[args.begin_id:args.end_id:args.split_num]

    if args.node_num is None:
        for_each(_run, arg_list, expand=True, verbose=False)
    else:
        multi_process(_run, arg_list, verbose=False, append_id=True,
                      expand=True, nodes=args.node_num)
