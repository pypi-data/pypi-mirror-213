#!/usr/bin/env python3
import os
import re
from datetime import datetime
import time

def auto_build_sw(n):
    while True:
        os.system('python3 ~/pyocs/pyocs/customers/customer_sqy/ApkSign/main.py')
        time.sleep(n)
        
def main():
    auto_build_sw(300)

if __name__ == "__main__":
    main()
