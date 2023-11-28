import logging

def create_logger():
    #basic logging config
    fmtstr = " %(asctime)s: (%(filename)s): %(levelname)s: %(funcName)s Line: %(lineno)d - %(message)s"
    datestr = "%d/%m/%Y %H:%M:%S"
    logging.basicConfig(
        filename="log_ebayka.log",
        level=logging.DEBUG,
        filemode="a",
        format=fmtstr,
        datefmt=datestr,
    )