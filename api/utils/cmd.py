from subprocess import call
import sys

def exec_cmd(cmd):
    call(cmd,shell=True,stdout=sys.stdout,stderr=sys.stderr)
