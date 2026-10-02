#!/usr/bin/env python3

from resource_management.core.logger import Logger
from resource_management.core.resources.system import (
    Directory,
    File,
    Execute,
)
from resource_management.core.source import Template
from resource_management.libraries.script import Script


class FluentBit(Script):

    def install(self, env):

        self.install_packages(env)

    def configure(self, env):

        import params

        Directory(
            params.fluent_bit_conf_dir,
            owner="root",
            group="root",
            mode=0o755,
            create_parents=True,
        )

        Directory(
            params.fluent_bit_storage_dir,
            owner="fluent-bit",
            group="fluent-bit",
            mode=0o750,
            create_parents=True,
        )

        File(
            params.fluent_bit_conf_file,
            content=Template("fluent-bit.conf.j2"),
            owner="root",
            group="root",
            mode=0o640,
        )

        Logger.info("Fluent Bit configuration generated")

    def start(self, env):

        self.configure(env)

        Execute(
            "systemctl enable fluent-bit",
            user="root",
        )

        Execute(
            "systemctl restart fluent-bit",
            user="root",
        )

    def stop(self, env):

        Execute(
            "systemctl stop fluent-bit",
            user="root",
        )

    def status(self, env):

        Execute(
            "systemctl is-active --quiet fluent-bit",
            user="root",
        )


if __name__ == "__main__":
    FluentBit().execute()