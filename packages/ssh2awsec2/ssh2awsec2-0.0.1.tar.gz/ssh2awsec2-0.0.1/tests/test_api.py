# -*- coding: utf-8 -*-

from ssh2awsec2 import api


def test():
    _ = api


if __name__ == "__main__":
    from ssh2awsec2.tests import run_cov_test

    run_cov_test(__file__, "ssh2awsec2.api", preview=False)
