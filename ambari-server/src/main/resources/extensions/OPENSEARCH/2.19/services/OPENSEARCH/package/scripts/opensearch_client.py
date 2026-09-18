import os

from resource_management import *
from resource_management.core.logger import Logger
from resource_management.core.resources.system import (
    Directory,
    File,
)
from resource_management.libraries.script import Script

import params


class OpenSearchClient(Script):

    def install(self, env):
        """
        Install OpenSearch client package.
        """

        Logger.info("Installing OpenSearch client")

        self.install_packages(
            env,
            packages=params.opensearch_packages
        )

        self.configure(env)

    def configure(self, env):
        """
        Configure OpenSearch client.
        """

        Logger.info("Configuring OpenSearch client")

        Directory(
            params.opensearch_conf_dir,
            owner=params.opensearch_user,
            group=params.opensearch_group,
            mode="0755",
            create_parents=True
        )

        TemplateConfig(
            params.opensearch_conf_file,
            owner=params.opensearch_user,
            group=params.opensearch_group,
            mode="0640",
            template_tag=None
        )

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

    def status(self, env):
        """
        Check that OpenSearch client files are available.
        """

        if not os.path.exists(
                params.opensearch_conf_file
        ):
            raise ComponentIsNotRunning(
                "OpenSearch client configuration does not exist"
            )


if __name__ == "__main__":
    OpenSearchClient().execute()
