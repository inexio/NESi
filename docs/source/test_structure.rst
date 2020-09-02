.. _test_structure:

**************
Test Structure
**************

Test Framework
##############

NESi´s test framework is `pytest <https://docs.pytest.org/en/stable/>`_.

Because of NESi´s API Server and client structure the normal testing method of pytest is not possible.
Therefore the testing behaviour of NESi is integrated into the project´s architecture.


Special test behaviour
######################

How to start tests
******************

Tests can be started with the following command structure:

    % ./bootup/restapi.sh --test-alcatel-commands

For other vendors replace 'alcatel' with your desired vendor, or use:

    % ./bootup/restapi.sh --help


At the beginning of the tests the API boots up and the CLI will start to receive test inputs from pytest. Therefore the
`CLI <https://github.com/inexio/NESi/blob/master/cli.py#L88>`_ starts pytest.main with vendor-specific arguments.
Both test types, unit and integration tests, are included.

Where you can find the tests
****************************

You can find the complete test structure in the `test_cases <https://github.com/inexio/NESi/tree/master/test_cases>`_ directory.
The entry point of all test are the `test_core <https://github.com/inexio/NESi/blob/master/test_cases/unit_tests/test_core.py>`_ and
the vendor specific tests can be found in the corresponding folders.

How to create tests
*******************

To create a new test for a specific vendor, the Testcore class must be extended to work with the api model.
Furthermore the test functions must start with `test_`.

For more informations about writing test please take a look at `TestAlcatel <https://github.com/inexio/NESi/blob/master/test_cases/unit_tests/alcatel/test_alcatel.py>`_.

Test types
##########

+ The "unit tests" are used to test the databasemodel itself

+ The "integration test" are used to test the correct implementation of the commands

The integration tests use .txt files with commands as I/O streams of the cli.

Github workflows/actions with test badges
#########################################

For every push on our master branch the tests for every vendor start automatically in a seperate workflow.
Test badges are linked in the README.md.
