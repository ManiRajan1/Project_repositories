#!/bin/bash
echo ">> Running Perl tests..."
perl framework1.pl

echo ">> Running Robot Framework tests..."
export PYTHONPATH=$(pwd)/resources
robot tests/