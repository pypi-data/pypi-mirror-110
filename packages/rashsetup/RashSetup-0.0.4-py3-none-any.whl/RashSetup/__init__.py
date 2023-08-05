import tempfile
import os
import json
import threading
import sys
import time
import gc
import pathlib
import subprocess

__all__ = [
    "JsonHandler",
    "TempHandler",
    "Launcher"
]


class JsonHandler:
    def __init__(self, file=None):
        self.file = file

    def load(self):
        with open(self.file, 'r') as loaded:
            return json.load(loaded)

    def dump(self, store):
        with open(self.file, 'w') as loaded:
            return json.dump(store, loaded, indent=4)

    def __call__(self, raw: str):
        return json.loads(raw)


class TempHandler:
    def __init__(self):
        self.note = []

    def __call__(self, suffix='', prefix='', dir_=None, text=True):
        mode, file = tempfile.mkstemp(suffix, prefix, dir_, text)
        os.close(mode)
        self.note.append(file)
        return file

    def close(self):
        return [os.remove(_) for _ in self.note if os.path.exists(_)]

    def make_temp(self, path=None):
        path = os.path.dirname(__file__) if not path else path if os.path.isdir(path) else os.path.dirname(path)
        temp = os.path.join(path, "temp")
        os.mkdir(temp)
        return temp


"""
LOCK SAUCE:
    GLOBAL LOCK:
    'e' - exited
    '1' - high state
    '' - low state

    MAX LOCK:
        '1' - someone tried to open
        'e' - close application [TODO]

    Rash is opened if it toggle s between high and low state for every second

"""


class Launcher:
    def __init__(self, pwd):
        self.pwd = pathlib.Path(pwd)
        self.pwd = self.pwd.parent if self.pwd.is_file() else self.pwd

        if not self.pwd.exists():
            raise FileNotFoundError(self.pwd)

        self.global_mutex = self.pwd / "GLOBAL.lock"
        self.max_mutex = self.pwd / "MAX.lock"

        None if self.test() else self._notify()

        read_thread = threading.Thread(target=self.read_thread)
        read_thread.setName("Global Mutex Thread")
        read_thread.setDaemon(True)
        write_thread = threading.Thread(target=self.write_thread)
        write_thread.setName("Max Mutex Thread")
        write_thread.setDaemon(True)

        self.workers = threading.Lock(), threading.Lock()
        self.remainder = None

        read_thread.start()
        write_thread.start()

    def _notify(self):
        self.max_mutex.write_text("1")
        return sys.exit(0)

    def register(self):
        pass

    def test(self):
        if not self.global_mutex.exists():
            self.global_mutex.write_text("")
            return True

        test_1 = self.global_mutex.read_text()

        if test_1 == 'e':
            return True

        time.sleep(1)

        test_2 = self.global_mutex.read_text()

        time.sleep(0.1)

        test_3 = self.global_mutex.read_text()

        if test_1 == test_2 and test_3 == test_1:
            return True

        return False

    def read_thread(self):
        self.workers[0].acquire()

        while self.workers[0].locked():

            code = None if self.max_mutex.exists() else self.max_mutex.write_text("")
            code = code if code else self.max_mutex.read_text()

            result = None if code == '' else self.remainder(code == '1') if self.remainder else None

            if result:
                break

            time.sleep(1)

        self.max_mutex.write_text("")

    def write_thread(self):
        self.workers[1].acquire()

        toggle = False

        while self.workers[1].locked():
            None if self.global_mutex.exists() else self.global_mutex.write_text("")

            self.global_mutex.write_text("" if toggle else "1")
            toggle = not toggle

            time.sleep(1)

    def close(self):
        for _ in self.workers:
            _.release()


def export_rash(current_path):
    if not os.path.isdir(current_path):
        raise NotADirectoryError(f"{current_path} is not a directory")


def pip_install(*packages):
    for _ in packages:
        subprocess.run([
            sys.executable, "-m", "pip", "install", _
        ])


def is_all_ready():
    return (pathlib.Path(__file__).parent.parent / "RashSetup.exe").exists()


gc.collect()

def start():
    with open("check.txt", 'w') as checker:
        checker.write("Alive")
