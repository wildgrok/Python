# mapreduce example
# last modified:
# 2/26/2015: fixed describe funcion (added float conversion)

from collections import namedtuple
from math import fsum

def map_reduce(data, mapper, reducer=None):
    '''Simple map/reduce for data analysis.

    Each data element is passed to a *mapper* function.
    The mapper returns key/value pairs
    or None for data elements to be skipped.

    Returns a dict with the data grouped into lists.
    If a *reducer* is specified, it aggregates each list.

    >>> def even_odd(elem):                     # sample mapper
    ...     if 10 <= elem <= 20:                # skip elems outside the range
    ...         key = elem % 2                  # group into evens and odds
    ...         return key, elem

    >>> map_reduce(range(30), even_odd)         # show group members
    {0: [10, 12, 14, 16, 18, 20], 1: [11, 13, 15, 17, 19]}

    >>> map_reduce(range(30), even_odd, sum)    # sum each group
    {0: 90, 1: 75}

    '''
    d = {}
    for elem in data:
        r = mapper(elem)
        if r is not None:
            key, value = r
            if key in d:
                d[key].append(value)
            else:
                d[key] = [value]
    if reducer is not None:
        for key, group in d.items():
            d[key] = reducer(group)
    return d

Summary = namedtuple('Summary', ['n', 'lo', 'mean', 'hi', 'std_dev'])

def describe(data1):
    'Simple reducer for descriptive statistics'
    data = []
    for x in data1:
        data.append(float(x))
    n = len(data)
    lo = min(data)
    hi = max(data)
    mean = fsum(data) / n
    std_dev = (fsum((x - mean) ** 2 for x in data) / n) ** 0.5
    return Summary(n, lo, mean, hi, std_dev)

def ReadCSV(filename):
    import csv, sys
    ary = []
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
               # print(row)
                ary.append(row)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
        return ary


def ReadPatientCSV(filename):
    """
    Usage:
    k = ReadPatientCSV(r'temperatures.csv')
    print('------')
    pprint(k)
    """
    from collections import namedtuple
    import csv, sys

    persons = []
    Person = namedtuple('Patient', ['name', 'date', 'time', 'temp'])
    i = 0
    try:
        for emp in map(Person._make, csv.reader(open(filename, "r"))):
            if i > 0:                   # skipping line with headers
                persons.append(emp)
            i = i + 1
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(filename, csv.reader.line_num, e))
    return persons


if __name__ == '__main__':

    from pprint import pprint
    import doctest
    filename = 'temperatures.csv'

    # Person = namedtuple('Person', ['name', 'gender', 'age', 'height'])
    # Person = namedtuple('Patient', ['name', 'date', 'time', 'temp'])

    # persons = [
    #     Person('mary', '1/22','7:30am' ,97),
    #     Person('suzy', '1/22','6:30pm' ,97),
    #     Person('jane', '1/23','7:30am' ,98.8),
    #     Person('jill', '1/26','10:00pm',98.1),
    #     Person('bess', '1/27','7:30am' ,96.2),
    #     Person('john', '1/27','6:30pm' ,94.4),
    #     Person('jack', '1/28','7:30am' ,96.9),
    #     Person('mike', '1/28','7:30pm' ,96.1),
    #     Person('zack', '1/29','7:30am' ,96.8),
    # ]

    # persons = [
    #     Person('jorge', '1/22','7:30am' ,97),
    #     Person('jorge', '1/22','6:30pm' ,97),
    #     Person('jorge2', '1/22','7:30am' ,97),
    #     Person('jorge2', '1/22','6:30pm' ,97.7),
    #     Person('jorge', '1/23','7:30am' ,98.8),
    #     Person('jorge', '1/26','10:00pm',98.1),
    #     Person('jorge', '1/27','7:30am' ,96.2),
    #     Person('jorge', '1/27','6:30pm' ,94.4),
    #     Person('jorge2', '1/27','7:30am' ,96.5),
    #     Person('jorge2', '1/27','6:30pm' ,94.4),
    #     Person('jorge', '1/28','7:30am' ,96.9),
    #     Person('jorge', '1/28','7:30pm' ,96.1),
    #     Person('jorge2', '1/28','7:30pm' ,95.1),
    #     Person('jorge', '1/29','7:30am' ,96.8),
    # ]


    # def height_by_gender_and_agegroup(p):
    #     key = p.gender, p.age //10
    #     val = p.height
    #     return key, val

    def temp_by_date_and_timegroup(p):
        key = p.date, p.time[-2:] #//10
        val = p.temp
        return key, val


    persons = ReadPatientCSV(filename)


    # pprint(persons)                                                      # upgrouped dataset
    # pprint(map_reduce(persons, lambda p: ((p.gender, p.age//10), p)))    # grouped people
    # pprint(map_reduce(persons, height_by_gender_and_agegroup, None))     # grouped heights
    # pprint(map_reduce(persons, height_by_gender_and_agegroup, len))      # size of each group
    # pprint(map_reduce(persons, height_by_gender_and_agegroup, describe)) # describe each group
    # print(doctest.testmod())

    print('upgrouped dataset')
    pprint(persons)                                                      # upgrouped dataset
    print('grouped people by date and am/pm')
    pprint(map_reduce(persons, lambda p: ((p.date, p.time[-2:]), p)))    # grouped people
    print('grouped temp by date and am/pm')
    pprint(map_reduce(persons, temp_by_date_and_timegroup, None))     # grouped temp
    print('size of each group')
    pprint(map_reduce(persons, temp_by_date_and_timegroup, len))      # size of each group
    print('describe each group')
    pprint(map_reduce(persons, temp_by_date_and_timegroup, describe)) # describe each group
    print(doctest.testmod())

