import os
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
SAMPLE_PATH = ROOT / "cvgen" / "samples"


class Environment:
    config = "config.toml"
    build = "_build"
    output = "output"
    template = "template"
    content = "content"

    def ensure_env(self):
        os.makedirs(self.build, exist_ok=True)
        os.makedirs(self.output, exist_ok=True)

        if not os.path.exists(ROOT / "config.toml"):
            self.create_sample_config()

    def create_sample_config(self):
        if not os.path.exists(self.config):
            shutil.copy(SAMPLE_PATH / "config.toml", ROOT / "config.sample.toml")
