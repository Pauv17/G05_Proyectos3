import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/pauv17/proyectos3/install/g05_prii3_move_jetbot'
