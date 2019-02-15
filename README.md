## Analyzing session level stats from weblogs
The goal of this project is to read a set of fields from each line of a weblog file supplied and produce session level stats for each ip address appeared in the input file. The session length is defined by the inactivity period in seconds that is read from another file.

### Fields fomr input csv file 
* `ip`: identifies the IP address of the device requesting the data. 
* `date`: date of the request (yyyy-mm-dd)
* `time`:  time of the request (hh:mm:ss)
* `cik`: SEC Central Index Key
* `accession`: SEC document accession number
* `extention`: Value that helps determine the document being requested

### Fields to be produced in the output file
* IP address of the user exactly as found in the input file
* date and time of the first webpage request in the session (yyyy-mm-dd hh:mm:ss)
* date and time of the last webpage request in the session (yyyy-mm-dd hh:mm:ss)
* duration of the session in seconds
* count of webpage requests during the session


Please refer to [docs/README.md](docs/README.md) for additional details.


