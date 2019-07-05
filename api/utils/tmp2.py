from __future__ import division
import math
import sys


def progressbar(cur, total):
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write('[%-50s] %s' % ('=' * int(math.floor(cur * 50 / total)), percent))
    sys.stdout.flush()
    if cur == total:
        sys.stdout.write('\n')


if __name__ == '__main__':
    file_size = 102400000
    size = 1024
    while file_size > 0:
        progressbar(size * 10 / file_size, 10)
        file_size -= 1024