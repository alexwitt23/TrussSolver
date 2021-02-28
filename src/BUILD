load("@rules_cc//cc:defs.bzl", "cc_binary")

cc_binary(
    name = "main",
    srcs = ["main.cpp"],
    deps = [
        "@eigen//:eigen3",
        "@com_github_gflags_gflags//:gflags",
        "@com_google_absl//absl/debugging:failure_signal_handler",
        "@com_google_absl//absl/strings:str_format",
        "@com_google_logging//:glog",
    ],
    visibility = ["//visibility:public"],
)