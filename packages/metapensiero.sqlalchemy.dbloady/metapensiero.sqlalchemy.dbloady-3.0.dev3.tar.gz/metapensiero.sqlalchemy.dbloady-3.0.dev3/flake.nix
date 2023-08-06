# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady — Development environment
# :Created:   gio 30 giu 2022, 8:29:40
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2022, 2023 Lele Gaifax
#

{
  description = "metapensiero.sqlalchemy.dbloady";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
    gitignore = {
      url = "github:hercules-ci/gitignore.nix";
      # Use the same nixpkgs
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, gitignore }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        inherit (builtins) fromTOML getAttr listToAttrs map readFile replaceStrings splitVersion;
        pkgs = import nixpkgs { inherit system; };
        inherit (pkgs.lib) cartesianProductOfSets flip;
        inherit (gitignore.lib) gitignoreFilterWith;

        getSource = name: path: pkgs.lib.cleanSourceWith {
          name = name;
          src = path;
          filter = gitignoreFilterWith { basePath = path; };
        };

        # Python versions to test against, see also Makefile
        pyVersions = [
          "python310"
          "python311"
        ];

        # SQLAlchemy versions to try out
        saVersions = [
          { version = "1.4.48";
            sha256 = "b47bc287096d989a0838ce96f7d8e966914a24da877ed41a7531d44b55cdb8df"; }
          { version = "2.0.16";
            sha256 = "1e2caba78e7d1f5003e88817b7a1754d4e58f4a8f956dc423bf8e304c568ab09"; }
        ];

        py-sa-pairs = cartesianProductOfSets { pyv = pyVersions; sav = saVersions; };

        mkSAPkg = python: saVersion:
          python.pkgs.buildPythonPackage rec {
            pname = "SQLAlchemy";
            version = saVersion.version;
            src = python.pkgs.fetchPypi {
              inherit pname version;
              sha256 = saVersion.sha256;
            };
            doCheck = false;
            nativeBuildInputs = [ python.pkgs.cython ];
            propagatedBuildInputs = [
              python.pkgs.greenlet
              python.pkgs.typing-extensions
            ];
          };

        mkPkg = pyVersion: saVersion:
          let
            py = getAttr pyVersion pkgs;
            sqlalchemy' = mkSAPkg py saVersion;
            pinfo = (fromTOML (readFile ./pyproject.toml)).project;
          in
            py.pkgs.buildPythonPackage {
              pname = pinfo.name;
              version = pinfo.version;

              src = getSource "dbloady" ./.;
              format = "pyproject";

              nativeBuildInputs = with py.pkgs; [
                pdm-pep517
              ];

              propagatedBuildInputs = with py.pkgs; [
                progressbar2
                ruamel-yaml
                sqlalchemy'
              ];
            };

        # Concatenate just the major and minor version parts: "1.2.3" -> "12"
        mamiVersion = v:
          let
            inherit (builtins) splitVersion;
            inherit (pkgs.lib.lists) take;
            inherit (pkgs.lib.strings) concatStrings;
          in
            concatStrings (take 2 (splitVersion v));

        dbloadyPkgs = flip map py-sa-pairs
          (pair: {
            name = "dbloady-${mamiVersion pair.pyv}-sqlalchemy${mamiVersion pair.sav.version}";
            value = mkPkg pair.pyv pair.sav;
          });

        mkTestShell = pyVersion: saVersion:
         let
           py = getAttr pyVersion pkgs;
           pkg = mkPkg pyVersion saVersion;
           env = py.buildEnv.override {
             extraLibs = [
               pkg
               py.pkgs.psycopg2
             ];
           };
         in pkgs.mkShell {
           name = "Test Python ${py.version} SA ${saVersion.version}";
           packages = with pkgs; [
             env
             just
             postgresql_15
             sqlite
             yq-go
           ];

           shellHook = ''
             TOP_DIR=$(pwd)
             export PYTHONPATH="$TOP_DIR/src''${PYTHONPATH:+:}$PYTHONPATH"
             trap "$TOP_DIR/tests/postgresql stop" EXIT
           '';
         };

        testShells = flip map py-sa-pairs
          (pair: {
            name = "test-${mamiVersion pair.pyv}-sqlalchemy${mamiVersion pair.sav.version}";
            value = mkTestShell pair.pyv pair.sav;
          });
      in {
        devShells = {
          default = pkgs.mkShell {
            name = "Dev shell";

            packages = (with pkgs; [
              bump2version
              just
              python3
              twine
              yq-go
            ]) ++ (with pkgs.python3Packages; [
              build
            ]);

            shellHook = ''
               TOP_DIR=$(pwd)
               export PYTHONPATH="$TOP_DIR/src''${PYTHONPATH:+:}$PYTHONPATH"
               trap "$TOP_DIR/tests/postgresql stop" EXIT
             '';
          };
        } // (listToAttrs testShells);

        packages = listToAttrs dbloadyPkgs;
      });
}
