# Machine-learning-study
## Meu estudo de machine learning
-------------------------------------

SETUP Mininet + Ryu (foi como consegui a melhor performance)

 Ryu no ubuntu do windows (python 3)
 
    % pip3 install ryu
 
 VM no virtual box com mininet (python 2)
 
    %  VM pronta no site do mininet
    
-------------------------------------
 
Roda o ryu (Ubuntu no windows) com:
 
    ````  sudo ryu-manager app/gui_topology/gui_topology.py throttling.py --observe-links
    
E a topologia do mininet (VM) com: 

    %  sudo python mininet_topology.py