# SQLBot
An Advanced SQLi Scanner

<img src="https://github.com/sourcecode347/SQLBot/blob/main/SQLBot.png" style="width:100%;height:auto;"/>

To Setup SQLBot Script execute this command :

    pip install requirements.txt

To use the SQLBot Script execute this Command :

    python sqlbot.py -t targets.txt -o results.txt -p 16

SQLBot Python Script is an Advanced SQL Injection Scanner that accepts targets from a file and crawls up to 3 Links at a time that contain Parameters and tests for possible SQL Injection Vulnerabilities.

It uses multithreaded technology and is quite fast, if we add too many processes or a very large list of targets, the processor and RAM memory may be overloaded, it is good not to define Processes manually and let it define the Threads of our processor, from lists it is good and fast to load up to 10000 targets at a time, because it loads all targets into memory and distributes them to the processes.

In combination with SiteDB and SQLMap it is a complete package to perform SQLi Attacks.

Have a nice day & Happy Hacking :)
