*** Settings ***
Documentation   Test handling of single line execution
...
...             This calls the single line execution with the dummy experiment.
...             The test then monitors that the execution returns 2 values as
...             specified by the palaestrai_runner module.

Library         Process
Library         OperatingSystem
Suite Teardown  Clean Files

*** Keywords ***
Clean Files
    Remove File                     ${TEMPDIR}${/}stdout.txt
    Remove File                     ${TEMPDIR}${/}stderr.txt

*** Test Cases ***
Call single line execution with the dummy experiment file.
    ${result} =                     Run Process    python     ${CURDIR}${/}single_line_test.py    ${CURDIR}${/}..${/}fixtures${/}dummy_run.yaml    stdout=${TEMPDIR}${/}stdout.txt 	stderr=${TEMPDIR}${/}stderr.txt
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}   2 
