import os
import time
import pandas as pd
from scapy.all import sniff
from scapy.all import wrpcap


def driver(query_path, q_time,q_name, device_ip, iterations):
    for i in range(iterations):
        # wait before starting capture
        time.sleep(1)
        # start capture
        start_capture(device_ip, q_name, i)

        # play query
        os.system("mpg321 " + query_path)
        # wait for duration specified and stop and save capture
        time.sleep(q_time)


def start_capture(ip, trace_name='trace_', trace_number=1):
    packets = sniff(filter='ip host ' + ip)
    wrpcap(trace_name + trace_number + '.pcap', packets)


if __name__ == "__main__":
    queries = pd.read_csv('/home/scramblesuit/PycharmProjects/speaker-crawler/data/echo_test/echo_test_queries.csv')

    query_directory = '/home/scramblesuit/PycharmProjects/speaker-crawler/voice_queries/echo_test/'

    from os import listdir
    from os.path import isfile, join
    q_files = [f for f in listdir(query_directory) if isfile(join(query_directory, f))]
    q_names = queries['Query']
    q_times = queries['Time']
    start_capture('192.168.86.36')
    driver(query_directory + q_files[0], q_times[0], q_names[0], 100)


