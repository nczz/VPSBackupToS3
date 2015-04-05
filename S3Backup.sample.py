#!/usr/bin/env python
# Author Mxp.tw
import os
import time

# Variables
backupfolderpath = '/PATH/TO/S3Backup'
s3bucketpath = 's3://BUCKET/OBJECT'
filestamp = time.strftime('%Y%m%d')
count = open(backupfolderpath+"/script/count.txt", "r").read().strip()
checkfiles = os.popen("ls %s/www | grep '%s'" % (backupfolderpath, filestamp)).readline() 
days = 14 # 14D period
counter = str(int(count)%days+1) 

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
if checkfiles.strip() != '':
    os.popen("rm %s/mysql/count-%s-*" % (backupfolderpath,counter))
    os.popen("rm %s/www/count-%s-*" % (backupfolderpath,counter))
else:
    print "Not Today! - %s" % (filestamp)

if checkfiles.strip() == '':

  for database in databaselist:
    database = database.strip()
    filename = "%s/mysql/count-%s-%s-%s.sql" % (backupfolderpath, counter, database, filestamp)
    print "Backing up %s" % (filename)
    os.popen("mysqldump -u%s -p%s -h%s -e --opt -c %s | gzip -c -9 > %s.gz" % (username, password, hostname, database, filename))
    print ".. done"

  for www in wwwdir:
    print "backing up www folder %s/%s" % (wwwpath, www)
    os.popen("tar JcpfP %s/www/count-%s-%s-%s.tar.bz2 %s/%s" % (backupfolderpath, counter, www, filestamp, wwwpath, www))

  #update count.txt (S3Backup/script/count.txt)
  os.popen("echo %s > %s/script/count.txt" % (str((int(count)+1)), backupfolderpath))
  os.popen("s3cmd sync --delete-removed --reduced-redundancy --skip-existing %s/www/ %s/www/" % (backupfolderpath, s3bucketpath))
  os.popen("s3cmd sync --delete-removed --reduced-redundancy --skip-existing %s/mysql/ %s/mysql/" % (backupfolderpath, s3bucketpath))

else:
    print "Not Today! - %s" % (filestamp)

