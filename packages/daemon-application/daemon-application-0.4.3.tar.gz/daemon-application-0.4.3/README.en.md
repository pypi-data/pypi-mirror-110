# daemon-application

A simple python package for creating daemon applications.

## Documents

- [中文文档](https://gitee.com/rRR0VrFP/daemon-application/)
- [English Document](https://gitee.com/rRR0VrFP/daemon-application/blob/master/README.en.md)

## Install

```
pip install daemon-application
```

## Usage

### Example for raw APIs

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

### Example for DaemonApplication

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

### Example for DaemonApplication adding new global options

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

*The output of the command help that added a new global option*

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

## Release

### v0.4.3 2021/06/26

- Deps on pyyaml.

### v0.4.2 2021/06/26

- Remove a print() statement.

### v0.4.1 2021/06/26

- Fix documents URLs.

### v0.4.0 2021/06/26

- Remove fastutils deps.
- Add `--config` global command option for DaemonApplication.
- Provide a way to override the global options for subclass of DaemonApplication.
- The sub-command `restart` will do just `start` if the old application is not running or crashed.
- Use gitee.com source code hosting service.

### v0.3.3 2020/11/22

- Fix show-config-filepaths.

### v0.3.2 2020/11/22

- Add click deps in requirements.txt

### v0.3.1 2020/11/22

- Add DaemonApplication.

### v0.3.0 2020/11/21

- New wrapper.

### v0.2.1 2018/04/18

- Old releases.
