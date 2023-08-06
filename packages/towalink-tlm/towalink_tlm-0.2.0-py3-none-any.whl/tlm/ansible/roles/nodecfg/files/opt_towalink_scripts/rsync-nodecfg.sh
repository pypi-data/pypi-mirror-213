#!/bin/bash

/usr/bin/rsync "$@"
result=$?
(
  if [ $result -eq 0 ]; then
     echo $(date) >> /tmp/rsync-after
  fi
) >/dev/null 2>/dev/null </dev/null
exit $result
