def iter(f,n):
	while True:
		n = f(n)
		yield n
