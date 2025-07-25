# -*- coding: utf-8 -*- #
# Copyright 2023 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Flags and helpers for the container related commands."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import arg_parsers


def AddAuthProviderCmdPath(parser):
  parser.add_argument(
      '--auth-provider-cmd-path',
      help="""
      Path to the gcloud executable for the auth provider field in kubeconfig.
      """,
  )


def AddAdminUsers(parser):
  parser.add_argument(
      '--admin-users',
      help="""
      Username (Google email address) of the user who should be granted
      cluster-admin initially. This currently supports exactly one admin. If
      not set, the account issuing the creation request will be used by
      default.
      """,
  )


def AddClusterIPV4CIDR(parser):
  parser.add_argument(
      '--cluster-ipv4-cidr',
      default='10.0.0.0/17',
      help="""
      All pods in the cluster are assigned an RFC1918 IPv4 address from this
      block. This field cannot be changed after creation.
      """,
  )


def AddServicesIPV4CIDR(parser):
  parser.add_argument(
      '--services-ipv4-cidr',
      default='10.96.0.0/12',
      help="""
      All services in the cluster are assigned an RFC1918 IPv4 address from
      this block. This field cannot be changed after creation.
      """,
  )


def AddDefaultMaxPodsPerNode(parser):
  parser.add_argument(
      '--default-max-pods-per-node',
      help='The default maximum number of pods per node.',
  )


def AddFleetProject(parser):
  parser.add_argument(
      '--fleet-project',
      help='Name of the Fleet host project where the cluster is registered.',
  )


def AddLabels(parser):
  parser.add_argument(
      '--labels',
      metavar='KEY=VALUE',
      type=arg_parsers.ArgDict(),
      help="""
      List of label KEY=VALUE pairs to add.

      Keys must start with a lowercase character and contain only hyphens
      (-), underscores (```_```), lowercase characters, and numbers. Values must
      contain only hyphens (-), underscores (```_```), lowercase characters, and
      numbers.
      """,
  )


def AddMaintenanceWindowRecurrence(parser):
  parser.add_argument(
      '--maintenance-window-recurrence',
      help="""
      An RFC 5545 (https://tools.ietf.org/html/rfc5545#section-3.8.5.3)
        recurrence rule for how the cluster maintenance window recurs. They go
        on for the span of time between the start and the end time. E.g.
        FREQ=WEEKLY;BYDAY=SU.
      """,
  )


def AddMaintenanceWindowEnd(parser):
  parser.add_argument(
      '--maintenance-window-end',
      help="""
      End time of the recurring cluster maintenance window in the RFC 3339
      (https://www.ietf.org/rfc/rfc3339.txt) format. E.g.
      "2021-01-01T00:00:00Z" or "2021-01-01T00:00:00-05:00"
      """,
  )


def AddMaintenanceWindowStart(parser):
  parser.add_argument(
      '--maintenance-window-start',
      help="""
      Start time of the recurring cluster maintenance window in the RFC 3339
      (https://www.ietf.org/rfc/rfc3339.txt) format. E.g.
      "2021-01-01T00:00:00Z" or "2021-01-01T00:00:00-05:00"
      """,
  )


def AddClusterIPV6CIDR(parser):
  parser.add_argument(
      '--cluster-ipv6-cidr',
      help="""
      If specified, all pods in the cluster are assigned an RFC4193 IPv6 address
      from this block. This field cannot be changed after creation.
      """,
  )


def AddServicesIPV6CIDR(parser):
  parser.add_argument(
      '--services-ipv6-cidr',
      help="""
      If specified, all services in the cluster are assigned an RFC4193 IPv6
      address from this block. This field cannot be changed after creation.
      """,
  )


def AddControlPlaneKMSKey(parser):
  parser.add_argument(
      '--control-plane-kms-key',
      help="""
      Google Cloud KMS key that will be used to secure persistent disks of the
      control plane VMs of a remote control plane cluster. The Edge Container
      service account for this project must have
      `roles/cloudkms.cryptoKeyEncrypterDecrypter` on the key.

      If not provided, a Google-managed key will be used by default.
      """,
  )


def AddSystemAddonsConfig(parser):
  parser.add_argument(
      '--system-addons-config',
      type=arg_parsers.YAMLFileContents(),
      help="""
      If specified as a YAML/JSON file, customized configuration in this file
      will be applied to the system add-ons.

      For example,

      {
        "systemAddonsConfig": {
          "ingress": {
            "disabled": true,
            "ipv4_vip": "10.0.0.1"
          }
        }
      }
      """,
  )


def AddExternalLbIpv4AddressPools(parser):
  parser.add_argument(
      '--external-lb-ipv4-address-pools',
      type=arg_parsers.ArgList(),
      metavar='EXTERNAL_LB_IPV4_ADDRESS',
      help="""
      IPv4 address pools that are used for data plane load balancing of
      local control plane clusters. Existing pools cannot be updated
      after cluster creation; only adding new pools is allowed.
      Each address pool must be specified as one of the following
      two types of values:
        1. A IPv4 address range, for example, "10.0.0.1-10.0.0.10". A range that contains a single IP (e.g. "10.0.0.1-10.0.0.1") is allowed.
        2. A IPv4 CIDR block, for example, "10.0.0.1/24"
      Use comma when specifying multiple address pools, for example:
        --external-lb-ipv4-address-pools 10.0.0.1-10.0.0.10,10.0.0.1/24
      """,
  )


def AddExternalLbIpv6AddressPools(parser):
  parser.add_argument(
      '--external-lb-ipv6-address-pools',
      type=arg_parsers.ArgList(),
      metavar='EXTERNAL_LB_IPV6_ADDRESS',
      help="""
      IPv6 address pools that are used for data plane load balancing of
      local control plane clusters. Existing pools cannot be updated
      after cluster creation; only adding new pools is allowed.
      Each address pool must be specified as one of the following
      two types of values:
        1. A IPv6 address range, for example, "2001:db8::1-2001:db8::a". A range that contains a single IP (e.g. "2001:db8::1-2001:db8::1") is allowed.
        2. A IPv6 CIDR block, for example, "2001:db8::/120"
      Use comma when specifying multiple address pools, for example:
        --external-lb-ipv6-address-pools 2001:db8::1-2001:db8::a,2001:db8::/120
      """,
  )


def AddExternalLoadBalancerAddressPools(parser):
  """Adds external load balancer address pools."""

  external_lb_config_address_pools_help_text = """
      Path to a YAML/JSON file containing external load balancer pool configuration.
      External load balancer pools are used for data plane load balancing of
      local control plane clusters, with custom config such as address pool
      name. Either --external-lb-ipv4-address-pools or --external-lb-address-pools
      should be specified.
      Existing pools cannot be updated after cluster creation; only adding new
      pools is allowed currently.

      For example,

      ```
      {
        "externalLoadBalancerAddressPools": [
          {
            "addressPool": "MyLoadBalancerPool",
            "ipv4Range": ["10.200.0.200-10.200.0.204","10.200.0.300/30"],
            "avoidBuggyIps": "false",
            "manualAssign": "true"
          }
        ]
      }
      ```

      *address_pool*::: Optional. A name that identifies an address pool. If a name is not specified, an auto-generated one will be used.

      *ipv4_range*::: Mandatory. One or more ipv4 address range, each must be specified as one
      of the following two types of values:

        1. A IPv4 address range, for example, "10.0.0.1-10.0.0.10". A range that contains a single IP (e.g. "10.0.0.1-10.0.0.1") is allowed.

        2. A IPv4 CIDR block, for example, "10.0.0.1/24"

      *ipv6_range*::: Optional. One or more ipv6 address range, each must be specified as one
      of the following two types of values:

        1. A IPv6 address range, for example, "2001:db8::1-2001:db8::a". A range that contains a single IP (e.g. "2001:db8::1-2001:db8::1") is allowed.

        2. A IPv6 CIDR block, for example, "2001:db8::/120"

      *avoid_buggy_ips*::: Optional. If true, the pool omits IP addresses
      ending in .0 and .255. Some network hardware drops traffic to these
      special addresses.
      Its default value is false.

      *manual_assign*::: Optional. If true, addresses in this pool are not
      automatically assigned to Kubernetes Services. If true, an IP address in
      this pool is used only when it is specified explicitly by a service.
      Its default value is false.
  """

  parser.add_argument(
      '--external-lb-address-pools',
      help=external_lb_config_address_pools_help_text,
      type=arg_parsers.YAMLFileContents(),
  )


def AddControlPlaneNodeLocation(parser):
  parser.add_argument(
      '--control-plane-node-location',
      help="""
      Google Edge Cloud zone where the local control plane nodes
      will be created.
      """,
  )


def AddControlPlaneNodeCount(parser):
  parser.add_argument(
      '--control-plane-node-count',
      help="""
      The number of local control plane nodes in a cluster. Use one to create
      a single-node control plane or use three to create a high availability
      control plane.
      Any other numbers of nodes will not be accepted.
      """,
  )


def AddControlPlaneMachineFilter(parser):
  parser.add_argument(
      '--control-plane-machine-filter',
      help="""
      Only machines matching this filter will be allowed to host
      local control plane nodes.
      The filtering language accepts strings like "name=<name>",
      and is documented here: [AIP-160](https://google.aip.dev/160).
      """,
  )


def AddControlPlaneSharedDeploymentPolicy(parser):
  parser.add_argument(
      '--control-plane-shared-deployment-policy',
      help="""
      Policy configuration about how user application is deployed for
      local control plane cluster. It supports two values, ALLOWED and
      DISALLOWED. ALLOWED means that user application can be deployed on
      control plane nodes. DISALLOWED means that user application can not be
      deployed on control plane nodes. Instead, it can only be deployed on
      worker nodes. By default, this value is DISALLOWED. The input is case
      insensitive.
      """,
  )


def AddControlPlaneNodeStorageSchema(parser):
  parser.add_argument(
      '--control-plane-node-storage-schema',
      help="""
      Name for the storage schema of control plane nodes.
      """,
  )


def AddLROMaximumTimeout(parser):
  parser.add_argument(
      '--lro-timeout',
      help="""
      Overwrite the default LRO maximum timeout.
      """,
  )


def AddVersion(parser):
  parser.add_argument(
      '--version',
      help="""
      Target cluster version. For example: "1.5.0".
      """,
  )


def AddReleaseChannel(parser):
  parser.add_argument(
      '--release-channel',
      default='RELEASE_CHANNEL_UNSPECIFIED',
      help="""
      Release channel a cluster is subscribed to. It supports two values,
      NONE and REGULAR. NONE is used to opt out of any release channel. Clusters
      subscribed to the REGULAR channel will be automatically upgraded to
      versions that are considered GA quality, and cannot be manually upgraded.
      Additionally, if the REGULAR channel is used, a specific target version
      cannot be set with the 'version' flag. If left unspecified, the release
      channel will default to REGULAR.
      """,
  )


def AddUpgradeVersion(parser):
  parser.add_argument(
      '--version',
      required=True,
      help="""
      Target cluster version to upgrade to. For example: "1.5.1".
      """,
  )


def AddUpgradeSchedule(parser):
  parser.add_argument(
      '--schedule',
      required=True,
      help="""
      Schedule to upgrade a cluster after the request is acknowledged by Google.
      Support values: IMMEDIATELY.
      """,
  )


def AddOfflineCredential(parser):
  parser.add_argument(
      '--offline-credential',
      action='store_true',
      help="""
      Once specified, an offline credential will be generated for the cluster.
      """,
  )


def AddUseGoogleManagedKey(parser):
  parser.add_argument(
      '--use-google-managed-key',
      action='store_true',
      help="""
      Once specified, a Google-managed key will be used for the control plane
      disk encryption.
      """,
  )


def AddNodeCount(parser, required=True):
  parser.add_argument(
      '--node-count',
      required=required,
      help="""
      Default nodeCount used by this node pool.
      """,
  )


def AddNodeLocation(parser):
  parser.add_argument(
      '--node-location',
      required=True,
      help="""
      Google Edge Cloud zone where nodes in this node pool will be created.
      """,
  )


def AddMachineFilter(parser):
  parser.add_argument(
      '--machine-filter',
      help="""
      Only machines matching this filter will be allowed to join the node
      pool. The filtering language accepts strings like "name=<name>", and is
      documented in more detail at https://google.aip.dev/160.
      """,
  )


def AddLocalDiskKMSKey(parser):
  parser.add_argument(
      '--local-disk-kms-key',
      help="""
      Google Cloud KMS key that will be used to secure local disks on nodes
      in this node pool. The Edge Container service account for this project
      must have `roles/cloudkms.cryptoKeyEncrypterDecrypter` on the key.

      If not provided, a Google-managed key will be used instead.
      """,
  )


def AddNodeLabelsForCreateNodePool(parser):
  parser.add_argument(
      '--node-labels',
      help="""
      Comma-delimited list of key-value pairs that comprise labels for the
      individual nodes in the node pool. This flag sets the Kubernetes
      labels, unlike `--labels` which sets the cloud resource labels.
      """,
      metavar='KEY=VALUE',
      type=arg_parsers.ArgDict(),
  )


def AddNodeLabelsForUpdateNodePool(parser):
  parser.add_argument(
      '--node-labels',
      help="""
      Comma-delimited list of key-value pairs that comprise labels for the
      individual nodes in the node pool. This flag updates the Kubernetes
      labels, unlike `--update-labels`, `--remove-labels`, and `--clear-labels`
      which update the cloud resource labels.
      """,
      metavar='KEY=VALUE',
      type=arg_parsers.ArgDict(),
  )


def AddNodeStorageSchema(parser):
  parser.add_argument(
      '--node-storage-schema',
      help="""
      Name for the storage schema of worker nodes.
      """,
  )


def AddOfflineRebootTtL(parser):
  parser.add_argument(
      '--offline-reboot-ttl',
      type=arg_parsers.Duration(),
      help="""
        Specifies the maximum duration a node can reboot offline (without
        connection to Google) and then rejoin its cluster to resume its
        designated workloads. This duration is relative to the machine's most
        recent connection to Google. The maximum allowed duration is 7 days.
        To disallow offline reboot, set the duration to "PT0S". The parameter
        should be an ISO 8601 duration string, for example, "P1DT1H2M3S".
      """,
  )


def AddZoneStorageKMSKey(parser):
  parser.add_argument(
      '--zone-storage-kms-key',
      help="""
      Google Cloud KMS key that will be used to encrypt and decrypt the root key
      for zone storage encryption. The zone storage KMS key is only
      applicable to the storage infra cluster. The Edge Container service
      account for this project must have
      `roles/cloudkms.cryptoKeyEncrypterDecrypter` on the key.

      If not provided, a Google-managed key will be used by default.
      """,
  )


def AddContainerDefaultRuntimeClass(parser):
  parser.add_argument(
      '--container-default-runtime-class',
      help="""
      Name of the default runtime class for containers. It supports two values
      RUNC and GVISOR.
      """,
  )


def AddEnableClusterIsolation(parser):
  parser.add_argument(
      '--enable-cluster-isolation',
      help="""
      If set, the cluster will be created in a secure cluster isolation mode.
      """,
  )


def AddEnableGoogleGroupAuthentication(parser):
  parser.add_argument(
      '--enable-google-group-authentication',
      action='store_true',
      help="""
      If set, the cluster will be configured to use Google Group authentication.
      """,
  )


def AddEnableRemoteBackup(parser):
  parser.add_argument(
      '--enable-remote-backup',
      action='store_true',
      hidden=True,
      help="""
      If set, the cluster will be created with remote backup featureenabled.
      """,
  )
