with import <nixpkgs> {};

stdenv.mkDerivation rec {
  name = "beam-env";

  buildInputs = [
    (python3.withPackages (ps: with ps; [
       flask
    ]))
  ];
}
