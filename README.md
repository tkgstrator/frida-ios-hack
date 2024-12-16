# iOS App Decryptor

SileoがインストールされているRootless脱獄されたiOSデバイスから復号されたアプリケーションをIPA形式でダンプするためのDevConatiner環境です。

## 環境構築

macOSではUSB接続されたデバイスを簡単にDockerの内部と共有できないため、必然的にリモート接続が必要になります。ただ、`frida-server`は`openssh`と違いデフォルトで外部からの接続を許可するようになっていないため、

デバイスには`openssh`と`frida`がインストールされている必要があります。

fridaは公式の標準レポジトリには追加されていないので[https://build.frida.re](sileo://source/https://build.frida.re)から追加します。

デバイスではデフォルトではUSB経由でしかfrida-serverの接続を許可していないので、全てのポートから受け付けられるようにします。

```bash
ssh root@192.168.XXX.YYY
```

Rootlessで脱獄した場合、以下のようなディレクトリになっているので`re.frida.server.plist`を編集します。

```bash
var/
└── jb/
    ├── Library/
    │   └── LaunchDaemons/
    │       └── re.frida.server.plist
    └── usr/
        └── lib/
            ├── frida/
            │   └── frida-agent.dylib
            └── sbin/
                └── frida-serer
```

`vi /var/jb/Library/LaunchDaemons/re.frida.server.plist`としてファイルを編集します。

```plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
 <key>Label</key>
 <string>re.frida.server</string>
 <key>Program</key>
 <string>/var/jb/usr/sbin/frida-server</string>

 <key>ProgramArguments</key>
 <array>
  <string>/var/jb/usr/sbin/frida-server</string>
 </array>

 <key>UserName</key>
 <string>root</string>
 <key>POSIXSpawnType</key>
 <string>Interactive</string>
 <key>RunAtLoad</key>
 <true/>
 <key>KeepAlive</key>
 <true/>
 <key>ThrottleInterval</key>
 <integer>5</integer>
 <key>ExecuteAllowed</key>
 <true/>
</dict>
</plist>
```

という感じになっているので、

```plist
<key>ProgramArguments</key>
<array>
 <string>/var/jb/usr/sbin/frida-server</string>
 <string>-l</string>
 <string>0.0.0.0</string>
</array>
```

という感じで起動時にオプションを渡すようにします。

```bash
$ launchctl unload re.frida.server.plist
$ launchctl load re.frida.server.plist
```

最後に設定を再読込するようにします。

これで`ps aux | grep frida`とすれば`/var/jb/usr/sbin/frida-server -l 0.0.0.0`のように起動するようになっています。

正しくオプション付きで立ち上がっていることを確認したらホストマシンから`frida-ps`で繋いでみます。

```bash
$ frida-ps -H 192.168.XXX.YYY
  PID  Name
-----  ------------------------------------------
32783  AMPIDService                              
32696  ASPCarryLog                               
32639  AccessibilityUIServer                     
32245  AnimalDev                                 
30344  App Store          
...
```

でリモートのデバイスに繋ぐことができるようになりました。