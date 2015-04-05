#!/bin/bash
# Author Mxp.tw
BACKUP_PATH='./S3Backup'
echo "0" > $BACKUP_PATH/script/count.txt
rm $BACKUP_PATH/mysql/*
rm $BACKUP_PATH/www/*
exit
