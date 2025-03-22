# "success-latency.py" Proxy Testing Script: 

This repository contains a combined script utilizing python requests library to help you test the latency and success rate of your proxies. The scripts support both **SOCKS5** and **HTTPS** proxies, and they use [ip-api.com](http://ip-api.com) as the default target to gather testing information.

You can consider other targets and benchmark its results, for example: https://www.cloudflare.com/cdn-cgi/trace

It is recommended to perform tests using a rotating port configuration. This setup causes the proxy IP to change with every request, providing an average measurement across a range of IP addresses rather than a single one.

## Overview

  Measures average, minimum, and maximum latency across multiple requests. It also logs any failed requests with error messages.

  Calculates the overall success rate of proxy requests and logs detailed information about any failed requests.

The script allow you to set the following variables:

- **Target Country:** (User-defined; leave blank ( do not append -country- ) for a random pool)
- **Protocol:** Choose between HTTP, HTTPS, or SOCKS5 ( default is HTTP/HTTPS )
- **Session Type:** Rotating (default) 
- **Target URL:** The URL to test against (default is set to [ip-api.com](http://ip-api.com))
- **Number of Requests:** Adjust for your testing needs  
  > **Recommendation:** For accurate results, run at least 2000 requests and use 5-10 threads.
- **Note: The test results can vary depending on the Gateway you are choosing as the proxy address. We currently offer 3 gateways location. 
- **Default gateway: proxy.geonode.io -> Europe, FR


## Note out port assignment:

	Rotating Ports:
	- HTTP/HTTPS: 9000 - 9010
	- SOCKS5: 11000 - 11010
	Sticky Ports:
	- HTTP/HTTPS: 10000 - 10900
	- SOCKS5: 12000 - 12010
	
	Rotating ports will change your IP on every request sent.
	
	Sticky ports enable you to maintain the same IP for any duration that you assign on the dashboard. 


## Default Settings

- **Protocol:** Use SOCKS5 = false or HTTPS as required.
- **Target:** [ip-api.com](http://ip-api.com) – our baseline for IP information.
- **Concurrency:** 5-10 threads (adjustable in the script)
- **Testing Volume:** At least 2000 requests for accuracy

## Installation

1. **Clone the Repository:**


## Result Output:

After running the script, you'll see a summary similar to the following alongside a pie chart:

Average Latency: 1.00 seconds
Median Latency: 1.00 seconds
Standard Deviation of Latency: 1.00 seconds

Status Code Percentages:
200: 85.00%
404: 10.00%
500: 5.00%

Total Requests: 1000
Successful (Status 200): 850
Timeouts: 100
Other Errors: 50

Error Messages:
Timeout: 100
Error: 50
