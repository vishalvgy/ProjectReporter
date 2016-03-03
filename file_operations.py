import os
import mimetypes
import subprocess

def is_hidden(path):
    try:
        if path and path.split("/")[-1].startswith("."):
            return True
    except Exception, ex:
        print "Exception in is_hidden() :",ex

    return False


def is_text_file(file_path):
    try:
        type_ = mimetypes.guess_type(file_path)[0]
        if type_ and type_.lower().startswith("text"):
            return True

    except Exception, ex:
        print "Exception in is_text_file :",ex

    return False


def count_text_lines(stream):
    try:
        cmd = ["wc","-l"]
        p = subprocess.Popen(cmd,stdin=stream,stdout=subprocess.PIPE)
        lines = 0
        while True:
            out = p.stdout.readline()
            if not out:
                break

            if int(out.split()[0]) > lines:
                lines = int(out.split()[0])
    except Exception, ex:
        print "Exception in count_text_lines() :",ex

    return lines


def get_lines_in_a_file(file_path):
    try:
        cmd = ["wc","-l",file_path]
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
        lines = 0
        while True:
            out = p.stdout.readline()
            if not out:
                break

            if int(out.split()[0]) > lines:
                lines = int(out.split()[0])
    except Exception, ex:
        print "Exception get_lines_in_a_file() :%s",ex

    return lines

