{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
        system = "aarch64-darwin";
        pkgs = nixpkgs.legacyPackages.${system};
        pypkgs = pkgs.python3Packages;
    in
    {
      packages.${system}.default = pypkgs.buildPythonPackage {
        pname = "lib50";
        version = "3.0.11";
        src = pkgs.fetchFromGitHub {
            owner = "peperronii";
            repo = "lib50";
            rev = "main";
            hash = "sha256-OzETG0uPv5wc3hYzHAtdzkc5DXFLcoEqdZxRW4qxblk=";
        };
      };
    };
}
