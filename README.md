# ViolentPy 
💻Violent Python using python3  
このリポジトリは書籍のソースコードをPython3向けに一部改変したものになります．

## Violent Python

![https://www.goodreads.com/book/show/16192263-violent-python](https://images.gr-assets.com/books/1355072634l/16192263.jpg)

["Violent Python" by TJ O'Connor](https://www.amazon.ca/Violent-Python-Cookbook-Penetration-Engineers/dp/1597499579)

## install 

pipenv (python 3.7.0)

`Pipfile.lock`を参照して環境を再現できます

```bash
$ pipenv sync
$ pipenv sync --dev # 開発用
```

 
### Chapter 1 and 2

All about penetration testing and understanding networks. Also, brute-force is fairly used. These first two chapters contain scripts to:
- Dictionary attacks
- Brute force password hash comparisons 
- Open secure zip files
- Port scanner
- SSH Botnet
- FTP Attack
- Replicate Conficker Attack

### Chapter 3 and 4

Geo-locating people and extrack meta data from apps.

- Geo-locate people using IPs and Images
- Firefox scrapper to download databases of saved cookies, download files list and past browser history
- Figure out where DDos attacks come from, from saved packets off the network

### Chapter 5
 
Manipulating Wifi packets.
- Wifi packet sniffer to find credit card number and google searches
- 802.11 protocol exploitation

### Chapter 6 and 7 

TBA

## License
All code here is under the MIT license.


## 免責事項
このリポジトリにおけるソースコードは全て教育・研究目的の為にあります．
他人の機器，或いはあなたが管理者権限を持たない環境での使用は違法行為とみなされる可能性があります．
自分の環境で使用される際は自己責任で使用してください．

## 開発用
導入パッケージは以下の通り

- flake8  
Python code checker

- flake8-import-order  
Python import order checker

- autopep8  
PEP8 style code formatter

```
$ pipenv install --dev flake8 autopep8 flake8-import-order
```

`Pipfile`へ実行コマンドの追加

```
[scripts]
lint = "flake8 --show-source ."
format = "autopep8 -ivr ."
```

パッケージの脆弱性検証
```
$ pipenv check
```