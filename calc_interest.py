
invest = 10000
capital = 10000
rate = 0.053 / 365
year = 1
interest = 0
for i in range(year * 365):
    if i % 365 == 0 and i != 0:
        capital += invest
    interest_now = (interest + capital) * rate
    interest = interest + interest_now
    print('{} day interest = {}'.format(i + 1, interest_now))

total = invest * year + interest

print('interest = {}'.format(interest))
print('total = {}'.format(total))
