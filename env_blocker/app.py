import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re
import os


class LogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        f = open("blk.txt", 'a+')
        if event.is_directory or not event.src_path.endswith(".log"):
            return

        with open(event.src_path, "r") as log_file:
           new_data = log_file.readlines()

        match = re.search(
            r'(\d+\.\d+\.\d+\.\d+).*?"GET (.*?) HTTP', new_data[-1].strip())
        if match:
            ip = match.group(1)
            path = match.group(2)
            if path.find(".env") != -1:
                os.system(f"ip route add blackhole {ip}")
                f.writelines(f"{ip}\n")


if __name__ == "__main__":

    log_directory = "/var/log/nginx/"
    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, path=log_directory, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
