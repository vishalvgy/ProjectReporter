from __future__ import division

import os
import subprocess
import mimetypes

from file_operations import *

def get_all_authors_commits(git_repo,all_branches=False):
    try:
        os.chdir(git_repo)
        cmd = ["git", "shortlog","-s"]

        if all_branches:
            cmd.append("--all")

        project_commits = {}
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE)
        while True:
            try:
                line = p.stdout.readline()
                if not line:
                    break
                author_name = ''
                author_details = line.split()
                for name in author_details[1:]:
                    author_name += " " + name

                author_name = author_name.strip()
                project_commits[author_name] = author_details[0]
            except Exception, ex:
                print "Exception in get_all_authors_commits() while reading process output:",ex

    except Exception,ex:
        print "Exception in get_all_authors_commits() :",ex

    return project_commits
                                          

def get_authors_contribution_to_file(file_path,author):
    try:
        total_lines = 0
        author_lines = 0
        contribution = 0

        total_lines = get_lines_in_a_file(file_path)

        os.chdir(os.path.dirname(file_path))

        git_blame = ["git","blame",file_path]
        p2 = subprocess.Popen(git_blame,stdout=subprocess.PIPE)

        grep_author = ["grep",author]
        p3 = subprocess.Popen(grep_author,stdin=p2.stdout,stdout=subprocess.PIPE)

        author_lines = count_text_lines(p3.stdout)

        if  total_lines:
            contribution = (author_lines / total_lines ) * 100

    except Exception, ex:
        print "Exception in get_authors_contribution_to_file() :",ex

    return contribution


def get_all_authors_contribution_to_file(file_path,authors):
    try:
        file_contribution = {}

        git_blame = ["git","blame","--line-porcelain",file_path]
        grep_author = ["grep",""]
        sort = ["sort"]
        unique = ["uniq","-c"]

        total_lines = get_lines_in_a_file(file_path)

        if not total_lines:
            return {}

        for author in authors:
            grep_author[1] = author
            p1 = subprocess.Popen(git_blame,stdout=subprocess.PIPE)
            p2 = subprocess.Popen(grep_author,stdin=p1.stdout,stdout=subprocess.PIPE)
            p3 = subprocess.Popen(sort,stdin=p2.stdout,stdout=subprocess.PIPE)
            p4 = subprocess.Popen(unique,stdin=p3.stdout,stdout=subprocess.PIPE)

            while True:
                line = p4.stdout.readline()
                if not line:
                    break

                details = line.split()
                author_lines = int(details[0])

                if total_lines and author_lines:
                    contribution =  (author_lines / total_lines ) * 100
                    file_contribution[author] = (float(100) if (contribution >= 100 ) else contribution) 

    except Exception, ex:
        print "Exception in get_all_authors_contribution_to_file() :",ex

    return file_contribution



def get_project_contribution_report(project,all_branches=False,include_hidden=True):
    try:
        report = {}
        report["files"] = []
        all_authors = get_all_authors_commits(project,all_branches).keys()

        for root_dir, sub_dirs, files in os.walk(project):
            if root_dir.find(".git") != -1:
                continue
            if not include_hidden and is_hidden(root_dir):
                continue
               
            for file_ in files:
                if not include_hidden and is_hidden(file_):
                    continue
                file_path = root_dir + "/" + file_
                if not is_text_file(file_path):
                    continue
                file_contribution = get_all_authors_contribution_to_file(file_path,all_authors)
                if file_contribution :
                    report["files"].append(file_path)
                    report[file_path] = file_contribution
    except Exception, ex:
        print "Exception in get_project_contribution_report() :%s",ex

    return report
