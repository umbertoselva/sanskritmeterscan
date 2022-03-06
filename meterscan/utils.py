from meterscan import app

# CUSTOM FUNCTIONS
# 1) meterscanner()
# 2) allowed_ext()
# 3) allowed_filesize()
# 4) vedic_meterscanner()

def meterscanner(pada, target):
	"""
	1) This is the function that scans the meter
	Arguments: 
		pada = the line of text
		target = the file to write to
	"""

	# add a line to remove signs within the text (*, +, and the avagraha ')
	pada = pada.replace('*','')
	pada = pada.replace('+','')
	pada = pada.replace('\'','')
	pada = pada.replace('  ',' ')

	# adapt Vedic characters (withc accents and underneath-placed circles)
	pada = pada.replace('ḷh','ḍh')
	pada = pada.replace('l̥','ḷ').replace('l̥̄','ḹ').replace('ĺ̥','ḷ').replace('l̥̀','ḷ')
	pada = pada.replace('r̥','ṛ').replace('r̥̄','ṝ').replace('ŕ̥','ṛ').replace('r̥̀','ṛ').replace('r̥̄́','ṝ')
	pada = pada.replace('ā̀','ā').replace('ā́','ā')
	pada = pada.replace('ī́','ī').replace('ī̀','ī')
	pada = pada.replace('ū́','ū').replace('ū̀','ū')
	# adapt other single-glyph long vowels
	pada = pada.replace('è','e').replace('é','e')
	pada = pada.replace('ò','o').replace('ó','o')
	pada = pada.replace('à','a').replace('á','a')
	pada = pada.replace('ì','i').replace('í','i')
	pada = pada.replace('ù','u').replace('ú','u')
	# Remove all two-glyph characters first.
	pada = pada.replace('ā3','ā').replace('ī3','ī').replace('ū3','ū').replace('ṝ3','ṝ').replace('ḹ3','ḹ')
	pada = pada.replace('ṝ','H').replace('ḹ','H')
	pada = pada.replace('ai','H').replace('au','H')	
	pada = pada.replace('kh','C').replace('gh','C')
	pada = pada.replace('ch','C').replace('jh','C')
	pada = pada.replace('ṭh','C').replace('ḍh','C')
	pada = pada.replace('th','C').replace('dh','C')
	pada = pada.replace('ph','C').replace('bh','C')
	# Replace remaining consonant classes (single-glyph characters).
	pada = pada.replace('k','C').replace('g','C').replace('ṅ','C')
	pada = pada.replace('c','C').replace('j','C').replace('ñ','C')
	pada = pada.replace('ṭ','C').replace('ḍ','C').replace('ṇ','C')
	pada = pada.replace('t','C').replace('d','C').replace('n','C')
	pada = pada.replace('p','C').replace('b','C').replace('m','C')
	pada = pada.replace('y','C').replace('r','C').replace('l','C').replace('v','C').replace('ẏ','C')
	pada = pada.replace('ś','C').replace('ṣ','C').replace('s','C').replace('h','C')
	pada = pada.replace('ṃ','C').replace('m̆̇','C').replace('ṁ','C').replace('m̥','C')
	pada = pada.replace('ḥ','C').replace('ḫ','C')
	# Mark L vowels.
	pada = pada.replace('a','L').replace('i','L').replace('u','L')
	pada = pada.replace('ṛ','L').replace('ḷ','L')
	# Mark H vowels.
	pada = pada.replace('ā','H').replace('ī','H').replace('ū','H').replace('e','H').replace('o','H').replace('ṝ','H').replace('ḹ','H')
	# Scan heaviness by position.
	pada = pada.replace('LCC', 'H').replace('L CC', 'H ').replace('LC C', 'H ')
	# Remove C's that don't contribute to scansion.
	pada = pada.replace('C','')

	# Remove trailing characters
	pada = pada.rstrip('\'/_-:.|{} 0123456789')
	# pada = pada.replace('H','h').replace('L','l')
	# pada = pada = ''.join(ch for ch in pada if not ch.isupper())
	# s/ s// s| s||

	# remove spaces
	pada = pada.replace(" ","")

	# remove remaining trailing characters
	for character in pada:
		if not character.isupper():
			pada = pada.split(f'{character}', 1)[0]
			break
	
	# write line to file
	for character in pada:
		target.write(character)
	
	# add trailing newline at the end of the line
	target.write("\n")


def allowed_ext(filename):
	"""
	2) This is the function to check the filename
	"""

	# we only want files with a . in the filename, so that we can split the ext
	if not "." in filename:
		return False

	# split the extension from the filename, select the ext (i.e. [1]) and store it
	ext = filename.rsplit(".", 1)[1]

	# check if the ext is in the ALLOWED_EXT list
	if ext.upper() in app.config["ALLOWED_EXT"]:
		return True
	else:
		return False


def allowed_filesize(filesize):
	"""
	3) this is the function to check the filesize
	"""

	if int(filesize) <= app.config["MAX_FILESIZE"]:
		return True
	else:
		return False


def vedic_meterscanner(pada, target):
	"""
	4) Same as function (1) but adapted for scanning Vedic meter
	Arguments: 
		pada = the line of text
		target = the file to write to
	"""

	# add a line to remove signs within the text (*, +, and the avagraha ') and double spaces
	pada = pada.replace('*','')
	pada = pada.replace('+','')
	pada = pada.replace('\'','')
	pada = pada.replace('  ',' ')

	# adapt Vedic characters (withc accents and underneath-placed circles)
	pada = pada.replace('ḷh','ḍh')
	pada = pada.replace('ĺ̥','ḷ').replace('l̥̀','ḷ').replace('l̥','ḷ').replace('l̥̄','ḹ')
	pada = pada.replace('r̥̄́','ṝ').replace('r̥̄','ṝ').replace('ŕ̥','ṛ').replace('r̥̀','ṛ').replace('r̥','ṛ')
	pada = pada.replace('ā̀','ā').replace('ā́','ā')
	pada = pada.replace('ī́','ī').replace('ī̀','ī')
	pada = pada.replace('ū́','ū').replace('ū̀','ū')
	# adapt other single-glyph long vowels
	pada = pada.replace('è','e').replace('é','e')
	pada = pada.replace('ò','o').replace('ó','o')
	pada = pada.replace('ái','ai').replace('ài','ai').replace('aí','ai').replace('aì','ai')
	pada = pada.replace('áu','au').replace('àu','au').replace('aú','au').replace('aù','au')
	pada = pada.replace('à','a').replace('á','a')
	pada = pada.replace('ì','i').replace('í','i')
	pada = pada.replace('ù','u').replace('ú','u')
	# Remove all two-glyph characters first.
	pada = pada.replace('ā3','ā').replace('ī3','ī').replace('ū3','ū').replace('ṝ3','ṝ').replace('ḹ3','ḹ')
	pada = pada.replace('ai','W').replace('au','W')
	pada = pada.replace('kh','C').replace('gh','C')
	pada = pada.replace('cch','ch').replace('ch','CC').replace('jh','C') # N.B. ch=cch
	pada = pada.replace('ṭh','C').replace('ḍh','C')
	pada = pada.replace('th','C').replace('dh','C')
	pada = pada.replace('ph','C').replace('bh','C')

	# replace long vowels with W, short with V
	pada = pada.replace('ṝ','W').replace('ḹ','W')
	pada = pada.replace('ā','W')
	pada = pada.replace('ī','W')
	pada = pada.replace('ū','W')
	pada = pada.replace('e','W')
	pada = pada.replace('o','W')
	pada = pada.replace('ṛ','V').replace('ḷ','V')
	pada = pada.replace('a','V')
	pada = pada.replace('i','V')
	pada = pada.replace('u','V')

	# vocalis ante vocalem corripitur
	pada = pada.replace('WV','VV').replace('W V','V V')

	# mark short vowels V as L, long vowels W as H
	pada = pada.replace('V','L').replace('W','H')

	# Replace remaining consonant classes (single-glyph characters).
	pada = pada.replace('k','C').replace('g','C').replace('ṅ','C')
	pada = pada.replace('c','C').replace('j','C').replace('ñ','C')
	pada = pada.replace('ṭ','C').replace('ḍ','C').replace('ṇ','C')
	pada = pada.replace('t','C').replace('d','C').replace('n','C')
	pada = pada.replace('p','C').replace('b','C').replace('m','C')
	pada = pada.replace('y','C').replace('r','C').replace('l','C').replace('v','C').replace('ẏ','C')
	pada = pada.replace('ś','C').replace('ṣ','C').replace('s','C').replace('h','C')
	pada = pada.replace('ṃ','C').replace('m̆̇','C').replace('ṁ','C').replace('m̥','C')
	pada = pada.replace('ḥ','C').replace('ḫ','C')
	
	# Scan heaviness by position.
	pada = pada.replace('LCC', 'H').replace('L CC', 'H ').replace('LC C', 'H ')
	
	# Remove C's that don't contribute to scansion.
	pada = pada.replace('C','')

	# Remove trailing characters
	pada = pada.rstrip('\'/_-:.*|{} 0123456789')

	# # remove spaces
	# pada = pada.replace(" ","")

	# remove remaining trailing characters
	for character in pada:
		if not character.isupper() and not character == ' ':
			pada = pada.split(f'{character}', 1)[0]
			break
	
	#count the syllables (i.e. the num of Hs + Ls - whitespaces)
	syllable_counter = pada
	# remove all whitespaces in pada_2
	syllable_counter = syllable_counter.replace(" ","")
	# put caesura if (presumably) Tristubh or Jagati
	if len(syllable_counter) == 11 or len(syllable_counter) == 12:
	
		# Set syllable counter.
		a = 0
		# insert caesura
		for i in pada:				# For each unit in the sequence,
			if i != " ":			# if the slot has a vowel (i.e., isn't a space),
				a = a+1			# count it up.
				target.write(i)		# (Print to keep track.)
			elif a == 4 and i == " ":	# If there's a word boundary (i.e., a space) after 4 vowels,
				target.write("|")	# print a caesura.
			elif a == 5 and i == " ":	# (Word boundary after 5 vowels.)
				target.write("|")	# print a caesura.
		target.write("\n")			# add final newline.

	else:
		#remove spaces
		pada = pada.replace(" ","")
		# write to file
		for i in pada:
			target.write(i)
		# add final newline
		target.write("\n")