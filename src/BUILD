load("@rules_cc//cc:defs.bzl", "cc_binary")
load("@rules_python//python:python.bzl", "py_library", "py_test")

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

py_library(
    name = "elements",
    srcs = [
        "elements.py",
    ],
    deps = [":nodes"]
)

py_test(
    name = "elements_test",
    srcs = ["elements_test.py"],
    deps = [":elements"],
    data = ["//examples/hw1:input_files"],
)

py_library(
    name = "nodes",
    srcs = [
        "nodes.py",
    ],
)

py_test(
    name = "nodes_test",
    srcs = ["nodes_test.py"],
    deps = [":nodes"],
    data = ["//examples/hw1:input_files"],
)