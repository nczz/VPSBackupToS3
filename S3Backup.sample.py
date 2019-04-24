#!/usr/bin/env python
# Author Mxp.tw
import os
from datetime import datetime, timedelta

# Variables
backupfolderpath = '/PATH/TO/S3Backup'
s3bucketpath = 's3://BUCKET/OBJECT'
filestamp = datetime.now().strftime('%Y%m%d')
count = open(backupfolderpath+"/script/count.txt", "r").read().strip()
days = 14 # 14D period
counter = str(int(count)%days+1) 
date_N_days_ago = datetime.now() - timedelta(days)
filestamp_back = date_N_days_ago.strftime('%Y%m%d')

# MySQL DB infomation
username = '==DBNAME=='
password = '==DBPASSWD=='
hostname = '==HOSTNAME=='
wwwpath = '/PATH/TO/WWW'
database_list_command = "mysql -u%s -p%s -h%s --silent -N -e 'show databases'" % (username, password, hostname)

wwwdir = os.listdir(wwwpath)
# excloude backup folders
wwwdir.remove('==IDONTWANTBACKUPSITE1==')
#wwwdir.remove('==IDONTWANTBACKUPSITE2==')
#wwwdir.remove('==IDONTWANTBACKUPSITE3==')
#... etc u know...

databaselist =  os.popen(database_list_command).readlines()
# excloude backup databases
databaselist.remove('mysql\n')
databaselist.remove('performance_schema\n')
databaselist.remove('information_schema\n')
#databaselist.remove('==DATABASENAME1==\n')
#databaselist.remove('==DATABASENAME2==\n')
#... etc u know... again

# remove old backup files
#os.system("rm `ls -rt -d -1 %s/mysql/* | grep '%s'` 2> /dev/null" % (backupfolderpath,filestamp_back))
#os.system("rm `ls -rt -d -1 %s/www/* | grep '%s'` 2> /dev/null" % (backupfolderpath,filestamp_back))
os.system("find %s/mysql/ -mindepth 1 -mtime +%s -delete" % (backupfolderpath,days))
os.system("find %s/www/ -mindepth 1 -mtime +%s -delete" % (backupfolderpath,days))
# remove today's backup files (debug mode)
os.system("rm `ls -rt -d -1 %s/mysql/* | grep '%s'` 2> /dev/null" % (backupfolderpath,filestamp))
os.system("rm `ls -rt -d -1 %s/www/* | grep '%s'` 2> /dev/null" % (backupfolderpath,filestamp))

for database in databaselist:
  database = database.strip()
  filename = "%s/mysql/count-%s-%s-%s.sql" % (backupfolderpath, counter, database, filestamp)
  print "Backing up %s" % (filename)
  os.system("mysqldump -u%s -p%s -h%s -e --opt -c %s | gzip -c -9 > %s.gz" % (username, password, hostname, database, filename))
  print ".. done"

for www in wwwdir:
  print "backing up www folder %s/%s" % (wwwpath, www)
  os.system("tar JcpfP %s/www/count-%s-%s-%s.tar.bz2 %s/%s --warning=no-file-changed" % (backupfolderpath, counter, www, filestamp, wwwpath, www))

#update count.txt (S3Backup/script/count.txt)
os.system("echo %s > %s/script/count.txt" % (str((int(count)+1)), backupfolderpath))
os.system("s3cmd sync --delete-removed --reduced-redundancy --skip-existing --disable-multipart %s/www/ %s/www/" % (backupfolderpath, s3bucketpath))
os.system("s3cmd sync --delete-removed --reduced-redundancy --skip-existing --disable-multipart %s/mysql/ %s/mysql/" % (backupfolderpath, s3bucketpath))
