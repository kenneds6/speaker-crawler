import argparse
import csv
import subprocess
import time
from os import listdir
from os.path import isfile, join


def driver(query_path, q_time, q_name, device_ip, iterations):
    for i in range(iterations):
        interface = 'br0'
        q_time = q_time + 1
        print('Starting capture...')
        capture = subprocess.Popen("sudo timeout " + str(q_time) + " tcpdump -i " + str(interface) + " -n host " + str(
            device_ip) + " -w " + "output/" + str(q_name) + str(
            i) + "_" + ".pcap", shell=True)
        time.sleep(1)
        print('Playing audio query...')
        play_audio = subprocess.Popen(["mpg321", query_path])
        capture.wait()
        print('Interaction captured')
        print("Capture File Saved, iter=" + str(i))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('csv',
                        help='A CSV File that contains the columns Query and Time, corresponding to the query and '
                             'interaction time')
    parser.add_argument('mp3_fp', help='The directory containing the audio query files')
    parser.add_argument('device_ip', help='The IP Address of the device')
    parser.add_argument('iter', help='Number of capture files to generate for each query')
    args = parser.parse_args()

    with open(args.csv) as csv_file:
        q_names = []
        q_times = []
        queries = csv.DictReader(csv_file)
        for row in queries:
            q_names.append(row["Query"])
            q_times.append(row["Time"])

    device_ip = args.device_ip
    query_directory = args.mp3_fp

    q_files = [f for f in listdir(query_directory) if isfile(join(query_directory, f))]
    q_files = sorted(q_files, key=lambda s: s.casefold())
    n_iter = int(args.iter)
    for idx, q in enumerate(q_files):
        driver(query_directory + q_files[idx], float(q_times[idx]), q_names[idx].replace(" ", "_") + '_', device_ip,
               n_iter)


