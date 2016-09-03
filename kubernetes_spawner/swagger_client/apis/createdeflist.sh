#!/bin/bash

cat apisv_api.py | grep -A 3 "   def" | sed 's/self,//g' | sed 's/ \*\*kwargs//g' | sed 's/def //g' | sed 's/\"\"\"//g'
