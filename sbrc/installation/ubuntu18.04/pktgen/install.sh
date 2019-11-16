sudo apt-get install -y wget patch libpcap-dev make curl
curl -LO http://www.dpdk.org/browse/apps/pktgen-dpdk/snapshot/pktgen-3.5.0.tar.gz
tar xvfz pktgen-3.5.0.tar.gz
echo "export RTE_SDK=\$DPDK_DIR" >> ~/.bashrc
echo "export RTE_TARGET=\$DPDK_TARGET" >> ~/.bashrc
. ~/.bashrc
cd pktgen-3.5.0
make