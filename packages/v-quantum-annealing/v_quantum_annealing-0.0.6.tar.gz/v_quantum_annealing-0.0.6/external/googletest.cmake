include(FetchContent)

message(CHECK_START "Fetching GoogleTest")
list(APPEND CMAKE_MESSAGE_INDENT "  ")

set(CMAKE_CXX_STANDARD 17)
set(FETCHCONTENT_QUIET OFF)

#### Google test ####
FetchContent_Declare(
    googletest
    GIT_REPOSITORY  https://github.com/google/googletest
    GIT_TAG         v1.13.0
    GIT_SHALLOW     TRUE
)

if(WIN32)
  set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
endif()

FetchContent_MakeAvailable(googletest)


#set gtest library
set(GTEST_INCLUDE_DIR ${gtest_SOURCE_DIR}/include)
set(GTEST_LIBRARY ${CMAKE_CURRENT_SOURCE_DIR}/lib/gtest.lib)
set(GTEST_MAIN_LIBRARY ${CMAKE_CURRENT_SOURCE_DIR}/lib/gtest_main.lib)

# message(STATUS "CMAKE_CURRENT_SOURCE_DIR = ${CMAKE_CURRENT_SOURCE_DIR}")
#end set gtest library

find_package(GTest)

# FetchContent_GetProperties(googletest)

# message(STATUS "gtest_SOURCE_DIR = ${gtest_SOURCE_DIR}")
# message(STATUS "gmock_SOURCE_DIR = ${gmock_SOURCE_DIR}")




list(POP_BACK CMAKE_MESSAGE_INDENT)
message(CHECK_PASS "fetched")
