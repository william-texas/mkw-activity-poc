import requests
import json
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import dates
from scipy.stats import gaussian_kde
import numpy as np
import math

# helpers
def format(time, n):
    time = datetime.fromtimestamp(time)
    return time.strftime("%m/%d/%Y")

def bins(n):
    return math.pow(n.n, -2/3)

# setup profile json
chadsoft_id = input("Enter your Chadsoft ID: ")
print("Waiting for Chadsoft...")
profile = requests.get(f"http://tt.chadsoft.co.uk/players/{chadsoft_id[0:2]}/{chadsoft_id[2:]}.json") # this request will take a while
profile = json.loads(profile.content)

# unix-timestampify each ghosts upload date
count = profile['ghostCount']
times = []
for i in range(count):
    time = datetime.fromisoformat(profile['ghosts'][i]['dateSet'])
    ts = time.timestamp()
    times.append(int(ts)) # turn to an integer for faster sort and KDEability
times.sort()

# generate plot data / perform kde and trend
bandwidth = 0.005 * (times[-1] - times[0]) # can adjust for lower or higher resolution
kde = gaussian_kde(times, bw_method=bandwidth / np.std(times))
x = np.linspace(times[0], int(datetime.now().timestamp()), count) # linspace ensures we KDE even the latest dates with 0 ghosts set
x_dates = [datetime.fromtimestamp(i) for i in x] # mpl has built in dates as data so we can use a datetime
y = kde(x)
coefficients = np.polyfit(x, y, 1)
trend = np.polyval(coefficients, x)

# setup fig
plt.plot(x_dates, y)
plt.plot(x_dates, trend, "r--") # red dashed line
plt.title("MKW Activity Over Time")

# setup x axis
ax = plt.gca()
ax.xaxis.set_major_formatter(dates.DateFormatter("%m/%d/%Y"))
plt.gcf().autofmt_xdate()
plt.xlim(min(x_dates), max(x_dates))

#setup y axis
plt.ylim(0, max(y))
plt.yticks([])
plt.ylabel("Activity")

plt.show()