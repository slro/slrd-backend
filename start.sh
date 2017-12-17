#!/usr/bin/env bash
#
##################################################################
# title:      start.sh                                           #
# descrption: Start a development version of SLRD backend server #
# usage:      start.sh -h                                        #
# developer:  ddnomad                                            #
# version:    0.0.1                                              #
##################################################################

readonly COLOR_INFO='\e[36m'
readonly COLOR_CONFIRM='\e[32m'
readonly COLOR_ERROR='\e[31m'
readonly COLOR_RESET='\e[39m'

# TODO: add support for CLI options (-h etc.)

echo -e "${COLOR_INFO}[i] Running setup${COLOR_RESET}"
echo -e "${COLOR_INFO}[i] Starting Flask${COLOR_RESET}"
nocache python3 ./server.py
