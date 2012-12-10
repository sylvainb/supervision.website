#!/bin/bash
# ./test-module.sh
# ===> create virtualenv, install the module
# ./test-set-buildout.sh clean
# ===> ATTENTION: remove virtualenv files, create virtualenv, and install the module

function print() 
{
    echo ''
    echo '================================================'
    echo $1
    echo '================================================'
    echo ''
}

if [ $1 == clean ]; then 
  if [ -f bin/python ]; then
      print "Remove virtualenv files"
      rm -rf bin htmlcov include lib man .coverage .Python
  fi
fi

if [ ! -f bin/python ]; then
    print "Install a virtual in the current directory"
    virtualenv .
    source bin/activate
    easy_install -U setuptools
    easy_install -U distribute
fi

print "Install the module"
source bin/activate
pip install -e .
pip install coverage
pip install nose

