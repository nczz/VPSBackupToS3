#### Information

找了半天沒看到輕巧好用的備份工具乾脆自己寫一個，第一次寫 Python 就當是練習拉XD

此工具備份 MySQL + www 資料，設定一個保存週期(預設14天)，過期的舊備份會自動移除，同步AWS S3 空間！

使用流程

1. 安裝 s3cmd & python-magic
	
	```
	sudo apt-get update
	sudo apt-get install s3cmd python-magic -y
	```
	
2. 確保環境變數中已經有加入 `mysqldump` & `s3cmd`

3. 已有AWS帳號並且創建過IAM的腳色，拿到 `Access Key` & `Secret Access Key`後設定 `s3cmd`
	
	```
	s3cmd --configure
	```
	
4. 抓下這個 repo，將 S3Backup.sample.py 更名為 S3Backup.py，並賦予執行權限、建立環境
	```
	cd path/to/repo
	mv S3Backup.sample.py S3Backup.py
	chmod +x S3Backup.py
	mkdir -p S3Backup/script
	mkdir -p S3Backup/www
	mkdir -p S3Backup/mysql
	echo "0" > S3Backup/script/count.txt
	```
5. 開啟 `S3Backup.py` 編輯設定參數

6. 加入 crontab 每天凌晨進行備份
	```
	crontab -e
	# add the line without '#'
	# 0 2 * * * /usr/bin/python /path/to/S3Backup.py > /path/to/backup.log 
	```
7. DONE, 剩下其他可能的問題大概都是檔案權限設定或是環境設置錯誤了

#### Required

> 注意，此腳本僅在下面環境測試

1. Ubuntu 14.04 64Bit
2. [Python 2.7](https://docs.python.org/2.7/)
3. Python-magic module
4. [S3cmd](http://s3tools.org/s3cmd)
5. MySQL-mysqldump

#### Changelog

```
V1.0 - init - 幾乎無防呆與設定項稍微整理過的第一版
V1.5 - 重大更新，刪除過期失效備份機制錯誤
V2.0 - 整理後發佈第二版
```
