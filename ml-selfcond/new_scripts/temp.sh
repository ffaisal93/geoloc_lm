#!/bin/bash
echo "Bash version ${BASH_VERSION}..."
for i in {310394..310435}
do
    scancel ${i}
done
