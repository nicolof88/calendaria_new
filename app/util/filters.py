def nth(n):
	n = int(n)
	if (n==1):
		return str(n) + "st"
	elif (n==2):
		return str(n) + "nd"
	elif (n==3):
		return str(n) + "rd"
	else:
		return str(n) + "th"