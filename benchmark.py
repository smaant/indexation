import math
import re

# LOG_PATTERN = re.compile(r'(?P<src>\w+).? \(n = (?P<count>\d+)(?P<total>, total)?\): (?P<time>\d+)')
LOG_PATTERN = re.compile(r'(\w+).? \(n = (\d+)\): (\d+)\n.*total\): (\d+)')


def load_data(log_name):
    f = open(log_name)
    line = f.read()
    results = LOG_PATTERN.findall(line)
    return [{'src': t[0], 'count': int(t[1]), 'total': int(t[3]),'time': int(t[2])} for t in results]


def median(mylist):
    sorts = sorted(mylist)
    length = len(sorts)
    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
    return sorts[length / 2]


def combine_results(results):
    combined = {}
    for item in results:
        src = item['src']
        if not combined.has_key(src):
            combined[src] = {}

        count = item['count']
        if not combined[src].has_key(count):
            combined[src][count] = []

        combined[src][count] += [(item['time'],item['total']), ]
    return combined

if __name__ == '__main__':
    data = combine_results(load_data('log_invert.txt'))
    for src in data:
        print(src)
        for cnt in data[src]:
            m = median([x[0] for x in data[src][cnt]])
            in_m = 0
            in_ell = []
            out_ell = []
            for t in data[src][cnt]:
                if float(math.fabs(t[0] - m)/m) <= .3:
                    in_m += 1
                    in_ell += [t,]
                else:
                    out_ell += [t,]
            # print('\t{}: {} / {} of {}'.format(cnt, m, in_m, len(data[src][cnt])))

            if in_m == 0:
                in_ell = [x[0] for x in data[src][cnt]]
            else:
                print('{}\t{}'.format(cnt, sum([x[0] for x in in_ell])/in_m, in_ell, out_ell))
        print

