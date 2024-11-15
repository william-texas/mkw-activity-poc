import requests
import json
from datetime import datetime
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde
import numpy as np
import math


# setup json
chadsoft_id = input("Enter your Chadsoft ID: ")

profile = requests.get(f"http://tt.chadsoft.co.uk/players/{chadsoft_id[0:2]}/{chadsoft_id[2:]}.json") # this request will take a while
profile = json.loads(profile.content)

count = profile['ghostCount']

times = []
for i in range(count):
    time = datetime.fromisoformat(profile['ghosts'][i]['dateSet'])
    ts = time.timestamp()
    times.append(int(ts)) # turn to an integer for faster sort and KDEability
times.sort()

def bins(n):
    return math.pow(n.n, -2/3)

bandwidth = 0.005 * (times[-1] - times[0]) # can adjust for lower or higher resolution

kde = gaussian_kde(times, bw_method=bandwidth / np.std(times))
y = kde(times)
plt.plot(times, y)
def format(time, n):
    time = datetime.fromtimestamp(time)
    return time.strftime("%m/%d/%Y")

plt.xlim(times[0], times[-1])
plt.gcf().autofmt_xdate()
plt.gca().xaxis.set_major_formatter(format)
plt.title("MKW Activity Over Time")
plt.yticks([])
plt.ylabel("Activity")
plt.show()
