{ pkgs }: {
  deps = [
    pkgs.python312
    pkgs.nodejs_20
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
    PYTHONPATH = "/home/runner/workspace:/home/runner/workspace/backend";
  };
}