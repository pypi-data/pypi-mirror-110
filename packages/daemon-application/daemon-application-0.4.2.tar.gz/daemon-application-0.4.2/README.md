# daemon-application

## 文档

- [中文文档](https://gitee.com/rRR0VrFP/daemon-application/)
- [English Document](https://gitee.com/rRR0VrFP/daemon-application/blob/master/README.en.md)

## 介绍

Python开发包，用于创建后台守护进程。

## 安装

```
pip install daemon-application
```

## 使用说明

### 底层函数的使用


```
import time
import threading
import signal
from daemon_application import daemon_start

stopflag = False

def main():
    def on_exit(*args, **kwargs):
        with open("backgroud.log", "a", encoding="utf-8") as fobj:
            print("process got exit signal...", file=fobj)
            print(args, file=fobj)
            print(kwargs, file=fobj)
        global stopflag
        stopflag = True
    signal.signal(signal.SIGTERM, on_exit)
    signal.signal(signal.SIGINT, on_exit)
    while not stopflag:
        time.sleep(1)
        print(time.time())

if __name__ == "__main__":
    print("start background application...")
    daemon_start(main, "background.pid", True)
```


### DaemonApplication包装类的使用

```
import time
from daemon_application import DaemonApplication

class HelloApplication(DaemonApplication):
    def main(self):
        while True:
            print("hello")
            time.sleep(1)

controller = HelloApplication().get_controller()

if __name__ == "__main__":
    controller()

```

### 继承DaemonApplication包装类，并添加自定义参数

```
import time
import click
from daemon_application import DaemonApplication

class HelloApplication(DaemonApplication):

    def get_main_options(self):
        options = [
            click.option("-m", "--message", default="hello")
        ]
        return options + super().get_main_options()

    def main(self):
        while True:
            print(self.config["message"])
            time.sleep(1)

controller = HelloApplication().get_controller()

if __name__ == "__main__":
    controller()
```

*添加自定义参数后的帮助信息*

```
Usage: example.py [OPTIONS] COMMAND [ARGS]...

Options:
  --pidfile TEXT          pidfile file path.
  --workspace TEXT        Set running folder
  --daemon / --no-daemon  Run application in background or in foreground.
  -c, --config TEXT       Config file path. Application will search config
                          file if this option is missing. Use sub-command
                          show-config-fileapaths to get the searching tactics.

  -m, --message TEXT
  --help                  Show this message and exit.

Commands:
  restart                Restart Daemon application.
  show-config-filepaths  Print out the config searching paths.
  start                  Start daemon application.
  stop                   Stop daemon application.
```

## 版本记录

### v0.4.2 2021/06/26

- 删除无效的print语句。

### v0.4.1 2021/06/26

- 修正文档链接。

### v0.4.0 2021/06/26

- 迁移fastutils的依赖。
- DaemonApplication包装类中添加`--config`全局参数。
- 为DaemonApplication子类提供重载全局参数的机制。
- DaemonApplication包装类的子命令`restart`在进程不存在时，进行启动，而不是报错。
- 使用gitee.com做源代码托管。

### v0.3.3 2020/11/22

- 修正show-config-filepaths子命令中的错误。

### v0.3.2 2020/11/22

- 完善依赖包信息。

### v0.3.1 2020/11/22

- 添加DaemonApplication包装类。

### v0.3.0 2020/11/21

- 重构底层函数。

### v0.2.1 2018/04/18

- 旧版本导入。
