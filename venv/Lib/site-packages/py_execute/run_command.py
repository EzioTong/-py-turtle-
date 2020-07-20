'''
Main application entry point
Note: If you execute a command that needs user_input and has
      a long output it may hang, try to avoid commands with input when possible
'''

from subprocess import Popen, PIPE, STDOUT
import platform
import os
from process_executor import execute as execute_process


def execute(cmd, user_input=None, env=None):
    '''
    Execute external process
    Params:
        user_input: string, ending in '\n'
                    e.g. 'name\npwd\n'
        env: dict containint environment
    '''
    user_input = user_input or []
    if env is None:
        env = os.environ

    if not user_input:
        _, out = execute_process(cmd, env=env)
    elif platform.system() != 'Windows':
        out = execute_unix(cmd, user_input, env=env)
    else:
        out = execute_windows(cmd, user_input, env=env)
    return out


def execute_unix(cmd, user_input, env):
    proc = Popen(cmd, shell=True, bufsize=1, stdout=PIPE,
                 stdin=PIPE, stderr=STDOUT, env=env)
    if user_input:
        proc.stdin.write(user_input)
    output = []

    while True:
        line = proc.stdout.readline()
        if not line:
            break
        output.append(line)
        print line
    out, err = proc.communicate()
    if out:
        output.append(out)
    err = err or ""
    output = ''.join(output)
    out = output + '\n' + err
    print out
    return out


def execute_windows(cmd, user_input, env):
    proc = Popen(cmd, shell=True, bufsize=1, stdout=PIPE,
                 stdin=PIPE, stderr=STDOUT, env=env)
    out, err = proc.communicate(input=user_input)
    err = err or ""
    print out
    print err
    return out + '\n' + err
