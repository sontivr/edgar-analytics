import sys
import os
import csv
import copy
from collections import defaultdict, OrderedDict
from datetime import datetime as dt

class analyze_weblog:
   """
   Class to compute session stats from a weblog

   """

   def __init__(self, weblog_file, inactivity_file, output_file):
       """
       Initialization

       :param weblog_file: input file
       :param inactivity_file: file with inactivity period in sec
       :param output_file: output file for the results
       """
       self.weblog_file = weblog_file
       self.output_file = output_file

       '''
       key: string for ip
       value: dict for other attributes
       '''
       self.ip_dict = OrderedDict()

       # store activity period
       with open(inactivity_file, "r") as fh:
           self.inactivity_period = int(fh.readline())

       if os.path.exists(self.output_file): os.remove(self.output_file)

   def compute_session_stats(self, ip, new_rec):
       """
       Computes the session stats for each of the ip address stored in self.ip_dict

       :param ip: ip address of the new record
       :param new_rec: dict for the reset of the elements
       """

       mydict = copy.deepcopy(self.ip_dict)
       for k, v in mydict.items():
          duration = (new_rec['datetime'] - v['last_request_time']).total_seconds()
          if duration > self.inactivity_period:
              with open(self.output_file, "a") as fh:
                  fh.write('{},{},{},{},{}\n'.format(k, dt.strftime(v['datetime'], '%y-%m-%d %H:%M:%S'), \
                                            dt.strftime(v['last_request_time'], '%y-%m-%d %H:%M:%S'), \
                                            int((v['last_request_time'] - v['datetime']).total_seconds()+1), v['count']))

              # delete the record since it was written to the output file
              del self.ip_dict[k]
          else:
              '''
              Increment the count and update last_request_time if the ip already exists in self.ip_dict
              '''
              if k == ip:
                 self.ip_dict[ip]['count'] += 1
                 self.ip_dict[ip]['last_request_time'] = new_rec['datetime']

       '''
       Insert the record with new ip
       '''
       if ip not in self.ip_dict:
          self.ip_dict.update({ip: new_rec})


   def dump_remaining_sessions(self):
       """
       outputs the stats for remaining sessions in self.ip_dict after the last record was read from the input_file
       """
       mydict = copy.deepcopy(self.ip_dict)
       for k, v in mydict.items():
           with open(self.output_file, "a") as fh:
               fh.write('{},{},{},{},{}\n'.format(k, dt.strftime(v['datetime'], '%y-%m-%d %H:%M:%S'), \
                                                dt.strftime(v['last_request_time'], '%y-%m-%d %H:%M:%S'), \
                                                int((v['last_request_time'] - v['datetime']).total_seconds()+1), v['count']))


   def read_weblog(self):
       """
       Reads input weblog one line at a time and builds a dict to send it to compute_session_stats
       """
       with open(self.weblog_file) as fh:
           reader = csv.DictReader(fh)
           for row in reader:
              new_rec = {}
              new_rec['datetime'] = dt.strptime(' '.join([row['date'],row['time']]), '%Y-%m-%d %H:%M:%S')
              new_rec['cik'] = row['cik']
              new_rec['accession'] = row['accession']
              new_rec['extention'] = row['extention']
              new_rec['count'] = 1
              new_rec['last_request_time'] = new_rec['datetime']

              self.compute_session_stats(row['ip'], new_rec)

       self.dump_remaining_sessions()

if __name__ == '__main__':
   args = sys.argv
   log_csv = str(args[1])
   inactivity_file = str(args[2])
   output_file = args[3]
   a = analyze_weblog(log_csv, inactivity_file, output_file)
   a.read_weblog()


