import os
from subprocess import Popen
from typing import List

from cvgen.loader import Loader
from cvgen.models import Config

WKHTMLTOPDF_ARGS = ["wkhtmltopdf", "-L", "5", "-R", "5", "--enable-local-file-access"]


class Builder:
    def __init__(self):
        self.loader = Loader()
        self.loader.load()
        self.env = self.loader.env

    def _add_jobs(self, build: Config, data) -> List[dict]:
        lang = build.lang
        jobs = []

        for job_id in build.jobs:
            print(f"  - Adding job {job_id}")

            source_data = data["jobs"][job_id]
            job_data = {
                "title": source_data["title"][lang],
                "company": source_data["company"],
                "years": source_data["years"],
                "details": source_data["details"][lang],
            }

            jobs.append(job_data)

        return jobs

    def _add_education(self, build: Config, data) -> List[dict]:
        lang = build.lang
        edus = []

        for edu_id in build.education:
            print(f"  - Adding education {edu_id}")

            source_data = data["education"][edu_id]
            edu_data = {
                "title": source_data["title"][lang],
                "location": source_data["location"][lang],
                "years": source_data["years"],
                "details": source_data["details"][lang],
            }

            edus.append(edu_data)

        return edus

    def render_template(self):
        for build in self.loader.cfg:
            if build.disabled:
                continue

            lang = build.lang
            data = self.loader.data

            print(f"Building {build.key}")

            cont = {
                "cfg": build,
                "jobs": self._add_jobs(build, data),
                "contact": data["contact"],
                "locale": data["locale"][lang],
                "education": self._add_education(build, data),
                "skills_interests": {
                    "technical": data["skills-interests"]["technical"][build.skills][lang],
                    "soft": data["skills-interests"]["soft"][lang],
                },
            }

            rendered_str = self.loader.template.render(cont)

            with open(os.path.join(self.env.build, f"{build.key}.html"), "w") as fw:
                fw.write(rendered_str)

    def render_pdf(self):
        for build in self.loader.cfg:
            if build.disabled:
                continue

            source_file = os.path.join(self.env.build, f"{build.key}.html")
            output_file = os.path.join(self.env.output, build.key, f"{build.name}.pdf")

            os.makedirs(os.path.join(self.env.output, build.key), exist_ok=True)

            args = WKHTMLTOPDF_ARGS + [source_file, output_file]
            Popen(args)

    def build(self):
        self.render_template()
        self.render_pdf()
