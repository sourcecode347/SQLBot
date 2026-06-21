# SQLBot
An Advanced SQLi Scanner

<img src="https://github.com/sourcecode347/SQLBot/blob/main/SQLBot.png" style="width:100%;height:auto;"/>

To Setup SQLBot Script execute this command :

    pip install -r requirements.txt

Open the sqlbot.py with a text editor and go to the settings sector and setup the SQLMAPAPI_PATH and the other settings if you want to change.

To use the SQLBot Script execute this Command :

    python sqlbot.py -t targets.txt -o results.txt -p 16

For Help execute this Command :

    python sqlbot.py -h

SQLBot Python Script is an Advanced SQL Injection Scanner that accepts targets from a file and crawls up to 3 Links at a time that contain Parameters and tests for possible SQL Injection Vulnerabilities.

It uses multithreaded technology and is quite fast, if we add too many processes or a very large list of targets, the processor and RAM memory may be overloaded, it is good not to define Processes manually and let it define the Threads of our processor, from lists it is good and fast to load up to 10000 targets at a time, because it loads all targets into memory and distributes them to the processes.

SQLBot has been upgraded quite a bit, you set it up with a list of sites, it visits them and there the Spider is activated which Crawls new URLs with Parameters, in each Crawl the Detector runs which has many SQLi Payloads and Error Signs and identifies possible SQLi vulnerabilities and submits them for automatic analysis to SQLMap.
SQLMap completes the analysis with a maximum time of 25 minutes per URL and if it gains access to the Server databases then it saves the Vulnerable URL in a document.

Have a nice day & Happy Hacking :)
