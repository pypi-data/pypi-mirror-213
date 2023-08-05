import logging
from logging.handlers import TimedRotatingFileHandler


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s ')
servers_log_hand = TimedRotatingFileHandler('log/server.log', when='w0')
servers_log_hand.setFormatter(formatter)


servers_log = logging.getLogger('server_1')
servers_log.setLevel(logging.INFO)
servers_log.addHandler(servers_log_hand)

formatter_1 = logging.Formatter('%(asctime)s -  %(message)s ')
servers_log_new_hand = logging.FileHandler('log/server.log')
servers_log_new_hand.setFormatter(formatter_1)
servers_log_new = logging.getLogger('server_1')
servers_log_new.setLevel(logging.INFO)
servers_log_new.addHandler(servers_log_new_hand)