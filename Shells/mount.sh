#!/usr/bin/env bash

set -euo pipefail

PORT=1337
MOUNTPOINT=/Users/Soren/Documents/Uddannelse/DIKU/År3/Bachelor/VmBox/

# mkdir local

sshfs \
  archimedes@localhost:.  \
  ${MOUNTPOINT} \
  -ocache=no \
  -onolocalcaches \
  -ovolname=ssh \
  -oport=${PORT} 
