import sys

id_load = {}
id_url = {}
file = sys.argv[1]
f = open(file, 'r').readlines()

del f[-1]

for line in f:
    line =line.split('\t')
    Sent = True if line[0] == 'Sent' else False
    reqId = line[1]
    url = line[2]
    time = float(line[3])
    if Sent:
        id_load[reqId] = [time]
        id_url[reqId] = url
    else:
        id_load[reqId].append(time)

id_load = sorted(id_load.items(), key=lambda item: item[0])
time_count = []
for reqId, times in id_load:
    if len(times) > 1:
        print('{}: {}'.format(id_url[reqId], (times[1] - times[0]) * 1000))
        time_count.append((times[1] - times[0]) * 1000)
time_count.sort()
for time in time_count:
    print(time)

print('\n')
print(sum(time_count))