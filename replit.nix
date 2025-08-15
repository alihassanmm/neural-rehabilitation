{ pkgs }: {
  deps = [
    pkgs.python311Full
    pkgs.python311Packages.pip
    pkgs.python311Packages.setuptools
    pkgs.python311Packages.wheel
    pkgs.nodejs_20
    pkgs.npm
    pkgs.texlive.combined.scheme-full
    pkgs.poppler_utils
    pkgs.ghostscript
    pkgs.imagemagick
    pkgs.curl
    pkgs.wget
    pkgs.git
    pkgs.gcc
    pkgs.gnumake
    pkgs.pkg-config
    pkgs.cairo
    pkgs.pango
    pkgs.gdk-pixbuf
    pkgs.libffi
    pkgs.openssl
  ];
  
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
      pkgs.glib
      pkgs.cairo
      pkgs.pango
      pkgs.gdk-pixbuf
      pkgs.libffi
      pkgs.openssl
    ];
    PYTHONPATH = "/home/runner/ResumeRefiner/backend";
    FLASK_ENV = "production";
    FLASK_RUN_HOST = "0.0.0.0";
    FLASK_RUN_PORT = "5000";
  };
}

