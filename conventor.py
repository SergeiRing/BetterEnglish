import filemapper as fm
def convent(files):
	all_words = []
	for file in files:
		for line in fm.read(file):
			if '-' in line:
				index = line.index('-')
				english = line[:index:]
				russian = line[index+1::]
				a = {english:russian.replace('\n', '')}
				all_words.append(a)
	return all_words

