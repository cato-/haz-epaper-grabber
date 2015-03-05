#!/usr/bin/env python
# Madsack ePaper Grabber v2
# Download the E-Paper for HAZ (Hannoversche Allgemeine Zeitung) with
# an account
#
# "THE BEER-WARE LICENSE" (Revision 42):
# <hazepaper -at- robertweidlich -dot- de> wrote this file. As long as you
# retain this notice you can do whatever you want with this stuff. If we meet
# some day, and you think this stuff is worth it, you can buy me a beer in
# return.

import argparse
from datetime import datetime
import os.path
import re
import json
import sys

import mechanize

baseurl = "https://epaper.haz.de"


def mkdate(datestr):
    try:
        return datetime.strptime(datestr, '%d.%m.%Y')
    except ValueError:
        msg = datestr + ' is not a proper date string'
        raise argparse.ArgumentTypeError(msg)


def download_url(date, issue):
    # URL is assembled via Javascript in
    # http://epaper.haz.de/js/application-min201503031.js
    url = "{baseurl}/issuefiles/{datum}_{issue}/pdfs/{issue}{datum}_Gesamt.pdf"
    return url.format(baseurl=baseurl, issue=issue, datum=date.strftime("%Y%m%d"))


def file_name(date, issue):
    file_template = "{issue}-{datum}.pdf"
    file = file_template.format(issue=issue, datum=date.strftime("%y%m%d"))
    return os.path.join(args.dumpdir, file)


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument(
    '-u', '--username', type=str,
    help='Username used to login', dest="user", required=True)
parser.add_argument(
    '-p', '--password', type=str,
    help='Password used to login', dest="password", required=True)
parser.add_argument(
    '-i', '--issue', type=str, nargs='+', default="HAZ",
    help='Issue to download. Use -a for possible values. Default: HAZ',
    dest="issue")
parser.add_argument(
    '-d', '--dumpdir', type=str, default=".",
    help='Direction where downloaded pdfs will be saved', dest="dumpdir")
parser.add_argument(
    '-t', '--date', type=mkdate,
    default=datetime.now().strftime("%d.%m.%Y"),
    help='Date of the desired issue. Default: Today', dest="date")
parser.add_argument(
    '-a', '--list-papers', action='store_true', dest="listavailable",
    help='Print Newspapers available in your account and issues ' +
         'available for download and exit.')

args = parser.parse_args()

br = mechanize.Browser()

# Browser options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Want debugging messages?
# br.set_debug_http(True)
# br.set_debug_redirects(True)
# This outputs the pdf as well to the terminal
# br.set_debug_responses(True)

# Set User-Agent to something common
ua = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36"
br.addheaders = [('User-agent', ua)]

# Get login page
response1 = br.open(baseurl)

# Login
br.select_form("login")
br["username"] = args.user
br["password"] = args.password

response2 = br.submit()

# Extract CRFS Token
data = response2.get_data()
ctoken = re.search("ctoken=.([a-zA-Z0-9]+)", data)
if not ctoken:
    print "Error while logging in. Check username and password."
    sys.exit(1)
ctoken = ctoken.group(1)

br.addheaders = [('X-CRFS-Token', ctoken), ('User-agent', ua)]

# Get json with information about available newspapers and issues
response = br.open("http://epaper.haz.de/newspaper")
data = response.get_data()
data = json.loads(data)

if type(args.issue) != list:
    args.issue = [args.issue, ]

available_papers = {}
titles = {}
available_issues = []

# extract needed information from json
for paper in data["newspaper"]:
    id = paper["epaper_id"].split("_")[0]
    available_papers[id] = []
    titles[id] = paper["title"]
    for i in paper["issues"]:
        key = i["key"]
        date = datetime.strptime(key[len(id):], "%Y%m%d")
        available_papers[id].append(date.strftime("%d.%m.%Y"))
        if date == args.date and id in args.issue:
            available_issues.append(id)
            break

# print available newspapers and their issues if requested
if args.listavailable:
    for p, issues in available_papers.iteritems():
        print p, titles[p],
        for i in issues:
            print i,
        else:
            print
    sys.exit(0)

# Download requested and available issues
for issue in available_issues:
    try:
        br.retrieve(download_url(args.date, issue), file_name(args.date, issue))
    except mechanize.HTTPError as e:
        msg = "Could not get issue of {issue} for {date}: {code}"
        print msg.format(issue=issue, date=args.date, code=e.code)
