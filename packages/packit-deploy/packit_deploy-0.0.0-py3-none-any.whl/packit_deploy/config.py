import constellation
from constellation import config

from packit_deploy.docker_helpers import docker_client


class PackitConfig:
    def __init__(self, path, extra=None, options=None):
        dat = config.read_yaml(f"{path}/packit.yml")
        dat = config.config_build(path, dat, extra, options)
        self.vault = config.config_vault(dat, ["vault"])
        self.network = config.config_string(dat, ["network"])
        self.protect_data = config.config_boolean(dat, ["protect_data"])
        self.volumes = {"outpack": config.config_string(dat, ["volumes", "outpack"])}

        self.container_prefix = config.config_string(dat, ["container_prefix"])
        self.repo = config.config_string(dat, ["repo"])

        self.outpack_name = config.config_string(dat, ["outpack", "server", "name"])
        self.outpack_tag = config.config_string(dat, ["outpack", "server", "tag"])
        self.outpack_ref = constellation.ImageReference(self.repo, self.outpack_name, self.outpack_tag)

        self.packit_db_name = config.config_string(dat, ["packit", "db", "name"])
        self.packit_db_tag = config.config_string(dat, ["packit", "db", "tag"])
        self.packit_db_ref = constellation.ImageReference(self.repo, self.packit_db_name, self.packit_db_tag)

        self.packit_api_name = config.config_string(dat, ["packit", "api", "name"])
        self.packit_api_tag = config.config_string(dat, ["packit", "api", "tag"])
        self.packit_api_ref = constellation.ImageReference(self.repo, self.packit_api_name, self.packit_api_tag)

        self.packit_name = config.config_string(dat, ["packit", "app", "name"])
        self.packit_tag = config.config_string(dat, ["packit", "app", "tag"])
        self.packit_ref = constellation.ImageReference(self.repo, self.packit_name, self.packit_tag)

        self.containers = {
            "outpack-server": "outpack-server",
            "packit-db": "packit-db",
            "packit-api": "packit-api",
            "packit": "packit",
        }

        self.images = {
            "outpack-server": self.outpack_ref,
            "packit-db": self.packit_db_ref,
            "packit-api": self.packit_api_ref,
            "packit": self.packit_ref,
        }

        if "proxy" in dat and dat["proxy"]:
            self.proxy_enabled = config.config_boolean(dat, ["proxy", "enabled"], True)

            if self.proxy_enabled:
                self.proxy_hostname = config.config_string(dat, ["proxy", "hostname"])
                self.proxy_port_http = config.config_integer(dat, ["proxy", "port_http"])
                self.proxy_port_https = config.config_integer(dat, ["proxy", "port_https"])
                ssl = config.config_dict(dat, ["proxy", "ssl"], True)
                self.proxy_ssl_self_signed = ssl is None
                if not self.proxy_ssl_self_signed:
                    self.proxy_ssl_certificate = config.config_string(dat, ["proxy", "ssl", "certificate"], True)
                    self.proxy_ssl_key = config.config_string(dat, ["proxy", "ssl", "key"], True)

                self.proxy_name = config.config_string(dat, ["proxy", "image", "name"])
                self.proxy_tag = config.config_string(dat, ["proxy", "image", "tag"])
                self.proxy_ref = constellation.ImageReference(self.repo, self.proxy_name, self.proxy_tag)
                self.containers["proxy"] = "proxy"
                self.images["proxy"] = self.proxy_ref
                self.volumes["proxy_logs"] = config.config_string(dat, ["volumes", "proxy_logs"])
        else:
            self.proxy_enabled = False

    def get_container(self, name):
        with docker_client() as cl:
            return cl.containers.get(f"{self.container_prefix}-{self.containers[name]}")
