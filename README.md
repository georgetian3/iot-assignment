# 《物联网导论》大作业

## 安装依赖

`pip install -r requirements.txt`

## 运行方式

只需要在 `src/` 下调用 `main.py` 中的若干个指令：

```
> py main.py -h
usage: main.py [-h] [--bs BS] [--br] [--ds] [--dr DR] [--host HOST] [--port PORT]
               [--dAA DAA] [--dBB DBB] [--gui] [--btest sent received]

options:
  -h, --help            show this help message and exit
  --bs BS               Run Bluetooth sender, argument is the text to be sent
  --br                  Run Bluetooth receiver
  --ds                  Run distance sender
  --dr DR               Run distance receiver, argument is IP address of sender
  --host HOST           The host IP of sender
  --port PORT           The host port of sender
  --dAA DAA             The distance between mic and speaker of the sender device (m)     
  --dBB DBB             The distance between mic and speaker of the receiver device (m)   
  --gui                 Run GUI
  --btest sent received
                        Calculates packet loss rate and error rate for Bluetooth
```

### 图形界面

`py main.py --gui`

### 通信

先调用接收方：`py --br`

再调用发送方：`py --bs "insert Unicode string here"`

计算丢包率和误码率：`py --btest sent received`

### 测距

先调用发送方：`py --ds`

再调用接收方：`py --dr --host 192.168.1.xxx --port 2333 --dAA 0.1 --dBB 0.1`