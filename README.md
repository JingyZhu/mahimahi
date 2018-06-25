This is a modified version of mahimahi for recording and replaying with RTT settings and Proxy emulation \
For the original repo: Please refer [here](https://github.com/ravinet/mahimahi)

#### Added feature:
1. RTT recording for different IPs during **mm-webrecord**
2. RTT application during the **mm-webreplay** in **mm-delay** shell
3. Server thinking time in Apache cgi_handler to emulate TTFB
##### Proxy emulation settings
1. Header modification for CORS
2. Redirection 307 status code to keep the method

#### To make it run
1. edit **src/frontend/recordshell.cc** line 103 NIC name (default ens3 or enp0s3). Remake
2. To parse the RTT, edit **PyScript/record-replay/parse.py** line line 36 NIC's ip address
