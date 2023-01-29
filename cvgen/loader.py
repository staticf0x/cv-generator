import os
import tomllib
from typing import List

from jinja2 import Environment as JinjaEnv
from jinja2 import FileSystemLoader

from cvgen.environment import Environment
from cvgen.models import Config


class Loader:
    def __init__(self):
        self.env = Environment()
        self.env.ensure_env()

        self.load()

    def load_template(self):
        env = JinjaEnv(loader=FileSystemLoader(self.env.template))

        return env.get_template("base.html")

    def load_config(self) -> List[Config]:
        with open(self.env.config, "rb") as fp:
            return [Config(key=key, **data) for key, data in tomllib.load(fp).items()]

    def load_content(self, path: str):
        with open(os.path.join(self.env.content, path), "rb") as fp:
            return tomllib.load(fp)

    def load(self):
        self.cfg = self.load_config()
        self.data = {
            "contact": self.load_content("contact.toml")["contact"],
            "jobs": self.load_content("jobs.toml"),
            "locale": self.load_content("locale.toml"),
            "education": self.load_content("education.toml"),
            "skills-interests": self.load_content("skills-interests.toml"),
        }
        self.template = self.load_template()
