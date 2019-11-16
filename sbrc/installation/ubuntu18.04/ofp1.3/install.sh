# install 

sudo apt-get install -y cmake make libpcap-dev libxerces-c3.2 libxerces-c-dev libpcre3 libpcre3-dev flex bison pkg-config autoconf libtool libboost-dev
git clone https://github.com/netgroup-polito/netbee.git
cd netbee/src
cmake .
make
cp ../bin/libn*.so /usr/local/lib
ldconfig
cp -R ../include/* /usr/include/
./boot.sh
./configure
make
make install