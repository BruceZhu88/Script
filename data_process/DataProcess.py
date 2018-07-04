
from itertools import dropwhile

# CA17_power_on_LED_600
# CA19_power_on_led_600
# CA19_power_off_led
path = '../data/CA19_power_on_led_600.txt'

data, t = [], []
with open(path, 'r') as f:
    for k, l in enumerate(dropwhile(
            lambda line: line.startswith('#'), f)):
        tmp = l.replace('\n', '')
        data.append(int(tmp.split(': ')[1]))
        t.append(tmp.split(': ')[0])


def avg(t, data, diff):
    i = 0
    new_data, new_t = [], []
    while i < len(data) - 2:
        print(data[i])
        a = data[i]
        b = data[i + 1]
        if abs(a - b) < diff:
            new_data.append(round((a + b) / 2, 2))
            new_t.append(t[i + 1])
            i += 2
        else:
        	new_data.append(data[i])
        	new_t.append(t[i])
        	i += 1
    return new_t, new_data

new_t, new_data = t, data

# CA17 pulse
diff = 30
for i in range(11):
	new_t, new_data = avg(new_t, new_data, diff)

'''
# ca19 pulse
for i in range(10):
	diff = 35
	new_t, new_data = avg(new_t, new_data, diff)
'''
'''
# ca19 transition
for i in range(10):
	diff = 8
	new_t, new_data = avg(new_t, new_data, diff)
'''
new_path = './data.txt'
with open(new_path, 'w') as f:
    for k, v in enumerate(new_data):
        f.write('{}: {}\n'.format(new_t[k], v))
