#!/usr/bin/env python3

from resource_management.libraries.script import Script

config = Script.get_config()

fluent_bit_conf_dir = "/etc/fluent-bit"
fluent_bit_conf_file = (
        fluent_bit_conf_dir + "/fluent-bit.conf"
)

fluent_bit_storage_dir = "/var/lib/fluent-bit"

fluent_bit_log_level = config["configurations"][
    "fluent-bit-site"
]["fluent_bit.service.log_level"]

fluent_bit_flush = config["configurations"][
    "fluent-bit-site"
]["fluent_bit.service.flush"]

opensearch_host = config["configurations"][
    "fluent-bit-site"
]["fluent_bit.opensearch.host"]

opensearch_port = config["configurations"][
    "fluent-bit-site"
]["fluent_bit.opensearch.port"]

opensearch_index = config["configurations"][
    "fluent-bit-site"
]["fluent_bit.opensearch.index"]

opensearch_tls = config["configurations"][
    "fluent-bit-site"
]["fluent_bit.opensearch.tls"]