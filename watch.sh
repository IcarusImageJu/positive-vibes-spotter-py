#!/bin/bash

# Surveillance des changements de fichiers avec entr
find . -name "*.py" | entr ./transfer.sh