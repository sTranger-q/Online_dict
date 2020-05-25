import datetime

a = "[('attack', 'n.  ~ violent attempt to hurt, overcome or defeat sb/sth', datetime.datetime(2020, 5, 25, 14, 19, 6))]"
b = eval(a)
print(b)
print(b[0][2])
print(type(b[0][2]))
format_title = "{:^20}{:^15}\t{:^30}"
print(format_title.format("time", "word", "mean"))
for w in b:
    t = "%s" % w[2]
    print(format_title.format(t, w[0], w[1]))
