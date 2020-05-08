# HTTP-Python-Projects
A collection of HTML files and Python scripts with HTTP and SMTP communication functionality, all created throughout the Fall 2019 semester as a part of my Net-Centric Computing class.
NOTE: Many of the links on index.html only work if a server script is running. Additionally, server scripts only appear to work on FIU's Ocelot servers.

## Files of note:

### TCPServer.py
Server code for TCP communication. Compatible with TCPClient.py and the found.html and "fake.html" (page not found error test) links on index.html.

### mail_auth.cgi
Uses an HTML submission form to send an email between two email addresses using the SMTP AUTH authenticated email protocol.

### ajax.html
An HTML page using Ajax to dynamically display information.

### CookieServer.py
Created, sent, and printed a cookie that is stored within the web browser.

### ThreadedServer.py
Basically a multithreaded implementation of TCPServer.py, splitting every HTTP request into its own thread.


Video (.mp4) files showcasing the functionality of the above scripts/files can be found in the "video demos" directory of this respository.
