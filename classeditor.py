# -*- coding: utf-8 -*-
"""
Class editing program
"""

import re
from File import File
from datetime import datetime, timedelta, date, time

file = File("stor.txt")

month_set = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05",
             "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10",
             "Nov": "11", "Dec": "12"}

default_add = timedelta(hours=3)
day = str(date.today() + timedelta(1 if time(21, 30) <= datetime.now().time() else 0))

reg_url = re.compile(r"https://\w*\.?(zoom\.us|google\.com)(/?[a-zA-Z0-9?=-]*)*")
reg_time = re.compile(r"(\d{1,2}\s?:\s?\d{1,2})\s?(AM|PM)?\s?((to|-)\s?(\d{1,2}\s?:\s?\d{1,2})\s?(AM|PM)?)?", re.I)
# group 1,2,5,6
reg_date = re.compile(r"(\w{3})[\s,.-/\\]\s?(\d{1,2})[\s,.-/\\]\s?(\d{4})")
# group 1,2,3


def appender(func):  # decorator for adding to file
    def funcer(*inpu):
        def writer(*args):
            if args:
                for i in args:
                    file.append(i)
            return args
        ret_val = writer(*(func(*inpu)))
        return ret_val
    return funcer


def con_time(time_tup):  # time formatting for iso format
    i, j = map(str, time_tup)
    isp = i.strip().split(":", 1)
    if j.strip().lower() == "pm" and isp[0] != "12":
        return f"{int(isp[0].strip())+12}:{isp[1].strip()}"
    elif j.strip().lower() == "am" and isp[0] == "12":
        return f"00:{isp[1].strip()}"
    else:
        return f"{'0' if len(isp[0].strip())==1 else ''}{i.strip()}"


def con_date(mth, dt, yr):  # date formatting for iso format
    return f"{yr.strip()}-{month_set[mth.strip()]}-{'0'*(len(dt)%2)}{dt.strip()}"


@appender
def adlec_auto(*inpu):  # finding links of a kind from a text
    inp = inpu[0]

    urls = [i for i in reg_url.finditer(inp)]  # urls-iterator objects

    if reg_time.search(inp).start() < urls[0].start():  # split the text
        tsplit = [inp[: urls[0].end()]]
        for i in range(1, len(urls)):
            tsplit.append(inp[urls[i-1].end(): urls[i].end()])
    elif reg_time.search(inp[urls[-1].end():]):
        tsplit = [inp[urls[-1].start():]]
        for i in range(1, len(urls)):
            tsplit.append(inp[urls[i-1].start(): urls[i].start()])
        tsplit = tsplit[1:] + tsplit[:1]
    else:
        return ()

    for ind in range(len(urls)):
        text = tsplit[ind]

        re_tm = list(reg_time.finditer(text))[0]
        t1 = con_time((re_tm.group(1), re_tm.group(2)))
        if not re_tm.group(3):
            t2 = str((datetime.combine(date.min, time.fromisoformat(t1)) + default_add).time())
        else:
            t2 = con_time((re_tm.group(5), re_tm.group(6)))

        if re_dt := list(reg_date.finditer(text)):
            dt = con_date(re_dt[0].group(1), re_dt[0].group(2), re_dt[0].group(3))
        else:
            dt = day

        yield {"from": f"{dt} {t1}", "to": f"{dt} {t2}", "url": urls[ind].group(0)}


@appender
def adlec_man(*inpu):  # add a lecture from manually entered time and link
    fro, to, url = inpu
    reg = re.compile(r"(AM|PM)", re.I)
    frod = reg.findall(fro)
    if frod:
        fro = con_time((fro[:fro.find(frod[0])], frod[0]))
    else:
        fro = fro.strip()
    tod = reg.findall(to)
    if tod:
        to = con_time((to[:to.find(tod[0])], tod[0]))
    else:
        to = to.strip()
    return [{"from": f"{day} {fro}", "to": f"{day} {to}", "url": url.strip()}]


if __name__ == "__main__":
    fun = 0 if input("add manual? ") == "y" else 1
    while str(input("Want to add lecture?('y'/'n'): ")) == "y":
        if fun:
            adlec_auto(input(">>>"))
        else:
            adlec_man(input("from time?: "), input("to time?: "), input("link?: "))
