
def percentage_increase(old, new):
	"""
	Returns Percentage Increase given the old and new value
	"""
    if old == 0:
        return "0%"
    else:
        return "{:.0%}".format(float(new - old) / old)
