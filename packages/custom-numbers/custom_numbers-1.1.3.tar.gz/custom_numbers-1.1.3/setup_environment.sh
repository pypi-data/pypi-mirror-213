#!/usr/bin/env bash
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt

echo "Now you can run inst.sh for an editable module installation"

