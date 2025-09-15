import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('file_changes.log'),
        logging.StreamHandler()
    ]
)

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.ignore_patterns = ['file_changes.log']
        
    def should_ignore(self, path):
        return any(pattern in path for pattern in self.ignore_patterns)
        
    def on_modified(self, event):
        if event.is_directory or self.should_ignore(event.src_path):
            return
        logging.info(f"Modified: {event.src_path}")

    def on_created(self, event):
        if event.is_directory or self.should_ignore(event.src_path):
            return
        logging.info(f"Created: {event.src_path}")

    def on_deleted(self, event):
        if event.is_directory or self.should_ignore(event.src_path):
            return
        logging.info(f"Deleted: {event.src_path}")
            
    def on_moved(self, event):
        if event.is_directory or self.should_ignore(event.src_path) or self.should_ignore(event.dest_path):
            return
        logging.info(f"Moved/Renamed: {event.src_path} -> {event.dest_path}")

def watch_directory(path='.'):
    # Convert to absolute path
    path = os.path.abspath(path)
    
    # Check if path exists
    if not os.path.exists(path):
        logging.error(f"The specified path does not exist: {path}")
        return
    
    # Initialize the observer
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    
    # Start the observer
    observer.start()
    logging.info(f"Started watching directory: {path}")
    logging.info("Press Ctrl+C to stop...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Stopped watching directory")
    observer.join()

if __name__ == "__main__":
    import sys
    # Use the first command line argument as the directory to watch, or current directory if not specified
    directory_to_watch = sys.argv[1] if len(sys.argv) > 1 else '.'
    watch_directory(directory_to_watch)

#   ''  ' here is vaibhav etxt'
