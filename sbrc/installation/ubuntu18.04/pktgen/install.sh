# Install dependencies
sudo apt-get update
sudo apt-get install git build-essential linux-headers-`uname -r`

# Get code
git clone http://dpdk.org/git/dpdk

# numa
apt-get install libnuma-dev

# Build code
cd dpdk
make config T=x86_64-native-linuxapp-gcc
make

# Install kernel modules
sudo modprobe uio
sudo insmod build/kmod/igb_uio.ko

# Configure hugepages
echo 1024 | sudo tee /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
sudo mkdir /mnt/huge
sudo mount -t hugetlbfs nodev /mnt/huge

# Bind secondary network adaptor
sudo ifconfig eth1 down
sudo ./tools/pci_unbind.py --bind=igb_uio eth1

# I needed to do this to make the examples compile, not sure why.
export RTE_SDK=/root/dpdk
ln -s $RTE_SDK/build $RTE_SDK/x86_64-default-linuxapp-gcc

# Go wild! You have a low-latency user-space network stack!

sudo apt-get install -y wget patch libpcap-dev make curl
curl -LO http://www.dpdk.org/browse/apps/pktgen-dpdk/snapshot/pktgen-3.5.0.tar.gz
tar xvfz pktgen-3.5.0.tar.gz
echo "export RTE_SDK=\$DPDK_DIR" >> ~/.bashrc
echo "export RTE_TARGET=\$DPDK_TARGET" >> ~/.bashrc
. ~/.bashrc
cd pktgen-3.5.0
make