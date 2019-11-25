# pyssh
simple python tools to help manage several virtual servers.

** developed and used in cmu cloud computing team project

## features
* pyssh - Send ssh commands to mulitple servers in parallel
* pyscp - upload files to multiple servers in parallel

## basic
```
python pyssh.py -i lightsail.pem -h cc/hosts -c 'mkdir .aws && mkdir s3q2 && mkdir s3q3'
```

host file(cc/hosts):
```
ubuntu@ip1
ununtu@ip2
...
```

Same command with be sent to all hosts in the host file.

## with variables
```
python pyssh.py -i lightsail.pem -h cc/hosts -e cc/s3q2 -c 'aws s3 sync {s3q2} s3q2/ > tmp.log'
```

varibale file(cc/s3q2):
```
url1
url2
url3
```
** note: the variable file should have same number of lines

Each remote server will start to download one url in the variable file.

## pyscp
```
python pyscp.py -i lightsail.pem -h cc/hosts -f cc/q2.sql -t "q2.sql"
```
Same file will be uploaded to remote servers
