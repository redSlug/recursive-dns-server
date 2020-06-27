# recursive-dns-server


## Setup

```bash
virtualenv --python=python3.7 venv
source venv/bin/activate
pip install requirements.txt
```

## Run

```bash
python -m service.server
python -m service.client
```

## Resources

### UDP server
https://pythontic.com/modules/socket/udp-client-server-example
https://pymotw.com/2/socket/udp.html
https://subscription.packtpub.com/book/networking_and_servers/9781784396008/7/ch07lvl1sec58/working-with-udp-sockets
https://docs.python.org/3/library/socket.html

### DNS
https://book.systemsapproach.org/applications/infrastructure.html
https://tools.ietf.org/html/rfc1035
https://jvns.ca/blog/how-updating-dns-works/

### Debugging
https://www.wireshark.org/ 
https://jvns.ca/blog/2018/06/19/what-i-use-wireshark-for/

to tell it to only look at local computer 
lo1

https://howdns.works
dig @localhost -p 5353 google.com