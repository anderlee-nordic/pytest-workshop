{
  description = "pytest workshop July 2026";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = f:
        nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in {
      devShells = forAllSystems (pkgs:
        let
          pythonPkgs = ps: with ps; [
            pytest
            pytest-asyncio
            pytest-mock
            pytest-html
            pytest-cov
            time-machine
          ];
          pythonEnv = pkgs.python3.withPackages pythonPkgs;
          pyNames = map (p: p.pname or p.name) (pythonPkgs pkgs.python3.pkgs);
        in {
          default = pkgs.mkShell {
            packages = [ pythonEnv ];
            shellHook = ''
              export PS1="(nix) $PS1"
              echo "Python packages:"
              ${pkgs.lib.concatMapStringsSep "\n" (n: ''echo "  - ${n}"'') pyNames}
              echo -e "\e[1;33mWelcome to nix shell\e[0m"
            '';
          };
        });
    };
}
