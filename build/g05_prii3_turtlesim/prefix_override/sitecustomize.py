import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/pauv17/g05_prii3_ws/install/g05_prii3_turtlesim'
