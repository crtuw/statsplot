#!/bin/bash
conda env export --ignore-channels --from-history | tail -r | 
tail -n +2 | tail -r > requirements.yml
