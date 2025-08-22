{ pkgs }: {
  deps = [
    pkgs.python313
    pkgs.nodejs-20_x
    pkgs.postgresql
    pkgs.redis
    pkgs.git
    pkgs.curl
    pkgs.vim
  ];
  
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
      pkgs.glib
      pkgs.cairo
      pkgs.gobject-introspection
    ];
    PYTHONPATH = "/home/runner/v0-botarmy-poc:/home/runner/v0-botarmy-poc/backend";
  };
}