
def percentage_increase(old, new):

    if old == 0:
        return "0%"
    else:
        return "{:.0%}".format(float(new - old) / old)
