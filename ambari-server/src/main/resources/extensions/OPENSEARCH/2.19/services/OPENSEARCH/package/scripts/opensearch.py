from resource_management import *
from resource_management.core.logger import Logger
from resource_management.core.resources.system import (
    Directory,
    Execute,
    File,
    Link,
)
from resource_management.core.source import Template
from resource_management.libraries.script import Script

import params


class OpenSearch(Script):

    def install(self, env):
        Logger.info("Installing OpenSearch")

        self.install_packages(
            env,
            packages=params.opensearch_packages
        )

        self.configure(env)

    def configure(self, env):
        """
        Generate OpenSearch configuration files.
        """

        Logger.info("Configuring OpenSearch")

        # Configuration directory
        Directory(
            params.opensearch_conf_dir,
            owner=params.opensearch_user,
            group=params.opensearch_group,
            mode="0755",
            create_parents=True
        )

        # Data directory
        Directory(
            params.path_data,
            owner=params.opensearch_user,
            group=params.opensearch_group,
            mode="0750",
            create_parents=True
        )

        # Log directory
        Directory(
            params.path_logs,
            owner=params.opensearch_user,
            group=params.opensearch_group,
            mode="0750",
            create_parents=True
        )

        # OpenSearch main configuration
        TemplateConfig(
            params.opensearch_conf_file,
            owner=params.opensearch_user,
            group=params.opensearch_group,
            mode="0640",
            template_tag=None
        )

        # Java configuration
        File(
            params.opensearch_env_file,
            content=(
                "OPENSEARCH_JAVA_HOME={0}\n"
                "JAVA_HOME={0}\n"
            ).format(params.opensearch_java_home),
            owner="root",
            group="root",
            mode="0644"
        )

        Logger.info(
            "OpenSearch configuration generated at %s",
            params.opensearch_conf_file
        )

    def start(self, env):

        Logger.info("Starting OpenSearch")

        self.configure(env)

        Execute(
            "systemctl start opensearch",
            sudo=True
        )

    def stop(self, env):

        Logger.info("Stopping OpenSearch")

        Execute(
            "systemctl stop opensearch",
            sudo=True
        )

    def status(self, env):

        Execute(
            "systemctl is-active opensearch",
            sudo=True
        )

    def restart(self, env):

        Logger.info("Restarting OpenSearch")

        self.configure(env)

        Execute(
            "systemctl restart opensearch",
            sudo=True
        )

    # def service_check(self, env):
    #
    #     Logger.info("Checking OpenSearch")
    #
    #     Execute(
    #         "curl -sf http://127.0.0.1:{0}/"
    #         .format(params.http_port),
    #         sudo=False
    #     )


if __name__ == "__main__":
    OpenSearch().execute()
