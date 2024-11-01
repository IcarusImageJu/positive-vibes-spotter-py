#!/bin/bash

# Surveillance des changements de fichiers avec entr
find . -name "*.py" | entr -r bash -c 'npx repopack && ./transfer.sh'
