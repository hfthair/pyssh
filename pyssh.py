import os
import argparse
import subprocess


def ssh(host_file=None, ssh_key=None, ssh_pwd=None, env_var_files=None, command=None):
    hosts = []
    with open(host_file, 'r', encoding='utf8') as f:
        for line in f:
            addr = line.strip()
            if addr in hosts:
                raise Exception('duplicate hosts!')
            hosts.append(addr)

    env = {}
    if env_var_files:
        for k in env_var_files:
            if not os.path.isfile(k):
                raise Exception('env file not exists', k)
            base = os.path.basename(k)
            tmp = []
            with open(k, 'r', encoding='utf8') as f:
                for line in f:
                    tmp.append(line.strip())
            env[base] = tmp

    procs = {}
    for idx, hh in enumerate(hosts):
        if '@' not in hh:
            hh = 'ubuntu@'+hh
        hc = command
        for ek in env:
            tmp = env[ek][idx]
            hc = hc.replace('{'+ek+'}', tmp)

        cmd = ['-o', 'StrictHostKeyChecking=no', hh, hc]
        if ssh_key:
            cmd = ['-i', ssh_key] + cmd
        cmd = ['ssh'] + cmd
        print(cmd)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf8')

        # todo: if not ssh_key and ssh_pwd:

        procs[hh] = proc

    output_cache = {addr: '' for addr in procs}
    def collect_output(stdout, addr, printt=False):
        tmp = []
        while True:
            out = stdout.readline()
            if not out:
                break
            tmp.append(out)

        output_cache[addr] += ''.join(tmp)
        if printt:
            print('-------')
            for out in tmp:
                print(f'[{addr}] {out}', end='')
            print('-------')

    while True:
        alldone = True
        for addr in procs:
            proc = procs[addr]
            try:
                proc.wait(timeout=3)
                collect_output(proc.stdout, addr)
            except subprocess.TimeoutExpired:
                alldone = False
                collect_output(proc.stdout, addr, printt=True)
        if alldone:
            break

    for addr in output_cache:
        output = output_cache[addr]
        print('=============' + addr + '==================')
        print(output)
        print('+++++++++++++++++++++++++++++++++++++++++++')

    print('exit code:', [procs[addr].poll() for addr in procs])
    print("***********", len(hosts), "*************")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', help='hosts files', required=True)
    parser.add_argument('-c', help='command')
    parser.add_argument('-i', help='pem')
    parser.add_argument('-p', help='password') # TODO:
    parser.add_argument('-e', help='env', nargs='*')
    arg = parser.parse_args()

    ssh(arg.h, arg.i, arg.p, arg.e, arg.c)
