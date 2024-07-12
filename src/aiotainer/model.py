"""Models for Husqvarna Automower data."""

import logging
import operator
from dataclasses import dataclass, field, fields
from datetime import UTC, datetime, timedelta
from enum import Enum, StrEnum
from re import sub
from typing import Any

from mashumaro import DataClassDictMixin, field_options

# class Agent:
#     version: str



# class AzureCredentials:
#     application_id: str
#     tenant_id: str
#     authentication_key: str


# class Edge:
#     async_mode: bool
#     ping_interval: int
#     snapshot_interval: int
#     command_interval: int



# class Configuration:
#     use_load_balancer: bool
#     use_server_metrics: bool
#     enable_resource_over_commit: bool
#     resource_over_commit_percentage: int
#     storage_classes: List[Any]
#     ingress_classes: List[Any]
#     restrict_default_namespace: bool
#     ingress_availability_per_namespace: bool
#     allow_none_ingress_class: bool



# class Flags:
#     is_server_metrics_detected: bool
#     is_server_ingress_class_detected: bool
#     is_server_storage_detected: bool


# class Kubernetes:
#     snapshots: List[Any]
#     configuration: Configuration
#     flags: Flags


# class PostInitMigrations:
#     migrate_ingresses: bool
#     migrate_gp_us: bool


# class SecuritySettings:
#     allow_bind_mounts_for_regular_users: bool
#     allow_privileged_mode_for_regular_users: bool
#     allow_volume_browser_for_regular_users: bool
#     allow_host_namespace_for_regular_users: bool
#     allow_device_mapping_for_regular_users: bool
#     allow_stack_management_for_regular_users: bool
#     allow_container_capabilities_for_regular_users: bool
#     allow_sysctl_setting_for_regular_users: bool
#     enable_host_management_features: bool



# class HostConfig:
#     network_mode: str


# class COMDockerComposeOneoff(Enum):
#     FALSE = "False"


# class COMDockerComposeVersion(Enum):
#     THE_2202 = "2.20.2"


# class ContainerLabels:
#     com_docker_compose_config_hash: Optional[str]
#     com_docker_compose_container_number: Optional[int]
#     com_docker_compose_depends_on: Optional[str]
#     com_docker_compose_image: Optional[str]
#     com_docker_compose_oneoff: Optional[COMDockerComposeOneoff]
#     com_docker_compose_project: Optional[str]
#     com_docker_compose_project_config_files: Optional[str]
#     com_docker_compose_project_working_dir: Optional[str]
#     com_docker_compose_service: Optional[str]
#     com_docker_compose_version: Optional[COMDockerComposeVersion]
#     org_opencontainers_image_created: Optional[datetime]
#     org_opencontainers_image_description: Optional[str]
#     org_opencontainers_image_documentation: Optional[str]
#     org_opencontainers_image_licenses: Optional[str]
#     org_opencontainers_image_revision: Optional[str]
#     org_opencontainers_image_source: Optional[str]
#     org_opencontainers_image_url: Optional[str]
#     org_opencontainers_image_version: Optional[str]
#     org_opencontainers_image_authors: Optional[str]
#     org_opencontainers_image_base_name: Optional[str]
#     org_opencontainers_image_ref_name: Optional[str]
#     org_opencontainers_image_title: Optional[str]
#     org_opencontainers_image_vendor: Optional[str]
#     org_label_schema_build_date: Optional[datetime]
#     org_label_schema_license: Optional[str]
#     org_label_schema_name: Optional[str]
#     org_label_schema_schema_version: Optional[str]
#     org_label_schema_url: Optional[str]
#     org_label_schema_usage: Optional[str]
#     org_label_schema_vcs_ref: Optional[str]
#     org_label_schema_vcs_url: Optional[str]
#     org_label_schema_vendor: Optional[str]
#     org_label_schema_version: Optional[str]
#     com_docker_compose_replace: Optional[str]
#     description: Optional[str]
#     maintainer: Optional[str]
#     repository: Optional[str]
#     version: Optional[str]
#     website: Optional[str]
#     com_docker_desktop_extension_api_version: Optional[str]
#     com_docker_desktop_extension_icon: Optional[str]
#     com_docker_extension_additional_urls: Optional[str]
#     com_docker_extension_detailed_description: Optional[str]
#     com_docker_extension_publisher_url: Optional[str]
#     com_docker_extension_screenshots: Optional[str]
#     io_portainer_server: Optional[bool]


class Mode(Enum):
    EMPTY = ""
    RW = "rw"
    Z = "z"


class Propagation(Enum):
    EMPTY = ""
    RPRIVATE = "rprivate"


class MountType(Enum):
    BIND = "bind"
    VOLUME = "volume"


# class Mount:
#     type: MountType
#     source: str
#     destination: str
#     mode: Mode
#     rw: bool
#     propagation: Propagation
#     name: Optional[str]
#     driver: Optional[str]



# class Networks:
#     vaultwarden_default: Optional[BaikalDefault]
#     seafile_default: Optional[BaikalDefault]
#     linkding_default: Optional[BaikalDefault]
#     baikal_default: Optional[BaikalDefault]
#     bridge: Optional[BaikalDefault]


# class NetworkSettings:
#     networks: Networks


class PortType(Enum):
    TCP = "tcp"


# class Port:
#     private_port: int
#     type: PortType
#     ip: Optional[str]
#     public_port: Optional[int]


class State(Enum):
    RUNNING = "running"
    EXITED = "exited"

@dataclass
class Container(DataClassDictMixin):
    id: str = field(metadata=field_options(alias="Id"))
    names: list[str] = field(metadata=field_options(alias="Names"))
    image: str = field(metadata=field_options(alias="Image"))
    # image_id: str
    # command: str
    # created: int
    # ports: List[Port]
    # labels: ContainerLabels
    state: State = field(metadata=field_options(alias="State"))
    # status: str
    # host_config: HostConfig
    # network_settings: NetworkSettings
    # mounts: List[Mount]



# class Image:
#     containers: int
#     created: int
#     id: str
#     labels: Union[ContainerLabels, str]
#     parent_id: str
#     repo_digests: List[str]
#     repo_tags: Union[List[str], str]
#     shared_size: int
#     size: int
#     virtual_size: int



# class Commit:
#     id: str
#     expected: str



# class Plugins:
#     volume: List[str]
#     network: List[str]
#     authorization: str
#     log: List[str]


# class DockerIo:
#     name: str
#     mirrors: List[Any]
#     secure: bool
#     official: bool



# class IndexConfigs:
#     docker_io: DockerIo


# class RegistryConfig:
#     allow_nondistributable_artifacts_cid_rs: str
#     allow_nondistributable_artifacts_hostnames: str
#     insecure_registry_cid_rs: List[str]
#     index_configs: IndexConfigs
#     mirrors: str


# class IoContainerdRuncV2:
#     path: str


# class Runtimes:
#     io_containerd_runc_v2: IoContainerdRuncV2
#     runc: IoContainerdRuncV2


# class Swarm:
#     node_id: str
#     node_addr: str
#     local_node_state: str
#     control_available: bool
#     error: str
#     remote_managers: str



# class Info:
#     id: UUID
#     containers: int
#     containers_running: int
#     containers_paused: int
#     containers_stopped: int
#     images: int
#     driver: str
#     driver_status: List[List[str]]
#     plugins: Plugins
#     memory_limit: bool
#     swap_limit: bool
#     cpu_cfs_period: bool
#     cpu_cfs_quota: bool
#     cpu_shares: bool
#     cpu_set: bool
#     pids_limit: bool
#     i_pv4_forwarding: bool
#     bridge_nf_iptables: bool
#     bridge_nf_ip6_tables: bool
#     debug: bool
#     n_fd: int
#     oom_kill_disable: bool
#     n_goroutines: int
#     system_time: datetime
#     logging_driver: str
#     cgroup_driver: str
#     cgroup_version: int
#     n_events_listener: int
#     kernel_version: str
#     operating_system: str
#     os_version: str
#     os_type: str
#     architecture: str
#     index_server_address: str
#     registry_config: RegistryConfig
#     ncpu: int
#     mem_total: int
#     generic_resources: str
#     docker_root_dir: str
#     http_proxy: str
#     https_proxy: str
#     no_proxy: str
#     name: str
#     labels: List[Any]
#     experimental_build: bool
#     server_version: str
#     runtimes: Runtimes
#     default_runtime: str
#     swarm: Swarm
#     live_restore_enabled: bool
#     isolation: str
#     init_binary: str
#     containerd_commit: Commit
#     runc_commit: Commit
#     init_commit: Commit
#     security_options: List[str]
#     warnings: str


# class ConfigFrom:
#     network: str


# class TeamAccessPolicies:
#     pass


# class ConfigElement:
#     subnet: str
#     gateway: str


# class IPAM:
#     driver: str
#     options: str
#     config: Union[List[ConfigElement], str]


# class NetworkLabels:
#     com_docker_compose_network: Optional[str]
#     com_docker_compose_project: Optional[str]
#     com_docker_compose_version: Optional[COMDockerComposeVersion]


# class Options:
#     com_docker_network_bridge_default_bridge: Optional[bool]
#     com_docker_network_bridge_enable_icc: Optional[bool]
#     com_docker_network_bridge_enable_ip_masquerade: Optional[bool]
#     com_docker_network_bridge_host_binding_ipv4: Optional[str]
#     com_docker_network_bridge_name: Optional[str]
#     com_docker_network_driver_mtu: Optional[int]


# class Network:
#     name: str
#     id: str
#     created: datetime
#     scope: str
#     driver: str
#     enable_i_pv6: bool
#     ipam: IPAM
#     internal: bool
#     attachable: bool
#     ingress: bool
#     config_from: ConfigFrom
#     config_only: bool
#     containers: TeamAccessPolicies
#     options: Options
#     labels: NetworkLabels


# class Details:
#     api_version: Optional[str]
#     arch: Optional[str]
#     build_time: Optional[datetime]
#     experimental: Optional[bool]
#     git_commit: str
#     go_version: Optional[str]
#     kernel_version: Optional[str]
#     min_api_version: Optional[str]
#     os: Optional[str]



# class Component:
#     name: str
#     version: str
#     details: Details


# class Platform:
#     name: str


# class Version:
#     platform: Platform
#     components: List[Component]
#     version: str
#     api_version: str
#     min_api_version: str
#     git_commit: str
#     go_version: str
#     os: str
#     arch: str
#     kernel_version: str
#     build_time: datetime


# class Volume:
#     created_at: datetime
#     driver: str
#     labels: str
#     mountpoint: str
#     name: str
#     options: str
#     scope: str


# class Volumes:
#     volumes: list[Volume]
#     warnings: str


@dataclass
class DockerSnapshotRaw(DataClassDictMixin):
    containers: list[Container] = field(metadata=field_options(alias="Containers"))
    #volumes: Volumes = field(metadata=field_options(alias="Volumes"))
    #networks: list[Network] = field(metadata=field_options(alias="Network"))
    #images: list[Image] = field(metadata=field_options(alias="Image"))
    #info: Info = field(metadata=field_options(alias="Info"))
    #version: Version = field(metadata=field_options(alias="Version"))

@dataclass
class Snapshot(DataClassDictMixin):
    time: int = field(metadata=field_options(alias="Time"))
    docker_version: str = field(metadata=field_options(alias="DockerVersion"))
    swarm: bool = field(metadata=field_options(alias="Swarm"))
    total_cpu: int = field(metadata=field_options(alias="TotalCPU"))
    total_memory: int = field(metadata=field_options(alias="TotalMemory"))
    running_container_count: int = field(metadata=field_options(alias="RunningContainerCount"))
    stopped_container_count: int = field(metadata=field_options(alias="StoppedContainerCount"))
    healthy_container_count: int = field(metadata=field_options(alias="HealthyContainerCount"))
    unhealthy_container_count: int = field(metadata=field_options(alias="UnhealthyContainerCount"))
    volume_count: int = field(metadata=field_options(alias="VolumeCount"))
    image_count: int = field(metadata=field_options(alias="ImageCount"))
    service_count: int = field(metadata=field_options(alias="ServiceCount"))
    stack_count: int = field(metadata=field_options(alias="StackCount"))
    docker_snapshot_raw: DockerSnapshotRaw = field(metadata=field_options(alias="DockerSnapshotRaw"))
    node_count: int = field(metadata=field_options(alias="NodeCount"))
    gpu_use_all: bool = field(metadata=field_options(alias="GpuUseAll"))
    gpu_use_list: list[Any] = field(metadata=field_options(alias="GpuUseList"))

@dataclass
class TLSConfig(DataClassDictMixin):
    tls: bool = field(metadata=field_options(alias="TLS"))
    tls_skip_verify: bool = field(metadata=field_options(alias="TLSSkipVerify"))


@dataclass
class NodeData(DataClassDictMixin):
    id: int = field(metadata=field_options(alias="Id"))
    name: str = field(metadata=field_options(alias="Name"))
    type: int = field(metadata=field_options(alias="Type"))
    url: str = field(metadata=field_options(alias="URL"))
    group_id: int = field(metadata=field_options(alias="GroupId"))
    public_url: str = field(metadata=field_options(alias="PublicURL"))
    gpus: list[Any] = field(metadata=field_options(alias="Gpus"))
    tls_config: TLSConfig = field(metadata=field_options(alias="TLSConfig"))
    #azure_credentials: AzureCredentials
    #tag_ids: list[Any]
    status: int = field(metadata=field_options(alias="Status"))
    snapshots: list[Snapshot] = field(metadata=field_options(alias="Snapshots"))
    #user_access_policies: TeamAccessPolicies
    #team_access_policies: TeamAccessPolicies
    #edge_key: str
    #edge_checkin_interval: int
    #kubernetes: Kubernetes
    #compose_syntax_max_version: str
    #security_settings: SecuritySettings
    #last_check_in_date: int
    #query_date: int
    #heartbeat: bool
    #user_trusted: bool
    #post_init_migrations: PostInitMigrations
    #edge: Edge
    #agent: Agent
    enable_gpu_management: bool = field(metadata=field_options(alias="EnableGPUManagement"))
    authorized_users: str = field(metadata=field_options(alias="AuthorizedUsers"))
    authorized_teams: str = field(metadata=field_options(alias="AuthorizedTeams"))
    tags: str = field(metadata=field_options(alias="Tags"))
    is_edge_device: bool = field(metadata=field_options(alias="IsEdgeDevice"))

@dataclass
class MowerList(DataClassDictMixin):
    """DataClass for a list of all mowers."""

    data: list[NodeData]