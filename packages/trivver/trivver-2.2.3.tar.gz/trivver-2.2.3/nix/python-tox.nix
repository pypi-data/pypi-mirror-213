# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

{ pkgs ? import <nixpkgs> {}, py-ver ? 311 }:
let
  python-name = "python${toString py-ver}";
  python = builtins.getAttr python-name pkgs;
  python-pkgs = python.withPackages (p: with p; [ tox ]);
in pkgs.mkShell {
  buildInputs = [
    pkgs.createrepo_c
    python-pkgs
  ];
  shellHook = ''
    set -e
    env TEST_CARGO_INDEX_PATH= tox run-parallel
    exit
  '';
}
