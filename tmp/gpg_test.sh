#!/usr/bin/env bash

time {
for i in {1..500}; do
    gpg --decrypt data.txt.gpg &> /dev/null
done
}
