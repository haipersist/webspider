
DATE=`date +"%Y-%m-%d"`

#sudo mount -t ntfs /dev/sdb5 /media/haibo/

JOBFILENAME=$DATE-job.sql
mysqldump -uroot -p320623 app_hbnnlove jobs > /media/haibo/$JOBFILENAME
mysqldump -uroot -p320623 app_hbnnlove jobs > /tmp/$JOBFILENAME





