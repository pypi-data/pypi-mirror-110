# uw-restclients-attestation
Restclient for Attestations Service

[![Build Status](https://github.com/uw-it-aca/uw-restclients-attest/workflows/tests/badge.svg?branch=main)](https://github.com/uw-it-aca/uw-restclients-attest/actions)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/uw-restclients-attest/badge.svg?branch=main)](https://coveralls.io/github/uw-it-aca/uw-restclients-attest?branch=main)
[![PyPi Version](https://img.shields.io/pypi/v/uw-restclients-attest.svg)](https://pypi.python.org/pypi/uw-restclients-attest)
![Python versions](https://img.shields.io/pypi/pyversions/uw-restclients-attest.svg)

Installation:

    pip install UW-RestClients-Attest

To use this client, you'll need these settings in your application or script:

    # Specifies whether requests should use live or mocked resources,
    # acceptable values are 'Live' or 'Mock' (default)
    RESTCLIENTS_ATTEST_DAO_CLASS='Live'
    RESTCLIENTS_ATTEST_AUTH_DAO_CLASS='Live'
    RESTCLIENTS_ATTEST_AUTH_SECRET=
    RESTCLIENTS_ATTEST_AUTH_HOST=''

Optional settings:

    # Customizable parameters for urllib3
    RESTCLIENTS_ATTEST_HOST=''
    RESTCLIENTS_ATTEST_TIMEOUT=5
    RESTCLIENTS_ATTEST_POOL_SIZE=10
