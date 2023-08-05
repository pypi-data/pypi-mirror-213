"""
.. module:: nodecoordinatorbase
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module contains the :class:`NodeCoordinatorBase` object which is a base
               class for objects create and manage cluster node objects.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>

"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import Any, Dict, List, Optional, Tuple, Union, TYPE_CHECKING

import os
import pprint

from mojo.xmods.exceptions import ConfigurationError, NotOverloadedError

from mojo.xmods.credentials.basecredential import BaseCredential
from mojo.xmods.landscaping.friendlyidentifier import FriendlyIdentifier

from mojo.xmods.landscaping.coordinators.coordinatorbase import CoordinatorBase
from mojo.xmods.landscaping.landscapeparameters import LandscapeActivationParams
from mojo.xmods.landscaping.landscapedevice import LandscapeDevice
from mojo.xmods.landscaping.landscapedevicecluster import LandscapeDeviceCluster
from mojo.xmods.landscaping.landscapedevicegroup import LandscapeDeviceGroup

from mojo.xmods.landscaping.cluster.nodebase import NodeBase


if TYPE_CHECKING:
    from mojo.xmods.landscaping.landscape import Landscape


def format_node_configuration_error(message, osxdev_config):
    """
        Takes an error message and an node configuration info dictionary and
        formats a configuration error message.
    """
    error_lines = [
        message,
        "DEVICE:"
    ]

    dev_repr_lines = pprint.pformat(osxdev_config, indent=4).splitlines(False)
    for dline in dev_repr_lines:
        error_lines.append("    " + dline)
    
    errmsg = os.linesep.join(error_lines)
    return errmsg

class NodeCoordinatorBase(CoordinatorBase):
    """
        The :class:`NodeCoordinatorBase` creates a pool of agents that can be used to
        coordinate the interop activities of the automation process and remote OSX
        node.
    """
    # pylint: disable=attribute-defined-outside-init

    INTEGRATION_CLASS = ""
    CLIENT_TYPE = NodeBase
    CLUSTER_TYPE = LandscapeDeviceCluster

    MUST_INCLUDE_SSH = False

    def __init__(self, lscape: "Landscape", *args, **kwargs):
        super().__init__(lscape, *args, **kwargs)

        self._cl_upnp_hint_to_ip_lookup: Dict[str, str] = {}
        self._cl_ip_to_host_lookup: Dict[str, str] = {}
        return

    def activate(self, activation_params: LandscapeActivationParams):
        """
            Called by the :class:`LandscapeOperationalLayer` in order for the coordinator to be able to
            potentially enhanced devices.
        """
        return

    def attach_protocol_extensions(self, landscape: "Landscape", device_info: Dict[str, Any], device: LandscapeDevice):
        """
            Called when a landscape device is created in order to attach device extensions.
        """
        self.attach_extension_for_ssh(landscape, device_info, device)
        return

    def attach_extension_for_ssh(self, landscape: "Landscape", device_info: Dict[str, Any], device: LandscapeDevice):

        credentials = device.credentials

        ssh_cred = None
        for cred in credentials.values():
            if "ssh" in cred.categories:
                ssh_cred = cred
                break

        ssh_add_error = None
        
        if ssh_cred is not None:
            if "host" in device_info:
                host = device_info["host"]

                users = None
                if "users" in device_info:
                    users = device_info["users"]

                port = 22
                if "port" in device_info:
                    port = device_info["port"]

                pty_params = None
                if "pty_params" in device_info:
                    pty_params = device_info["pty_params"]

                self.create_ssh_agent(device, device_info, host, ssh_cred, 
                                      users=users, port=port, pty_params=pty_params)
            else:
                ssh_add_error = "missing 'host'"
        else:
            ssh_add_error = "missing 'ssh' credential"

        if self.MUST_INCLUDE_SSH and ssh_add_error is not None:
            type_name = type(self).__name__
            err_msg = f"{type_name} client needs to have an 'ssh' credential. ({ssh_add_error})"
            raise ConfigurationError(err_msg)

        return

    def create_cluster_for_devices(self, cluster_name: str, group: LandscapeDeviceGroup,
                                   nodes: List[str], spares: List[str]) -> LandscapeDeviceCluster:
        """
            Called in order to create a cluster object for a given group of devices, list of node
            names and list of spare node names.
        """
        node_devices = {}
        spare_devices = {}

        grplable = group.label

        unexpected_devices = {}

        for dev in group.items:
            node_name = dev.name
            if node_name in nodes:
                node_devices[node_name] = dev
            elif node_name in spares:
                spare_devices[node_name] = dev
            else:
                unexpected_devices[node_name] = dev
        
        if len(unexpected_devices) > 0:
            errmsg_lines = [
                f"The group '{grplable}' contained devices that were not in the nodes or spares lists.",
                "NODES:"
            ]
            for nname in nodes:
                errmsg_lines.append(f"    {nname}")

            errmsg_lines.append("SPARES:")
            for nname in spares:
                errmsg_lines.append(f"    {nname}")

            errmsg_lines.append("UNEXPECTED:")
            for nname in unexpected_devices.keys():
                errmsg_lines.append(f"    {nname}")

            errmsg = os.linesep.join(errmsg_lines)
            raise ConfigurationError(errmsg)

        cluster = self.CLUSTER_TYPE(cluster_name, node_devices, spare_devices, group)

        return cluster

    def create_landscape_device(self, landscape: "Landscape", device_info: Dict[str, Any]) -> Tuple[FriendlyIdentifier, NodeBase]:
        """
            Called to declare a declared landscape device for a given coordinator.
        """
        host = device_info["host"]
        dev_type = device_info["deviceType"]
        fid = FriendlyIdentifier(host, host)

        device = self.CLIENT_TYPE(landscape, self, fid, dev_type, device_info)

        with self.begin_locked_coordinator_scope() as lkscope:
            self._cl_children[device.identity] = device

        self.attach_protocol_extensions(landscape, device_info, device)

        return fid, device

    def create_ssh_agent(self, device: LandscapeDevice, device_info: Dict[str, Any], host: str, cred: BaseCredential,
                         users: Optional[dict] = None, port: int = 22, pty_params: Optional[dict] = None):
        
        if self.MUST_INCLUDE_SSH:
            err_mgs = "if 'MUST_INCLUDE_SSH' is 'True' then 'create_ssh_agent' must be overloaded."
            raise NotOverloadedError(err_mgs)

        return

    def establish_connectivity(self, activation_params: LandscapeActivationParams):
        """
            Called by the :class:`LandscapeOperationalLayer` in order for the coordinator to be able to
            verify connectivity with devices.
        """
        results = []

        cmd: str = "echo 'It Works'"

        for agent in self.children_as_extension:
            host = agent.host
            ipaddr = agent.ipaddr
            try:
                status, stdout, stderr = agent.run_cmd(cmd)
                results.append((host, ipaddr, status, stdout, stderr, None))
            except Exception as xcpt: # pylint: disable=broad-except
                results.append((host, ipaddr, None, None, None, xcpt))

        return results

    def lookup_device_by_host(self, host: str) -> Union[LandscapeDevice, None]:
        """
            Looks up the agent for a device by its hostname.  If the
            agent is not found then the API returns None.

            :param host: The host name of the LandscapeDevice to search for.

            :returns: The found LandscapeDevice or None
        """
        device = None

        self._coord_lock.acquire()
        try:
            if host in self._cl_children:
                device = self._cl_children[host].basedevice
        finally:
            self._coord_lock.release()

        return device

    def lookup_device_by_ip(self, ip) -> Union[LandscapeDevice, None]:
        """
            Looks up the agent for a device by its ip address.  If the
            agent is not found then the API returns None.

            :param ip: The ip address of the LandscapeDevice to search for.

            :returns: The found LandscapeDevice or None
        """
        device = None

        self._coord_lock.acquire()
        try:
            if ip in self._cl_ip_to_host_lookup:
                if ip in self._cl_ip_to_host_lookup:
                    host = self._cl_ip_to_host_lookup[ip]
                    if host in self._cl_children:
                        device = self._cl_children[host].basedevice
        finally:
            self._coord_lock.release()

        return device

    def verify_connectivity(self, cmd: str = "echo 'It Works'", user: Optional[str] = None, raiseerror: bool = True) -> List[tuple]:
        """
            Loops through the nodes in the node pool and utilizes the credentials for the specified user in order to verify
            connectivity with the remote node.

            :param cmd: A command to run on the remote machine in order
                        to verify that osx connectivity can be establish.
            :param user: The name of the user credentials to use for connectivity.
                         If the 'user' parameter is not provided, then the
                         credentials of the default or priviledged user will be used.
            :param raiseerror: A boolean value indicating if this API should raise an Exception on failure.

            :returns: A list of errors encountered when verifying connectivity with the devices managed or watched by the coordinator.
        """
        results = []

        for agent in self.children_as_extension:
            host = agent.host
            ipaddr = agent.ipaddr
            try:
                status, stdout, stderr = agent.run_cmd(cmd)
                results.append((host, ipaddr, status, stdout, stderr, None))
            except Exception as xcpt: # pylint: disable=broad-except
                if raiseerror:
                    raise
                results.append((host, ipaddr, None, None, None, xcpt))

        return results
