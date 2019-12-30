chromebot
=========

This is a small intoduction into common chromebot admin tasks.

Restarting
----------

To restart chromebot run::

   systemctl --user restart chromebot-irc

The dashboard can be restarted with::

   systemctl --user restart chromebot-irc-dashboard

If you want to retrieve the status of a service like chromebot-irc, replace
“restart” with “status”.

Killing jobs
------------

Usually only jobs that ran for more than a few hours should be killed. Get a
list of browser processes using::

   ps -f -C google-chrome-stable

Then check the column stime (start time) and verify the process has been
running a long time. Use the PID (not PPID) column to figure out the process
ID, which you can then feed into::

   kill 12345

Replace 12345 with the actual number. If you now run the first command the
process should be gone and – if any – the next job will run.

Cleaning up crashed jobs
------------------------

Crashing jobs leave their temporary data behind in the directory
crocoite-data/temp, thus it is necessary to clean those up from time to time.

Most jobs that crashed Google Chrome can be uploaded, because they usually fail
during screenshot capturing. These jobs can be found and moved using::

   cd crocoite-data/temp/
   find . -mtime +0 -size +2M -ls

Examine list of files, check the WARCs look alright and they finished with
status 2, then::

   find . -mtime +0 -size +2M | parallel 'mv -vi {} ../finished/'

