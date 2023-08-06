"""roce.py: Module to check or configure RoCE."""

__author__ = "Zhaojuan Guo"
__copyright__ = "Copyright (c) 2023 Red Hat, Inc. All rights reserved."

from libsan.host.linux import mount, mkdir
from libsan.host.cmdline import run


# check the default RoCE mode
def get_roce_mode(dev_id, port):
    """
    :return:
    """
    # mount the configfs file, # mount -t configfs none /sys/kernel/config
    # create a directory for the device
    # validate what is the used RoCE mode in the default_roce_mode configfs file
    #
    dev_dir = "/sys/kernel/config/rdma_cm/{}/".format(dev_id)
    if mkdir(dev_dir):
        cmd = "cat /sys/kernel/config/rdma_cm/{}/ports/{}/default_roce_mode".format(dev_id, port)
        ret, output = run(cmd, return_output=True, verbose=False)
        print(output)
        return output


# set RoCE mode
def set_roce_mode(dev_id, port, mode):
    """
    :param dev_id: e.g. mlx4_0
    :param port: e.g. 0
    :param mode: v1 or v2
    :return: True of False
    """
    # Change the default RoCE mode
    # For RoCE v1: IB/RoCE v1
    # For RoCE v2: RoCE v2
    dev_dir = "/sys/kernel/config/rdma_cm/{}/".format(dev_id)
    if not mkdir(dev_dir):
        return False
    else:
        _dev_dir = "/sys/kernel/config/rdma_cm/{}/ports/{}/default_roce_mode".format(dev_id, port)
        if mode == "v1":
            cmd = 'echo "IB/RoCE v1" > {}'.format(_dev_dir)
        elif mode == "v2":
            cmd = 'echo "RoCE v2" > {}'.format(_dev_dir)

        if run(cmd) != 0:
            print("FAIL: set_roce_mode - could not set RoCE mode to %s" % mode)
            return False
    return True


def disable_or_enable_roce(bus_name, dis_or_en):
    """
    Disable or enable RoCE by devlink. Note: it only supports mlx5 RoCE.
    @param bus_name: like "0000:06:00.0"
    @param dis_or_en: "true" means enable RoCE, while "false" means disable RoCE
    @return: True if operation succeeds. Otherwise False
    """
    _cmd = "devlink dev param set pci/" + bus_name + " name enable_roce value " + dis_or_en + " cmode driverinit"
    if run(_cmd) != 0:
        return False
    _cmd = "devlink dev reload pci/" + bus_name
    if run(_cmd) != 0:
        return False
    _cmd = "devlink dev param show pci/" + bus_name + " name enable_roce"
    run(_cmd)
    return True
