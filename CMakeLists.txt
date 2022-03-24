# CMakeList.txt: centerlineLinux 的 CMake 项目，在此处包括源代码并定义
# 项目特定的逻辑。
#
cmake_minimum_required (VERSION 3.8)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED on)
project ("centerlineLinux")
find_package(CUDA  REQUIRED)
include_directories("${CUDA_INCLUDE_DIRS}")


add_library(MySharedLib SHARED CenterlineExtraction.cpp CenterlineExtraction.h CUDA_DeviceHelperFunctions.cuh CUDA_SubiterationKernels2D.cuh CUDA_ThinningKernelMultiBlock2D.cuh ExtractSegments.cpp ExtractSegments.h LibThinning2D.cu LibThinning2D.h Structs.h)
# 将源代码添加到此项目的可执行文件。
# add_executable (centerlineLinux "CenterlineExtraction.cpp" )

# TODO: 如有需要，请添加测试并安装目标。
# 添加cuda文件
project(CUDA_MAT_MUL LANGUAGES CXX CUDA)

