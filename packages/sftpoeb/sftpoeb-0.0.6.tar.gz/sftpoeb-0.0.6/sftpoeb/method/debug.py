import os, sys

def debug_row(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    error_type = exc_type
    error_file = fname
    error_line = exc_tb.tb_lineno
    error_message = e
    return exc_type, fname, exc_tb.tb_lineno, e