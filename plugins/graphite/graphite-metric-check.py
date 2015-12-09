#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from sensu_plugin import SensuPluginCheck
import json
import requests

def getGraphiteValue(host, port, target, from_time, to_time):
    
    request_url = 'http://' + host + ':' + str(port) + '/render'
    ranges = { 'from': '-' + from_time, 'to': to_time, 'target': target, 'format': 'json' }


    r = requests.get(request_url, params=ranges)
    graphite_dict = json.loads(r.content)

    counter = 0
    point_sum = 0
    for point in graphite_dict:
        for value, timestamp in point['datapoints']:
            if value is not None:
                point_sum = int(point_sum) + int(value)
                counter += 1
    
    avg_value = point_sum / counter

 #   return str(graphite_dict)

    return avg_value


class GraphiteMetricCheck(SensuPluginCheck):
    def setup(self):
        self.parser.add_argument(
          '-w',
          '--warning',
          required=True,
          type=int,
          help='Integer warning level to output'
        )
        self.parser.add_argument(
          '-c',
          '--critical',
          required=True,
          type=int,
          help='Integer critical level to output'
        )
        self.parser.add_argument(
          '-s',
          '--host',
          required=True,
          type=str,
          help='graphite host. http://graphite.example.com'
        )
        self.parser.add_argument(
            '-p',
            '--port',
            type=int,
            default=8080,
            help='Port'
        )
        self.parser.add_argument(
          '-t',
          '--target',
          required=True,
          type=str,
          help='metric target: com.example.some.metric'
        )
        self.parser.add_argument(
          '-f', 
          '--from_time',
          default='-5min',
          type=str,
          help='from time. without -. Example: -f 15h. Default value: -5min'
        )
        self.parser.add_argument(
          '-o',
          '--to_time',
          type=str,
          default='now',
          help='to time. Default = now'
        )
        self.parser.add_argument(
          '-m',
          '--message',
          type=str,
          default=None,
          help='message to display'
        )

    def run(self):
        # this method is called to_time perform the actual check

        self.check_name('GraphiteMetricCheck') # defaults to_time class name

        avg = getGraphiteValue(self.options.host, self.options.port, self.options.target, self.options.from_time, self.options.to_time)

        if avg > self.options.warning and avg < self.options.critical:
          self.warning(self.options.target + ' ' + str(avg))
        elif avg < self.options.warning:
          self.ok(self.options.target + ' ' + str(avg))
        elif avg >= self.options.critical:
          self.critical(self.options.target + ' ' + str(avg))
        else:
          self.unknown(self.options.message)

if __name__ == "__main__":
    f = GraphiteMetricCheck()
