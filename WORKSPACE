workspace(name = "truss_solver")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "bazel_skylib",
    sha256 = "97e70364e9249702246c0e9444bccdc4b847bed1eb03c5a3ece4f83dfe6abc44",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-skylib/releases/download/1.0.2/bazel-skylib-1.0.2.tar.gz",
        "https://github.com/bazelbuild/bazel-skylib/releases/download/1.0.2/bazel-skylib-1.0.2.tar.gz",
    ],
)

http_archive(
    name = "com_google_absl",
    sha256 = "f41868f7a938605c92936230081175d1eae87f6ea2c248f41077c8f88316f111",
    strip_prefix = "abseil-cpp-20200225.2",
    urls = ["https://github.com/abseil/abseil-cpp/archive/20200225.2.tar.gz"],
)

http_archive(
    name = "com_google_logging",
    sha256 = "9e1b54eb2782f53cd8af107ecf08d2ab64b8d0dc2b7f5594472f3bd63ca85cdc",
    strip_prefix = "glog-0.4.0",
    urls = ["https://github.com/google/glog/archive/v0.4.0.zip"],
)

http_archive(
    name = "com_github_gflags_gflags",
    sha256 = "34af2f15cf7367513b352bdcd2493ab14ce43692d2dcd9dfc499492966c64dcf",
    strip_prefix = "gflags-2.2.2",
    urls = [
        "https://mirror.bazel.build/github.com/gflags/gflags/archive/v2.2.2.tar.gz",
        "https://github.com/gflags/gflags/archive/v2.2.2.tar.gz",
    ],
)

http_archive(
    name = "eigen",
    build_file = "//third_party:eigen.BUILD",
    sha256 = "d76992f1972e4ff270221c7ee8125610a8e02bb46708a7295ee646e99287083b",  # SHARED_EIGEN_SHA
    strip_prefix = "eigen-90ee821c563fa20db4d64d6991ddca256d5c52f2",
    urls = [
        "https://storage.googleapis.com/mirror.tensorflow.org/gitlab.com/libeigen/eigen/-/archive/90ee821c563fa20db4d64d6991ddca256d5c52f2/eigen-90ee821c563fa20db4d64d6991ddca256d5c52f2.tar.gz",
        "https://gitlab.com/libeigen/eigen/-/archive/90ee821c563fa20db4d64d6991ddca256d5c52f2/eigen-90ee821c563fa20db4d64d6991ddca256d5c52f2.tar.gz",
    ],
)

rules_python_version = "c8c79aae9aa1b61d199ad03d5fe06338febd0774" # Latest @ 2020-10-15

http_archive(
    name = "rules_python",
    sha256 = "5be9610a959772697f57ec66bb58c8132970686ed7fb0f1cf81b22ddf12f5368",
    strip_prefix = "rules_python-{}".format(rules_python_version),
    url = "https://github.com/bazelbuild/rules_python/archive/{}.zip".format(rules_python_version),
)