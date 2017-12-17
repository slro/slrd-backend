#!/usr/bin/env bash
#
##################################################################
# title:      run_tests.sh                                       #
# descrption: Run all unit tests in ./test folder                #
# usage:      run_tests.sh -h                                    #
# developer:  ddnomad                                            #
# version:    0.0.1                                              #
##################################################################

OPT_UT_OPTS='--'
OPT_UT_FILES='./test'
OPT_UT_MODE='discover'

readonly INFO_SCRIPT_PDIR="$(dirname "$0")"
readonly INFO_SCRIPT_NAME="$(basename "$0")"

readonly ERR_RUN_NDIRNAME='Error: script should be run from directory: '
readonly ERR_NPARAM='Error: missing required possitional parameter: '
readonly ERR_NFILE='Error: passed in test file do not exist: '
readonly ERR_UOPT='Error: unknown option: '
readonly MSG_SCRIPT_HELP="$(cat <<EOF
Usage: ./${INFO_SCRIPT_NAME} [OPTIONS]

Run unit tests from ./test directory. Without no parameters passed
test discovery is started that runs all tests (except for ones that
are skipped in test modules explicitly).

As for now there is no way to start a particular test but it will be
added in a future iterations of this script (as it will be needed).

NOTE: This script should be run from the directory it's located in.
      Attempts to run in from elsewhere will result in error and
      termination.

Options

    -h  --help          Print this message and exit
    -v  --verbose       Run unit tests in a verbose mode
    -m  --modules       Allows to specify what test modules to run

Examples

    ${INFO_SCRIPT_NAME}     # run unittest discovery
    ${INFO_SCRIPT_NAME} -v  # run unittest discovery in a verbose mode

    # run only test_module_1.py and test_module_2 from ./test/ directory
    ${INFO_SCRIPT_NAME} -m test/test_module_1.py test/test_module_2.py
EOF
)"


#########################################
# Enforce script is run from its dirname
#
# Arguments:
#   None
#
# Access:
#   None
#
# Return:
#   None
#
# Terminates:
#   Yes
#########################################
function enforce_run_dirname {
    if [[ ! "${INFO_SCRIPT_PDIR}" = '.' ]]; then
        echo "${ERR_RUN_NDIRNAME}$(pwd)${INFO_SCRIPT_PDIR#?}"
        exit 1
    fi
}


##############################################
# Resolve arguments and set runtime options
#
# Arguments:
#   $@ - input parameters of a parent script
#
# Access:
#   OPT_UT_OPTS  [modify]
#   OPT_UT_MODE  [modify]
#   OPT_UT_FILES [modify]
#
# Return:
#   None
#
# Terminates:
#   Yes
##############################################
function resolve_arguments {
    while true; do
        if [[ -z "$1" ]]; then
            return
        fi

        local opt
        opt="$1"

        case "${opt}" in
            -h | --help )
                echo "${MSG_SCRIPT_HELP}"
                exit 0
                ;;
            -v | --verbose )
                OPT_UT_OPTS='-v'
                ;;
            -m | --module )
                unset OPT_UT_MODE
                unset OPT_UT_FILES
                declare -g -a OPT_UT_FILES
                shift
                if [[ -z "$1" ]]; then
                    echo "${ERR_NPARAM}test module to run"
                    exit 1
                fi
                while [[ -n "$1" ]]; do
                    if [[ ! -f "$1" ]]; then
                        echo "${ERR_NFILE}$1"
                        exit 1
                    fi
                    OPT_UT_FILES+=("$1")
                    shift
                done
                ;;
            * )
                echo "${ERR_UOPT}$1"
                exit 1
        esac
        shift
    done
    readonly OPT_UT_OPTS
    readonly OPT_UT_FILES
    readonly OPT_UT_MODE
}


# === MAIN FLOW ===
enforce_run_dirname
resolve_arguments "$@"
python3 -B -m unittest ${OPT_UT_MODE} "${OPT_UT_OPTS}" "${OPT_UT_FILES[@]}"
