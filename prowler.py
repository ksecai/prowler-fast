#!/usr/bin/env python3

import sys
import time

from prowler.__main__ import prowler

if __name__ == "__main__":
    start_time = time.time()
    #sys.exit(prowler())
    prowler()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

