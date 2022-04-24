python3 /home/ec3-user/krx/guessBuyPoint.py >> /home/ec3-user/krx/log/guessBP.log

python3 /home/ec3-user/krx/mergeBP.py

mv -f /home/ec3-user/krx/output/_chartData/* /home/ec3-user/krx/output/chartData/

curl "https://gx.tool4.us/manage?checkCode=rh&actType=reload"

