loadHomePage()
Get number of pages

Loop "1-N"
	LoadPage("http://www.ygdy8.net/html/gndy/dyzz/list_23_N.html")
	print("Page N/M")
	GetList()
	LoopContext()
		getDate
		writeCsv
	End
End