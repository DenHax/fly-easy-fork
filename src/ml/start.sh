#!/bin/bash

_base="$(dirname "$0")"
_base="$(realpath "$_base")"

main() {
  python "$_base/server.py"
}

main
