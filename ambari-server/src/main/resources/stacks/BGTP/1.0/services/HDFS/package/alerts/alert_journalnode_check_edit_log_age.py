#!/usr/bin/env python

import os
import sys
import time
import glob
import argparse

RESULT_STATE_OK = 'OK'
RESULT_STATE_CRITICAL = 'CRITICAL'
RESULT_STATE_UNKNOWN = 'UNKNOWN'

def parse_args():
    parser = argparse.ArgumentParser(description="Check JournalNode edit log age")
    parser.add_argument("--edits_dir", default="/hadoop/hdfs/journal/mycluster/current",
                        help="Directory with edit logs")
    parser.add_argument("--max_age", type=int, default=10,
                        help="Maximum allowed age in minutes")
    return parser.parse_args()

def main():
    args = parse_args()
    edits_dir = args.edits_dir
    max_age = args.max_age

    try:
        edit_logs = sorted(glob.glob(os.path.join(edits_dir, "edits*")), key=os.path.getmtime, reverse=True)
    except Exception as e:
        print("UNKNOWN: Failed to read edit logs: {}".format(str(e)))
        return RESULT_STATE_UNKNOWN

    if not edit_logs:
        print("CRITICAL: No edit logs found in {}".format(edits_dir))
        return RESULT_STATE_CRITICAL

    latest_file = edit_logs[0]

    try:
        mtime = os.path.getmtime(latest_file)
    except Exception as e:
        print("UNKNOWN: Failed to stat file {}: {}".format(latest_file, str(e)))
        return RESULT_STATE_UNKNOWN

    now = time.time()
    age_minutes = int((now - mtime) / 60)

    if age_minutes >= max_age:
        print("CRITICAL: Latest edit log is {} minutes old".format(age_minutes))
        return RESULT_STATE_CRITICAL
    else:
        print("OK: Latest edit log is {} minutes old".format(age_minutes))
        return RESULT_STATE_OK

if __name__ == "__main__":
    main()
