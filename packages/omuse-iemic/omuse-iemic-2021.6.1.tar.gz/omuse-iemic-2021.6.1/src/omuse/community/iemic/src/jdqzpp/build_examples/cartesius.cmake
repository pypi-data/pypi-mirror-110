rm -rf CMakeCache.txt CMakeFiles

cmake \
-D CMAKE_C_COMPILER:STRING="mpiicc" \
-D CMAKE_CXX_COMPILER:STRING="mpiicpc" \
-D CMAKE_Fortran_COMPILER:STRING="mpiifort" \
-D CMAKE_INSTALL_PREFIX:STRING="/home/emulder/local/" \
-D BUILD_SHARED_LIBS:STRING="off" \
../
