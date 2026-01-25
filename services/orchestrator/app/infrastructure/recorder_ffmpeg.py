import subprocess
from pathlib import Path

class FFmpegRecorder:
    def __init__(self, output: Path):
        self.output = output
        self.process = None

    def start(self):
        self.process = subprocess.Popen(
            ["ffmpeg", "-f", "alsa", "-i", "default", str(self.output)]
        )

    def stop(self):
        self.process.terminate()
        self.process.wait()
