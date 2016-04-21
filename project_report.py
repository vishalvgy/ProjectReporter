#!/usr/bin/python -u

#This program is takes path of a git project and ouputs a json containing every author's contribution to each 
#text file in the project(in percentage).

#Author :    Vishal 
#Date   :    1st March 2016
#Karthavya Technologies Pvt. Ltd.

import sys
import os

from git_operations import *


if __name__ == '__main__':

    if len(sys.argv) < 2:
       sys.exit("USAGE: ./poject_report.py <Project Path>")

    project = sys.argv[1]
    if not os.path.exists(project):
        sys.exit("Project <%s> does not exists..!!"%project)

    print "Report:",get_project_contribution_report(project)
