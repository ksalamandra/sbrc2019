# Machine-learning-study
Meu estudo de machine learning
-------------------------------------

SETUP Mininet + Ryu (foi como consegui a melhor performance)

 - Ryu no ubuntu do windows (python 3)
 
    % pip3 install ryu
 
 - VM no virtual box com mininet (python 2)
 
    %  VM pronta no site do mininet
 
Roda o ryu (Ubuntu no windows) com:
 
    %  ryu-manager app/gui_topology/gui_topology.py ryu_test.py --observe-links
    
E a topologia do mininet (VM) com: 

    %  sudo mn --custom paper_topo.py --topo papertopo --controller remote,ip=<IP do hospedeiro>
