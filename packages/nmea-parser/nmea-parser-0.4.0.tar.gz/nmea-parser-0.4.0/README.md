# NMEA Parser

A library used to decode NMEA data streams from GNSS receivers. Capable of parsing a text file
containing NMEA data or reading from a serial port real time.

This library is currently in Beta and is subject to change any time.

## Dependencies

PySerial is the only dependency. See `requirements.txt`.

## Usage

See www.bek.sh/nmea-parser for a full manual.

### Examples

#### Opening and Reading a Serial Port

It is highly sugested that you use all input streams within a context manager (`with` statement) as shown below.

```python
from nmea import input_stream

stream = input_stream.GenericInputStream.open_stream('/dev/ttyACM0', 9600)

print(stream)

with stream:
    print(stream.get_line())
```

If you must use an input stream without a context manager, make sure that the `ensure_closed()` function
is called prior to exit:

```python
from nmea import input_stream

stream = input_stream.GenericInputStream.open_stream('/dev/ttyACM0', 9600)

print(stream)
print(stream.get_line())
stream.ensure_closed()      # You must not forget to manually close the stream.
```

Using a context manager ensures that the port is always closed should your program halt unexpectedly.

`GenericInputStream.open_stream()` also accepts all keyword arguments that are accepted by `serial.Serial()` in
PySerial.

### Opening and Reading a NMEA Dump file

Text files containing NMEA streams may also be used with this library. Just point the `open_stream()` function at
the desired file:

```python
from nmea import input_stream, data_frame

stream = input_stream.GenericInputStream.open_stream('sample-data/sample1.txt')

with stream:
    new_frame = data_frame.DataFrame.get_next_frame(stream)

    print("Current GPS time:", new_frame.gps_time)
    print("Current Latitude:", new_frame.latitude)
    print("Current Longitude:", new_frame.longitude)
    print("Current Speed:", new_frame.velocity)
    print("Current heading:", new_frame.track)
```

### Getting Position Data and Logging to a Database

The `DataFrame` object contains properties that allow you to access your current position, movement, and information
on all satellites used to calculate your fix. The logging module allows you to record these objects in an SQLite
database.

```python
from nmea import input_stream, data_frame, database_wrapper

stream = input_stream.GenericInputStream.open_stream('/dev/ttyACM0', 9600)

db = database_wrapper.SQLiteConnection.from_path('./example.sqlite')

print(stream)

with stream:
    while True:
        new_frame = data_frame.DataFrame.get_next_frame(stream)

        print("Current GPS time:", new_frame.gps_time)
        print("Current Latitude:", new_frame.latitude)
        print("Current Longitude:", new_frame.longitude)
        print("Current Speed:", new_frame.velocity)
        print("Current heading:", new_frame.track)
        print("Number of Satellites above:", new_frame.nsats)
        print("Individual Observations:")
        for obs in new_frame.sv_observations:
            print('\tPRN:', obs.prn)
            print('\t\tSignal to Noise:', obs.snr)
            print('\t\tAzimuth:', obs.azimuth)
            print('\t\tElevation:', obs.elevation)

        db.insert_dataframe(new_frame)
```

