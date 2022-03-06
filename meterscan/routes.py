# Flask imports
from flask import render_template, redirect, url_for, flash, request, session, send_file
from werkzeug.utils import secure_filename

# System imports
import time
import os

# App from __init__.py
from meterscan import app

# Custom functions
from meterscan.utils import meterscanner, allowed_ext, allowed_filesize, vedic_meterscanner


# ROUTES				functions				templates (< layout.html)

# 1) /sanskrit				home()					home.html
# 2) /about 				about() 				about.html
# 3) /scansion 				scansion()				scansion.html (lang='Sanskrit')
# 4) /download_file			download_file()		
# 5) /display_file			display_file()
# 6) /display_text			display_text()
# 7) /vedic 				vedic() 				vedic.html
# 8) /vedic_scansion			vedic_scansion()			scansion.html (lang='Vedic')
# 9) /download_vedic_file		download_vedic_file()
# 10)/display_vedic_file		display_vedic_file()
# 11)/display_vedic_text 		display_vedic_text()

# ERRORS
# 404 Page Not Found 								404.html
# 500 server error / FileNotFound error 					500.html


# ROUTES

#1) route to display the sanskrit forms (GET)
# it also process the upload form (POST) which leads to 3) the scansion page
# or if the user uses the textarea form (POST) leads to 6) display text
@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
@app.route("/sanskrit", methods=["GET", "POST"])
def home():

	# if the user visits the page, display the forms
	if request.method == "GET":
		return render_template("home.html", lang='Sanskrit')

	# if the user submits the first form (i.e. uploads a file)
	if request.method == 'POST':

		# check that a file has been submitted
		if not request.files:
			# Alert
			flash("Upload failed!", 'danger')
			return redirect('/sanskrit')

		# ensure the filesize is within the set limit
		print(request.cookies)
		if "filesize" in request.cookies:
			if not allowed_filesize(request.cookies["filesize"]):
				# here error message that file is too big
				flash("The file is too large. The limit is 2MB.", 'danger')
				# reload form
				return redirect('/sanskrit')

		# access the submtted file by the input name='file' in the form
		# and store it file in a variable in order to manipulate it with flask
		file = request.files['file']

		# ensure file has a filename
		if file.filename == "":
			# alert
			flash("The file has no filename.", 'danger')
			return redirect('/sanskrit')

		# ensure extension is allowed
		if not allowed_ext(file.filename):
			# alert
			flash("Extension not allowed. Only .txt files are allowed.", 'danger')
			return redirect('/sanskrit')

		# ensure filename is secure and store a secure filename
		ok_filename = secure_filename(file.filename)

		# save the file on server in the upload folder
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], ok_filename))

		# open the file
		with open(os.path.join(app.config['UPLOAD_FOLDER'], ok_filename), 'r') as text:

			# create the output filename as "original.txt" > "original" > "original_SCAN.txt"
			output_filename = ok_filename.rsplit(".", 1)[0] + "_SCAN.txt"

			# store the path in the session
			session["output_file_path"] = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
			###print(session["output_file_path"])

			# open destination file to write into
			with open(session["output_file_path"], 'w') as target:

				# get the status of the checkbox (if checked == on, if unckecked == None)
				remove_verse_num = request.form.get('checkbox')
				###print(remove_verse_num)

				# For each line,
				for line in text:
					# remove the trailing newline (if the final line doesn't have a newline, no problem)
					line = line.rstrip('\n')
					# and write the contents of the line (and newline).
					#print(line)
					target.write(line + '\n') # it's useful to do this here and not before, because if the final line has no newline, this will add it

					# if checkbox was ticked (== on) the user indicated that there is a verse number at the beginning. So remove it
					if remove_verse_num == "on":
						pada = line.split(" ", 1)[-1]
						#print(pada)
						# Optional: remove leading (and trailing whitespaces) that may have been left by split()
						###pada = pada.strip()
					else:
						pada = line

					###print(pada)

					# process the pada and write in the target file
					meterscanner(pada, target)

		# Alert
		flash("Scansion successful!", 'success')

		return redirect("/scansion")


# 2) route to the About page
@app.route("/about")
def about():

	return render_template("about.html", lang='Sanskrit', title='About')


# 3) route to the scansion page
# the user gets here by using the upload form in 1)
# and gets to choose between 4) downloading the file and 5) displaying the file in a new tab
@app.route("/scansion")
def scansion():

	return render_template("scansion.html", lang='Sanskrit', title='Scansion')


# 4) route from 3) scansion if the user chooses to download a file
@app.route("/download_file")
def download_file():

	try:
		# return the scansion as a downloadable attachment
		return send_file(session["output_file_path"], as_attachment=True, cache_timeout=0)
	except:
		return render_template('errors/500.html', lang='Sanskrit', title="Error"), 500


# 5) route from 3) scansion if the user chooses to display the file in a new tab
@app.route("/display_file")
def display_file():

	try:
		# return the scansion by displaying the content of the file in a new tab
		return send_file(session["output_file_path"], cache_timeout=0)
	except:
		return render_template('errors/500.html', lang='Sanskrit', title="Error"), 500


# 6) route from 1) if the user uses the textarea form to display scansion in new tab
@app.route("/display_text", methods=["POST"])
def display_text():

		# if the user submits the second form (textarea) with the SCAN button

		# get the text from the textarea
		current_text = request.form.get("textarea")
		###print(current_text)

		# use time,strftime to get the current time for new filenames
		current_time = time.strftime("%Y%m%d-%H%M%S")
		# store this current time in session so that it's valid for the current user's file only
		session["current_time_name"] = current_time
		###print(session["current_time_name"])

		# create path for new source file with current time as filename
		session["source_file_path_2"] = os.path.join(app.config['UPLOAD_FOLDER'], session["current_time_name"])

		# open this new file and write the textarea text into it (this creates the file) - then close the file
		source_file = open(session["source_file_path_2"], 'w')
		source_file.write(current_text)
		###print(source_file)
		source_file.close()

		# create path to target file (adding the .txt extension just in case we'll make this downloadable in the future)
		session["output_file_path_2"] = os.path.join(app.config['UPLOAD_FOLDER'], session["current_time_name"] + "_SCAN.txt")
		###print(session["output_file_path_2"])

		# open source file for use (reading mode)
		with open(session["source_file_path_2"], 'r') as text:

			# create target file by opening it in writing mode
			with open(session["output_file_path_2"], 'w') as target:

				# get the status of the checkbox2 (if checkd == on, if unckecked == None)
				remove_verse_num = request.form.get('checkbox2')
				###print(remove_verse_num)

				# For each line,
				for line in text:
					# remove the trailing newline (if the final line doesn't have a newline, no problem)
					line = line.rstrip('\n')
					# and write the contents of the line (and newline).
					###print(line)
					target.write(line + '\n') # it's useful to do this here and not before, because if the final line has no newline, this will add it

					# if checkbox was ticked (== on) the user indicated that there is a verse number at the beginning. So remove it
					if remove_verse_num == "on":
						pada = line.split(" ", 1)[-1]
						print(pada)
						# Optional: remove leading (and trailing whitespaces) that may have been left by split
						#pada = pada.strip()
					else:
						pada = line

					print(pada)

					# process the pada and write it in the target file
					meterscanner(pada, target)

		try:
			# return the scansion by displaying the content of the file in a new tab
			return send_file(session["output_file_path_2"], cache_timeout=0)
		except:
			return render_template('errors/500.html', lang='Sanskrit', title="Error"), 500



# Vedic

# 7) home page for Vedic with upload and textarea forms
# with GET displays the forms
# if the user uses the upload form (POST) it leads to 8) Vedic scansion page
# if the user uses the textarea form (POST) it leads to 11) the display text in new tab page
@app.route("/vedic", methods=["GET", "POST"])
def vedic():

	# if the user visits the page, display the forms
	if request.method == "GET":
		return render_template("vedic.html", lang='Vedic')

	# if the user submits the first form (i.e. uploads a file)
	if request.method == 'POST':

		# check that a file has been submitted
		if not request.files:
			# Alert
			flash("Upload failed!", 'danger')
			return render_template("vedic.html", lang='Vedic')

		# ensure the filesize is within the set limit
		print(request.cookies)
		if "filesize" in request.cookies:
			if not allowed_filesize(request.cookies["filesize"]):
				# here error message that file is too big
				flash("The file is too large. The limit is 2MB.", 'danger')
				# reload form
				# return render_template("vedic.html", lang='Vedic')
				return redirect("/vedic")

		# access the submtted file by the input name='file' in the form
		# and store it file in a variable in order to manipulate it with flask
		file = request.files['file2']

		# ensure file has a filename
		if file.filename == "":
			# alert
			flash("The file has no filename.", 'danger')
			# return render_template("vedic.html", lang='Vedic')
			return redirect("/vedic")

		# ensure extension is allowed
		if not allowed_ext(file.filename):
			# alert
			flash("Extension not allowed. Only .txt files are allowed.", 'danger')
			# return render_template("vedic.html", lang='Vedic')
			return redirect("/vedic")

		# ensure filename is secure and store a secure filename
		ok_filename = secure_filename(file.filename)

		# save the file on server in the upload folder
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], ok_filename))

		# open the file
		with open(os.path.join(app.config['UPLOAD_FOLDER'], ok_filename), 'r') as text:

			# create the output filename as "original.txt" > "original" > "original_SCAN.txt"
			output_filename = ok_filename.rsplit(".", 1)[0] + "_SCAN.txt"

			# store the path in the session
			session["output_file_path_3"] = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
			###print(session["output_file_path_3"])

			# open destination file to write into
			with open(session["output_file_path_3"], 'w') as target:

				# get the status of the checkbox (if checked == on, if unckecked == None)
				remove_verse_num = request.form.get('checkbox3')
				###print(remove_verse_num)

				# For each line,
				for line in text:
					# remove the trailing newline (if the final line doesn't have a newline, no problem)
					line = line.rstrip('\n')
					# and write the contents of the line (and newline).
					###print(line)
					target.write(line + '\n') # it's useful to do this here and not before, because if the final line has no newline, this will add it

					# if checkbox was ticked (== on) the user indicated that there is a verse number at the beginning. So remove it
					if remove_verse_num == "on":
						pada = line.split(" ", 1)[-1]
						print(pada)
						# Optional: remove leading (and trailing whitespaces) that may have been left by split()
						#pada = pada.strip()
					else:
						pada = line

					###print(pada)

					# process the pada and write in the target file
					vedic_meterscanner(pada, target)

		# Alert
		flash("Scansion successful!", 'success')

		return redirect("/vedic_scansion")


# 8) route from 7) Vedic upload form
# allows you to choose between 9) download file or 10) display file in new tab
@app.route("/vedic_scansion")
def vedic_scansion():

	return render_template("scansion.html", lang='Vedic', title="Scansion")


# 9) route from 8) scansion if user chooses to download file
@app.route("/download_vedic_file")
def download_vedic_file():

	try:
		# return the scansion as a downloadable attachment
		return send_file(session["output_file_path_3"], as_attachment=True, cache_timeout=0)
	except:
		return render_template('errors/500.html', lang='Vedic', title="Error"), 500


# 10) route from 8) scansion if user chooses to display file
@app.route("/display_vedic_file")
def display_vedic_file():

	try:
		# return the scansion by displaying the content of the file in a new tab
		return send_file(session["output_file_path_3"], cache_timeout=0)
	except:
		return render_template('errors/500.html', lang='Vedic', title="Error"), 500

# 11) route from 7) Vedic home if user uses the textarea form
@app.route("/display_vedic_text", methods=["POST"])
def display_vedic_text():

		# if the user submits the second form (textarea) with the SCAN TEXT button

		# get the text from the textarea
		current_text = request.form.get("textarea")
		print(current_text)

		# use time,strftime to get the current time for new filenames
		current_time = time.strftime("%Y%m%d-%H%M%S")
		# store this current time in session so that it's valid for the current user's file only
		session["current_time_name"] = current_time
		###print(session["current_time_name"])

		# create path for new source file with current time as filename
		session["source_file_path_4"] = os.path.join(app.config['UPLOAD_FOLDER'], session["current_time_name"])

		# open this new file and write the textarea text into it (this creates the file) - then close the file
		source_file = open(session["source_file_path_4"], 'w')
		source_file.write(current_text)
		###print(source_file)
		source_file.close()

		# create path to target file (adding the .txt extension just in case we'll make this downloadable in the future)
		session["output_file_path_4"] = os.path.join(app.config['UPLOAD_FOLDER'], session["current_time_name"] + "_SCAN.txt")
		###print(session["output_file_path_4"])

		# open source file for use (reading mode)
		with open(session["source_file_path_4"], 'r') as text:

			# create target file by opening it in writing mode
			with open(session["output_file_path_4"], 'w') as target:

				# get the status of the checkbox4 (if checkd == on, if unckecked == None)
				remove_verse_num = request.form.get('checkbox4')
				print(remove_verse_num)

				# For each line,
				for line in text:
					# remove the trailing newline (if the final line doesn't have a newline, no problem)
					line = line.rstrip('\n')
					# and write the contents of the line (and newline).
					###print(line)
					target.write(line + '\n') # it's useful to do this here and not before, because if the final line has no newline, this will add it

					# if checkbox was ticked (== on) the user indicated that there is a verse number at the beginning. So remove it
					if remove_verse_num == "on":
						pada = line.split(" ", 1)[-1]
						print(pada)
						# Optional: remove leading (and trailing whitespaces) that may have been left by split
						#pada = pada.strip()
					else:
						pada = line

					###print(pada)

					# process the pada and write it in the target file
					vedic_meterscanner(pada, target)

		try:
			# return the scansion by displaying the content of the file in a new tab
			return send_file(session["output_file_path_4"], cache_timeout=0)
		except:
			return render_template('errors/500.html', lang='Vedic', title="Error"), 500



# ERROR HANDLERS

# 404 - Page Not Found error
@app.errorhandler(404)
def error_404(error):

	# N.B. in Flask, routes "return" returns 2 things
	# 1) a render_template or a redirect instruction
	# 2) the status code
	# Normally the default status code is 200 and can be omitted
	# but if you want to return a different status code, you name it explicitly after a comma
	return render_template('errors/404.html'), 404


# 500 - Server error (also FileNotFound errors)
@app.errorhandler(500)
def error_500(error):

	return render_template('errors/500.html'), 500
