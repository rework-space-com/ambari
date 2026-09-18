import os

from resource_management.libraries.functions import format
from resource_management.libraries.functions.default import default
from resource_management.libraries.script import Script


config = Script.get_config()

hostname = config["hostname"]

opensearch_user = "opensearch"
opensearch_group = "opensearch"

opensearch_home = "/usr/share/opensearch"
opensearch_conf_dir = "/etc/opensearch"

opensearch_conf_file = os.path.join(
    opensearch_conf_dir,
    "opensearch.yml"
)

opensearch_env_file = "/etc/sysconfig/opensearch"

opensearch_data_dir = default(
    "/var/lib/opensearch"
)

opensearch_log_dir = default(
    "/var/log/opensearch"
)

opensearch_java_home = default(
    "/usr/lib/jvm/java-17-openjdk"
)

# Ambari configuration
opensearch_site = config["configurations"]["opensearch-site"]["properties"]

cluster_name = opensearch_site.get(
    "cluster.name",
    "hdp-opensearch"
)

configured_node_name = opensearch_site.get(
    "node.name",
    ""
)

node_name = configured_node_name or hostname

network_host = opensearch_site.get(
    "network.host",
    "0.0.0.0"
)

http_port = int(
    opensearch_site.get(
        "http.port",
        "9200"
    )
)

transport_port = int(
    opensearch_site.get(
        "transport.port",
        "9300"
    )
)

discovery_seed_hosts = opensearch_site.get(
    "discovery.seed_hosts",
    ""
)

initial_cluster_manager_nodes = opensearch_site.get(
    "cluster.initial_cluster_manager_nodes",
    ""
)

path_data = opensearch_site.get(
    "path.data",
    opensearch_data_dir
)

path_logs = opensearch_site.get(
    "path.logs",
    opensearch_log_dir
)

security_disabled = opensearch_site.get(
    "plugins.security.disabled",
    "false"
)

opensearch_packages = [
    "opensearch"
]
