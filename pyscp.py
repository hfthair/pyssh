import os
import argparse
import subprocess


def scp(ssh_key=None, hosts_file=None, to_upload=None, target_location=None):
    hosts = []
    with open(hosts_file, 'r', encoding='utf8') as ff:
        for line in ff:
            hosts.append(line.strip())

    procs = {}
    for idx, hh in enumerate(hosts):
        if '@' not in hh:
            hh = 'ubuntu@'+hh
        cmd = ['scp', '-o', 'StrictHostKeyChecking=no', '-i', ssh_key, to_upload, hh+':'+target_location]
        print(cmd)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf8')
        procs[hh] = proc

    for proc in procs.values():
        proc.wait()

    for addr in procs:
        proc = procs[addr]
        print('=============' + addr + '==================')
        stdout, stderr = proc.communicate()
        print(stdout)
        if stderr:
            print('  ERROR:\n    ', stderr)
        print('+++++++++++++++++++++++++++++++++++++++++++')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-i', help='pem', required=True)
    parser.add_argument('-h', help='hosts files', required=True)
    parser.add_argument('-f', help='file to upload', required=True)
    parser.add_argument('-t', help='target location', required=True)
    arg = parser.parse_args()

    scp(arg.i, arg.h, arg.f, arg.t)
