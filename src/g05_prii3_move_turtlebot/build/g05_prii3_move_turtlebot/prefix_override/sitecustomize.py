import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/pauv17/proyectos3/src/g05_prii3_move_turtlebot/install/g05_prii3_move_turtlebot'
