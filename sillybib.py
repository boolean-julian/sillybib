import sys

input_filename = ""
try:
	input_filename = sys.argv[1]
except:
	print("Usage: python3 sillybib.py /path/to/bibliography.bib")
	exit()

def split_at_last_occurence(string, char):
	ilast = len(string)-1
	while ilast >= 0 and string[ilast] != char:
		ilast -= 1

	return string[:ilast], string[ilast+1:]

prefix, suffix = split_at_last_occurence(input_filename, ".")
output_filename = f"{prefix}-filtered.{suffix}"

def get_substring_between_chars(string, cfirst, clast):
	ifirst = 0
	while ifirst < len(string) and string[ifirst] != cfirst:
		ifirst += 1

	ilast = len(string)-1
	while ilast >= 0 and string[ilast] != clast:
		ilast -= 1

	return string[ifirst+1:ilast]

def replace_line(string):
	# Filter out names
	authors = get_substring_between_chars(string, "{", "}")
	names = authors.split(" and ")

	# Modify first names
	for i in range(len(names)):
		current_names = names[i].split(", ")

		current_lastname = ''.join(c for c in current_names[0] if c != "{" and c != "}")
		current_firstnames = current_names[1:]
		
		names[i] = current_lastname
		if len(current_firstnames) > 0:
			names[i] = names[i] + ", "
		for j in range(len(current_firstnames)):
			current_firstnames[j] = ''.join(c + ". " for c in current_firstnames[j] if c.isupper())
			names[i] += current_firstnames[j]

	# Add " and " between names
	result = ""
	for i in range(len(names)):
		result += names[i]
		if i < len(names)-1:
			result += "and "
	
	# Add line prefix and suffix
	line_prefix = "\tauthor = {"
	line_suffix = "},\n"
	result = line_prefix + result + line_suffix
	
	return result

input_file = open(input_filename, encoding="utf-8")
lines = input_file.readlines()
for i in range(len(lines)):
	if "author = " in lines[i]:
		lines[i] = replace_line(lines[i])
input_file.close()

output_file = open(output_filename, "w", encoding="utf-8")
for line in lines:
	output_file.write(line)
output_file.close()