# cf-remote

Install, without bootstrap:
```
$ cf-remote -H 1.2.3.4
```

Install and bootstrap:
```
$ cf-remote -H 192.168.100.10 -B 192.168.100.1 install
```
(`install` command is optional)

Install and bootstrap 2 hosts:
```
$ cf-remote -H cfengine.com,1.2.3.4 -B 192.168.100.1
```

Add remote(s) to a local file, so you don't have to use `-H` each time.
```
$ cf-remote add 1.2.3.4
```

Ideas for commands:
```
$ cf-remote install
$ cf-remote status
$ cf-remote info
$ cf-remote vars
$ cf-remote classes
$ cf-remote execute
$ cf-remote restart
$ cf-remote uninstall
$ cf-remote help
$ cf-remote version
$ cf-remote --version
$ cf-remote --help
```
