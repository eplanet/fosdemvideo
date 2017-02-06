#!/bin/bash

PYVENV=pyvenv

[ ! -d $PYVENV ] && virtualenv --python=/usr/bin/python3 $PYVENV
source $PYVENV/bin/activate

