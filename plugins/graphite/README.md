# sensu-plugin-graphite-metric-check

Check average value from graphite metric.

## Usage
```
usage: graphite-metric-check.py [-h] -w WARNING -c CRITICAL -s HOST [-p PORT]
                                -t TARGET [-f FROM_TIME] [-o TO_TIME]
                                [-m MESSAGE]

optional arguments:
  -h, --help            show this help message and exit
  -w WARNING, --warning WARNING
                        Integer warning level to output
  -c CRITICAL, --critical CRITICAL
                        Integer critical level to output
  -s HOST, --host HOST  graphite host. http://graphite.example.com
  -p PORT, --port PORT  Port
  -t TARGET, --target TARGET
                        metric target: com.example.some.metric
  -f FROM_TIME, --from_time FROM_TIME
                        from time. Default = -5min
  -o TO_TIME, --to_time TO_TIME
                        to time. Default = now
  -m MESSAGE, --message MESSAGE
                        message to display
```

## Dependencies

* sensu-python-plugin
* libjson-python


