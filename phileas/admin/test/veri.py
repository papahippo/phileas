#!/usr/bin/python3
# -*- encoding: utf8 -*-
from phileas.admin import *


if __name__ == "__main__":
    mailGroup = MailGroup('Musicians')
    lid = Lid(name='test', mailGroups='badgroup')
    print(lid)
