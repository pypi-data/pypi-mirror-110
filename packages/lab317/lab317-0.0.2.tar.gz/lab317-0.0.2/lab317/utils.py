from datetime import datetime as D

def is_bq_format(m):
    if type(m) != str or '_' not in m:
        print('Date not in BQ string format. expected_format: 2012_01 got: ' + str(m))
        return False

    date = m.split('_')
    y = int(date[0])
    m = int(date[1])
    
    if len(m) != 2:
        print('Date not in BQ string format. expected_format: 2012_01 got: ' + str(m))
        return False

    if len(y) != 4:
        print('Date not in BQ string format. expected_format: 2012_01 got: ' + str(m))
        return False

    return True


def convert_integer_date(m):
    if type(m) != int:
        raise Exception('Month already in string. month: ' + str(m))
    if len(str(m)) != 6:
        raise Exception('Expected month to be in this formar: 201201 gor: ' + str(m))

    m = str(m)
    y = m[0:4]
    m = m[4:]
    return y + '_' + m


def convert_date(y, m):
    if type(m) != int:
        raise Exception('Month already in string. month: ' + str(m))
    if type(y) != int:
        raise Exception('Year already in string. year: ' + str(y))

    m = str(m)
    if len(m) == 1:
        m = '0' + m

    return str(y) + '_' + m


def increment_date(m):
    """
    Input month is in BQ string format
    """

    if type(m) != str or '_' not in m:
        raise Exception('Month not in BQ string format. expected_format: 2012_01 got: ' + str(m))

    date = m.split('_')
    y = int(date[0])
    m = int(date[1])

    if m == 12:
        y += 1
        m = 1
    else:
        m += 1


    return convert_date(y, m)


def date_to_utc(y, m, d=1, h=1, shift=0):
    date = D(y, m, d, h)
    date = date.timestamp()
    return str(int(date+shift))



def get_all_weeks(W):
    _ = []
    weeks = []
    for w in W.keys():
        for i in W[w]:
            weeks.append(i['start'])
            _.append(i['end'])

    weeks.append(_[-1])
    return weeks

def get_weeks(M, G):
    G = 4
    dates = []
    months = M[:]
    months.append(get_next_month(months[-1]))

    for m in months:
        dates.append(D.strptime(m, '%Y_%m'))

    weeks = dict()
    tz = D.utcnow().astimezone().utcoffset().total_seconds()

    for i, date in enumerate(dates[:-1]):
        start = date
        end = dates[i+1]
        
        start_epoch = start.timestamp() + tz
        end_epoch = end.timestamp() + tz
        
        inc = (end_epoch - start_epoch)/G
        
        weeks[months[i]] = [] 
        
        for k in range(0, G):
            s = start_epoch + (inc*k)
            e = s + inc

            s = int(s)
            e = int(e)
            
            week_range = dict()
            week_range['start'] = s
            week_range['end'] = e
            week_range['mid'] = int((e-s)/2) + s
            weeks[months[i]].append(week_range)

    return weeks       

def get_months(start, end):
    s = start.split('_')
    e = end.split('_')
    sy, sm = int(s[0]), int(s[1])
    ey, em = int(e[0]), int(e[1])

    if sy == ey:
        if sm > em:
            return [] 
        if sm == em:
            return [start]
    if ey < sy:
        return []

    dates = []

    while sy < ey:
        if sm < 10:
            dates.append(str(sy) + '_0' + str(sm))
        else:
            dates.append(str(sy) + '_' + str(sm))

        if sm == 12:
            sm = 1
            sy += 1
        else:
            sm += 1


    while sm <= em:
        if sm < 10:
            dates.append(str(sy) + '_0' + str(sm))
        else:
            dates.append(str(sy) + '_' + str(sm))
        sm += 1

    return dates

