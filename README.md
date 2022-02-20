# Chukeki
 
これはLoRaの中継機 
 
# Requirement
  
* pip3
* pyserial
* rpi.gpio 
* sqlite3

* gpsd
* gpsd-clients
* pps-tools
* ntp

# Installation
  
```bash
sudo apt install -y python3-pip
sudo pip3 install pyserial 
sudo pip3 install rpi.gpio 
sudo apt install sqlite3 -y

sudo apt install gpsd gpsd-clients pps-tools -y
sudo apt install ntp -y

```
 
# Usage

### RasberryPi Imagerをインストール
https://www.raspberrypi.com/software/

### OSのインストール
Shift + Command + x　をしてみる
→設定が開かれる
Wifiとかを設定


```bash
git clone https://github.com/hoge/~
cd examples
python demo.py
```
 
# Note
 
注意点などがあれば書く
 
# Author
 
作成情報を列挙する
 
* 作成者
* 所属
* E-mail
 
# License
ライセンスを明示する
 
"hoge" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
 
社内向けなら社外秘であることを明示してる
 
"hoge" is Confidential.
