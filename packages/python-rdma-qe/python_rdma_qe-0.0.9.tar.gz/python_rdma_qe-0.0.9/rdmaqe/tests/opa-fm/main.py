"""opa-fm functional test module"""

__author__ = "Zhaojuan Guo"
__copyright__ = "Copyright (c) 2023 Red Hat, Inc. All rights reserved."

from rdmaqe.rdma.general import is_opa_device
from rdmaqe.common.tc import Test
from rdmaqe.rdma.opa import opa_setup
from rdmaqe.common.file_libs import configure_file

import libsan.host.linux as linux
from libsan.host.cmdline import run

from stqe.host.atomic_run import atomic_run

import sys


def test(tc):
    print("\n#######################################\n")
    print("INFO: Testing opa-fm.")

    # pre-test
    # Skip if no OPA device found on the testing machine
    if not is_opa_device():
        tc.tskip("No OPA device found on this testing machine.")
        return 2
    # setup for OPA
    #opa_setup()
    # host file
    _hosts = None
    if _hosts is None:
        _hosts = linux.hostname()
        configure_file("/etc/opa/hosts", _hosts)
    # Remote PMA query.
    # First get a valid remote LID. The chain below will get the last listed LID in the fabric.
    # Why the last LID? Because assuming the SM is running on this node, this node will
    # be listed first. The one that is last should therefore be a remote LID.
    cmd = "opasaquery | grep 'Type: FI' | tail -1 | awk '{print $2}'"
    ret, out = remote_LID = run(cmd, return_output=True)
    if ret == 0:
        tc.tfail()

    #_cmd = "opapmaquery -l " + remote_LID + " -m 0"
    #tc.tok(_cmd)
    #tc.tok("/usr/sbin/opafmcmdall smLogLevel 7")
    # post-test


def main():
    test_class = Test()

    ret = test(test_class)
    print("Test return code: %s" % ret)

    if not test_class.tend():
        print("FAIL: test failed")
        sys.exit(1)
    if ret == 2:
        print("SKIP: test has been skipped because no OPA device found on the testing machines.")
        sys.exit(2)

    print("PASS: opa-fm functional test passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
