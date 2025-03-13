import requests
import time
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# Set this to True if you want to use a SOCKS5 proxy, otherwise False.
use_socks5 = False

# Proxy settings
if use_socks5:
    proxies = {
        'http': 'socks5://username:password@proxy.geonode.io:11009',
        'https': 'socks5://username:password@proxy.geonode.io:11009'
    }
else:
    proxies = {
        'http': 'http://username:password@proxy.geonode.io:9008',
        'https': 'http://username:password@proxy.geonode.io:9008'
    }

# Target URL
url = 'http://ip-api.com'#http://ip-api.com https://www.cloudflare.com/cdn-cgi/trace

# Number of requests to send and concurrent workers
num_requests = 5000
num_workers = 5  # Adjust as needed

# Lists to store latencies and statuses
latencies = []
statuses = []
timeouts = 0
other_errors = 0
error_messages = []

def fetch_url(i):
    global timeouts, other_errors
    try:
        start_time = time.time()  # Start the timer
        response = requests.get(url, proxies=proxies, timeout=60)
        latency = time.time() - start_time  # Calculate latency
        print(f"Request #{i+1}: Status Code: {response.status_code}, Total Latency: {latency:.2f} seconds")
        return response.status_code, latency

    except requests.exceptions.Timeout:
        print(f"Request #{i+1} timed out.")
        timeouts += 1
        error_messages.append('Timeout')
        return 'Timeout', time.time() - start_time
    except requests.exceptions.RequestException as e:
        print(f"Request #{i+1} failed: {e}")
        other_errors += 1
        error_messages.append('Error')
        return 'Error', time.time() - start_time

# Use ThreadPoolExecutor to send requests concurrently
with ThreadPoolExecutor(max_workers=num_workers) as executor:
    results = list(executor.map(fetch_url, range(num_requests)))

# Process results
for status, latency in results:
    statuses.append(status)
    latencies.append(latency)

# Plotting the results
plt.figure(figsize=(10, 6))

# Separate latencies by status code
latencies_200 = [lat for status, lat in zip(statuses, latencies) if status == 200]
latencies_not_200 = [lat for status, lat in zip(statuses, latencies) if status != 200 and status not in ['Timeout', 'Error']]
latencies_timeout = [lat for status, lat in zip(statuses, latencies) if status == 'Timeout']
latencies_error = [lat for status, lat in zip(statuses, latencies) if status == 'Error']

indices_200 = [i for i, status in enumerate(statuses) if status == 200]
indices_not_200 = [i for i, status in enumerate(statuses) if status != 200 and status not in ['Timeout', 'Error']]
indices_timeout = [i for i, status in enumerate(statuses) if status == 'Timeout']
indices_error = [i for i, status in enumerate(statuses) if status == 'Error']

plt.plot(indices_200, latencies_200, marker='o', linestyle='-', color='b', label='Status 200')
plt.plot(indices_not_200, latencies_not_200, marker='o', linestyle='-', color='r', label='Status != 200')
plt.plot(indices_timeout, latencies_timeout, marker='x', linestyle='None', color='g', label='Timeout')
plt.plot(indices_error, latencies_error, marker='x', linestyle='None', color='m', label='Error')

plt.title('Latencies of HTTP Requests Through Proxy')
plt.xlabel('Request Number')
plt.ylabel('Latency (seconds)')
plt.legend()
plt.grid(True)

# Calculate and display statistics on the plot
latencies_filtered = [lat for lat in latencies if lat is not None]
average_latency = np.mean(latencies_filtered)
median_latency = np.median(latencies_filtered)
std_dev_latency = np.std(latencies_filtered)

# Calculate status code percentages
total_requests = len(statuses)
status_counts = {status: statuses.count(status) for status in set(statuses)}
status_percentages = {status: (count / total_requests) * 100 for status, count in status_counts.items()}

# Error message counts
error_message_counts = Counter(error_messages)

# Adding text to the plot
stats_text = (
    f"Average Latency: {average_latency:.2f} seconds\n"
    f"Median Latency: {median_latency:.2f} seconds\n"
    f"Standard Deviation of Latency: {std_dev_latency:.2f} seconds\n\n"
    "Status Code Percentages:\n" +
    "\n".join([f"{status}: {percentage:.2f}%" for status, percentage in status_percentages.items()]) +
    f"\n\nTotal Requests: {num_requests}\n"
    f"Successful (Status 200): {statuses.count(200)}\n"
    f"Timeouts: {timeouts}\n"
    f"Other Errors: {other_errors}\n\n"
    "Error Messages:\n" +
    "\n".join([f"{message}: {count}" for message, count in error_message_counts.items()])
)


# Print the results in the terminal
print("\n--- Test Results ---")
print(stats_text)


plt.figtext(0.15, 0.5, stats_text, bbox=dict(facecolor='white', alpha=0.5))
plt.show()
