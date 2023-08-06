"""siw.py: Module to check/configure siw (Soft-iWARP)."""

__author__ = "Zhaojuan Guo"
__copyright__ = "Copyright (c) 2023 Red Hat, Inc. All rights reserved."

from libsan.host.cmdline import run


def siw_setup(link_name="siw_eno2", netdev="eno2"):
    """
    @param link_name: name of the new link
    @param netdev: name of an Ethernet device
    @return: zero if succeed to set up siw. Otherwise, return non-zero
    """
    _cmd = "modprobe siw"
    retcode = run(_cmd)
    if retcode != 0:
        print("ERROR: failed to modprobe siw")
        return retcode
    _cmd = "rdma link add " + link_name + " type siw netdev " + netdev
    retcode = run(_cmd)
    if retcode != 0:
        print("ERROR: add siw link failed")
        return retcode
    run("rdma link show")
    return retcode


def check_siw_paras(link_name="siw_eno2"):
    """
    @param link_name: name of the siw link
    @return: None
    """
    _cmd = "rdma link show " + "| grep " + link_name
    run(_cmd)
    _cmd = "ibv_devinfo -d " + link_name
    run(_cmd)


def siw_delete(link_name="siw_eno2"):
    """
    @param link_name: name of the siw link
    @return: zero if succeed in deleting the siw link, otherwise, return non-zero
    """
    _cmd = "rdma link delete " + link_name
    retcode = run(_cmd)
    if retcode != 0:
        print("ERROR: failed to delete the siw link")
        return retcode
    run("rdma link show")
    return retcode

