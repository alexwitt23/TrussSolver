load("@rules_cc//cc:defs.bzl", "cc_library")

licenses([
    "reciprocal",  # MPL2
    "notice",  # Portions BSD
])

exports_files(["LICENSE"])

cc_library(
    name = "eigen3",
    hdrs = glob(["**"]),
    visibility = ["//visibility:public"],
)