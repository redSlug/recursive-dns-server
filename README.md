# recursive-dns-server


## Setup

```bash
virtualenv --python=python3.7 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python -m service.server
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

### Debug
https://www.wireshark.org/
https://jvns.ca/blog/2018/06/19/what-i-use-wireshark-for/
https://howdns.works

to tell it to only look at local computer use `lo0` from `ifconfig`

```bash
python -m service.server
sudo tcpdump -i any port 50007 -w output.pcapdig @127.0.0.1 -p 50007 github.yo.com
dig @127.0.0.1 -p 50007 github.yo.com
```
