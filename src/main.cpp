/*
bazel run //src:main -- \
  --displacements_file /home/alex/Desktop/classes/S2021/COE321K/code/examples/displacements.txt \
  --elements_file /home/alex/Desktop/classes/S2021/COE321K/code/examples/elements.txt \
  --forces_file /home/alex/Desktop/classes/S2021/COE321K/code/examples/forces.txt \
  --nodes_file /home/alex/Desktop/classes/S2021/COE321K/code/examples/nodes.txt
*/

#include <iostream>
#include <filesystem>
#include <fstream>

#include "absl/strings/substitute.h"
#include "absl/debugging/failure_signal_handler.h"
#include "Eigen/Dense"
#include "gflags/gflags.h"
#include "glog/logging.h"

DEFINE_string(displacements_file, "", "Displacements file.");
DEFINE_string(elements_file, "", "Elements file.");
DEFINE_string(forces_file, "", "Forces file.");
DEFINE_string(nodes_file, "", "Nodes file.");

namespace filesystem = std::filesystem;

int main(int argc, char* argv[])
{
  absl::FailureSignalHandlerOptions opts;
  absl::InstallFailureSignalHandler(opts);
  gflags::SetUsageMessage("Tile a directory of images.");
  gflags::ParseCommandLineFlags(&argc, &argv, true);
  google::InitGoogleLogging(argv[0]);

  FLAGS_alsologtostderr = true;
  FLAGS_colorlogtostderr = true;

  // Process input arguments.
  filesystem::path displacements_file = filesystem::path(FLAGS_displacements_file);
  filesystem::path elements_file = filesystem::path(FLAGS_elements_file);
  filesystem::path forces_file = filesystem::path(FLAGS_forces_file);
  filesystem::path nodes_file = filesystem::path(FLAGS_nodes_file);


  std::ifstream file(displacements_file);
  std::string str;
  std::string file_contents;
  while (std::getline(file, str))
  {
    file_contents += str;
    file_contents.push_back('\n');
  } 
  std::cout << file_contents << std::endl;
  /*
  Eigen::MatrixXd m(2,2);
  m(0,0) = 3;
  m(1,0) = 2.5;
  m(0,1) = -1;
  m(1,1) = m(1,0) + m(0,1);
  std::cout << m << std::endl;
  */
}