#!/usr/bin/python


import os,sys
import urllib2


def get_md_names(url, all_md=list()):
    """
    **Recursively** traverses the metadata hierarchy and returns a list of each metadata
    with values

    :param url: the metadat url, should always be http://169.254.169.254/latest/meta-data/
    :param all_md: current metadata list
    :return:  list(all_md)
    """

    md = (urllib2.urlopen(url).read()).split()

    for m in md:
        m = m.rstrip()
        if not m.endswith("/"):
            if (url + m) not in all_md:
                all_md.append(url + m)
        else:
            r_url = url + m
            get_md_names(r_url, all_md)

    return(all_md)

def main():

    rc = 0

    # not including these
    no_include = ["iam/security-credentials", "iam/info"]
    md = list()

    for url in get_md_names("http://169.254.169.254/latest/meta-data/"):
        if not any(x in url for x in no_include):
            try:
                md = (urllib2.urlopen(url).read()).split()
            except urllib2.HTTPError:
                pass
            except:
                e = sys.exc_info()[0]
                print "General Exception: %s" % e

            s_url = url.replace("http://169.254.169.254/latest/meta-data/", "")

            if "public-keys/" in s_url:
                md = list()
                (s_url,keys) = s_url.split("/")
                md.append(keys)
            print("{} =  {}".format(s_url.ljust(80), ", ".join(md)))

    return rc

if __name__ == "__main__":
    sys.exit(main())
    
