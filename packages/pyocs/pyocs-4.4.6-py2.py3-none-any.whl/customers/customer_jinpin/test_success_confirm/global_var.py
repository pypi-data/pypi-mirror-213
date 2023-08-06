# -*- coding: utf-8 -*-

def _init():
    global recive_new_email_flag
    recive_new_email_flag = False
def get_recive_new_email_flag():
    global recive_new_email_flag
    return recive_new_email_flag
def set_recive_new_email_flag(get_status):
    global recive_new_email_flag
    recive_new_email_flag = get_status