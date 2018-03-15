#!/usr/bin/env python3
# coding=utf-8

from subprocess import PIPE, run
from statistics import mean

HOSTS = [
    'www.bing.com',
    'www.google.com',
    'mail.google.com',
    'www.youtube.com',
    'www.amazon.com',
    'www.amazonvideo.com',
    'd2lkq7nlcrdi7q.cloudfront.net',
    'www.walmart.com',
    'www.facebook.com',
    'connect.facebook.net',
    'staticxx.facebook.com',
    'bbc.com',
    'www.theguardian.com',
    'c.apple.news'
]

SERVERS = [
    '8.8.8.8',
    '8.8.4.4',
    '68.94.156.1',
    '68.94.157.1',
    '208.67.222.222',
    '208.67.220.220',
    '129.250.35.250',
    '129.250.35.251',
    '172.17.0.30'
]


def main():
    res = {}
    for dns in SERVERS:
        res[dns] = {'min': [], 'avg': [], 'max': [], 'stdev': []}

    for rep in range(10):
        for host in HOSTS:
            for dns in SERVERS:
                print(f'benching {host} via {dns}')
                command = f'host -4 -t A {host} {dns} | awk \'/address/{{system("ping -i 0.1 -c 10 "$4" | grep round")}}\''
                r = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
                for line in r.stdout.strip().splitlines():
                    (tmin, tavg, tmax, tstdev) = line.split()[3].split('/')
                    res[dns]['min'].append(float(tmin))
                    res[dns]['max'].append(float(tmax))
                    res[dns]['avg'].append(float(tavg))
                    res[dns]['stdev'].append(float(tstdev))

        print('')
        print('server min avg max stdev')
        for dns in res:
            print(f"{dns} {mean(res[dns]['min']):.3f} {mean(res[dns]['avg']):.3f}",
                  f"{mean(res[dns]['max']):.3f} {mean(res[dns]['stdev']):.3f}")
        print('')


if __name__ == '__main__':
    main()
