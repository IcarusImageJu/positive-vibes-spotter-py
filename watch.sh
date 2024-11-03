#!/bin/bash

# Surveillance des changements de fichiers avec entr
find . -name "*.py" | entr -r bash -c 'npx repomix && ./transfer.sh'
