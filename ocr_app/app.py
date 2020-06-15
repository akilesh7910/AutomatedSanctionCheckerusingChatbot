import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, jsonify, make_response
from werkzeug.utils import secure_filename
import pandas as pd
import pytesseract

from iso3166 import countries
import pandas as pd

import re
import numpy as np

from passporteye import read_mrz

from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os
import pandas as pd
from io import BytesIO

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '\\downloads\\'
ALLOWED_EXTENSIONS = {'jpg','jpeg','png'}

pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\akile\\Tesseract-OCR\\tesseract'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			folder=UPLOAD_FOLDER+ filename
			address=request.form['address']
			pob=request.form['pob']
			results=ocr(folder, address, pob)
			print(results)
			rs=(list(results)[0])
			nrr=(list(results)[1])
			return render_template('index.html',rs=rs, nrr=nrr)
	return render_template('index.html')

@app.route('/get', methods=['GET', 'POST'])
def get():
	address=request.form['address']
	pob=request.form['pob']
	folder=request.form['folder']

#	print(folder,address1,pob1)
	results=ocr(folder, address, pob)
	print(results)
	rs=(list(results)[0])
	nrr=(list(results)[1])
	print(rs)
	print(nrr)
	print(type(rs))
	print(type(nrr))

	return render_template('index.html', rs=rs,nrr=nrr)

def ocr(folder,address,pob):
	mrz = read_mrz(folder)

	print(mrz)
	mrz_data = mrz.to_dict()
	t1=mrz_data['names']

	t2=mrz_data['surname']

	t3=mrz_data['names']+" "+mrz_data['surname']

	res = mrz_data['date_of_birth']
	res1=int(str(res)[::-1])
	res2=str(res1)
	t4='/'.join(re.findall('..', res2))

	t5=address

	s=(mrz_data['country'])
	location=countries.get(s)
	f4=list(location)
	my_string = ','.join(map(str, f4))
	newl = [x for v in f4 for x in v.rstrip().split(",")]
	t6=newl[4]

	t7=mrz_data['number']

	t8=mrz_data['country']

	t9=mrz_data['sex']

	foo=mrz_data['expiration_date']
	foo1=int(str(foo)[::-1])
	foo2=str(foo1)
	t10='/'.join(re.findall('..', foo2))

	t11=mrz_data['nationality']

	t12 =pob

	List=[]
	List=[t1, t2, t3,t4,t5,t6,t7,t8,t9,t10,t11,t12]
	df1 = pd.DataFrame(List)
	df=df1.T
	df.columns = ['FirstName','LastName','WholeName','DateofBirth','Address','Country','PassportNumber','CountryCode','Gender','ExpiryDate','PlaceofIssue','PlaceofBirth']
	print(df)
	# reading csv file from url



	credentials_dict = {
	"type": "service_account",
	"project_id": "aki-python",
	"private_key_id": "73202949799976fc76d72d6d38b3935129315a17",
	"private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDADlmjF3ls1Bv/\nbneunQNRnhpN6+XAzA8BOobadowy/hW+k7ivCw1BIO7oFgssGqoszsZlzJAb/Uu3\npY4AC8gq1ybMekYb2ppCB+/k42j8rsac0w6qQNvccdgx3MYcfq2N8ZikqoCHFeqq\np7+g+YhT5DbPP46zakYwOY/8d60LIAr1IzPTOnKb+1c66Oo5j0v0h5LErykvy+9D\n0Etctq7mc5R1b+gVqf6OVKPA6vsFUb2GpBWQFlX831s6Iklsw48uAynj++XbWnHH\nV41hwsUMnsdlw1vn15cZ/8LI63Dwk+5vYhU5ljOhXJpggnLhX1+8QEWqtnGUixGL\nGq5HHJtZAgMBAAECggEADWb69Z0B39ix7vppHu3tUTzimkkx1mlPCz+HsVdYO4c8\nYnkZyFpRtZesIFVIeI6QTVHtKaWzsUZU6jcDAKkR0f6DYj3Opmsz/FNkN+FwPkDe\nkotOcM5XoWuu4fTlfM/QwfDn/Wa6EyMyBfBwmJXNQAhzFDWb2lSaWwtrSzuZP2dB\nDsMFwRwTj/tj/jKBh3LR8ndIjA3kvUKYgFSC7VtmrwNrKpOurtnd8Hw7GUbEihuA\nm3FqCL5ThMPS5QgGxpcwPwkgEGuRcsEM3LH+J91EvgU25RUhLLO4p6R2jju9mvnE\nud9OvfJKcA2n2R10Ii2giVmzpgRvWQnXvZiURKDxcQKBgQD079rTxCSDeGSPBS0X\n6I+3SA8g6MVA1/6ZhxKK6+f17u6VbevhXZnzloj//y8R82KMjBD6WWOzF8wj2gF7\nH+E4yi38pn91BoNQEhHVn2FiotVVNIZwhxOW8c7LjucCLMkhi2US6PKZVJ3WN48I\niZN1BL8mwnWkHIqYHTtkC+gziQKBgQDIuwv9cxNZf1m90Hyh/ZMHHzkEGxmhv5kf\nXE68kI48VznduxTtT5nx4ok2VkKgm+DV3d1aXCWMNl5HRhqIiJIa0ZvzEkdyGATS\nnTCRMVYeyOu6rciX9Hbt7/h5hWoktdG3UytJtl3u0Ysc3fX7v2adsBheTxkBDWJz\ntYSPacWlUQKBgDkeUgZ+QBGUmsara1ee+RzBph2DirRTamD9GbrhxocYf/TC3HYC\nsOsYGLyyEpT6D+o8o5zuCYzzKLzXku7WgVwP8edwIFr2+NpMTHJnp3ssA9nJ1Owa\n49uYaiQYIBDmxsSW0Cw3vJM7I0+YRzezdXqdb8InKO3rZfqRHo93I2AZAoGBAJOi\nBoKFRYD4ij9x/IiD4MRHMX8Uk3iEW5FWKc7EHujAWp36/7w+ZIIj1DkznlNT8jw5\nrpjL1w3V2ude5xruH088RQ+0rPl8MufYlqTi/W0s5zton3UrZuE/Mqfl+RhA5ZqI\nv/i5+UIxubgkg8uBjW6C2plaYZCFkJh7s6Bq8ePRAoGAGlGjbWRPb21JcRVf6P9j\nlJIcDkdTGekis3+/ySFvFeG73wLiISXPqSzqnzGBft3NkIJzJqBxx1V9hvzfN+Ua\n7VhLglr/vHbVk6pqkZ7Od2O+YPzCCQRow4q+4sIYPGgqnn0qTDoMFHAs0C2Uw79x\nJsymjxtXE6JuAaYAXZ0QYRk=\n-----END PRIVATE KEY-----\n",
	"client_email": "akilesh7910@aki-python.iam.gserviceaccount.com",
	"client_id": "114127699863693119653",
	"auth_uri": "https://accounts.google.com/o/oauth2/auth",
	"token_uri": "https://oauth2.googleapis.com/token",
	"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
	"client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/akilesh7910%40aki-python.iam.gserviceaccount.com"
	}

	credentials = ServiceAccountCredentials.from_json_keyfile_dict(
	credentials_dict
	)
	client = storage.Client(credentials=credentials, project='aki-python')
	bucket = client.get_bucket('thesis-akilesh7910')
	blob = bucket.blob('MockSanctionFormatted.csv')

	content = blob.download_as_string()

	sanction = pd.read_csv(BytesIO(content))
	def levenshtein_ratio_and_distance(s, t, ratio_calc = False):
	    """ levenshtein_ratio_and_distance:
	        Calculates levenshtein distance between two strings.
	        If ratio_calc = True, the function computes the
	        levenshtein distance ratio of similarity between two strings
	        For all i and j, distance[i,j] will contain the Levenshtein
	        distance between the first i characters of s and the
	        first j characters of t
	    """
	    # Initialize matrix of zeros
	    rows = len(s)+1
	    cols = len(t)+1
	    distance = np.zeros((rows,cols),dtype = int)

	    # Populate matrix of zeros with the indeces of each character of both strings
	    for i in range(1, rows):
	        for k in range(1,cols):
	            distance[i][0] = i
	            distance[0][k] = k

	    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions
	    for col in range(1, cols):
	        for row in range(1, rows):
	            if s[row-1] == t[col-1]:
	                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
	            else:
	                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
	                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
	                if ratio_calc == True:
	                    cost = 2
	                else:
	                    cost = 1
	            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
	                                 distance[row][col-1] + 1,          # Cost of insertions
	                                 distance[row-1][col-1] + cost)     # Cost of substitutions
	    if ratio_calc == True:
	        # Computation of the Levenshtein Distance Ratio
	        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
	        return Ratio
	    else:
	        # print(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
	        # insertions and/or substitutions
	        # This is the minimum number of edits needed to convert string a to string b
	        return "The strings are {} edits away".format(distance[row][col])

	sanction1=sanction['FirstName']
	sanction1=sanction1.fillna('Unknown')
	sec1=df['FirstName']
	h1=sanction1.apply(lambda x:levenshtein_ratio_and_distance(sec1[0],x,ratio_calc=True))
	f1=h1.max()

	sanction2=sanction['LastName']
	sanction2=sanction1.fillna('Unknown')
	sec2=df['LastName']
	h2=sanction2.apply(lambda x:levenshtein_ratio_and_distance(sec2[0],x,ratio_calc=True))
	f2=h2.max()

	sanction3=sanction['WholeName']
	sanction3=sanction1.fillna('Unknown')
	sec3=df['WholeName']
	h3=sanction3.apply(lambda x:levenshtein_ratio_and_distance(sec3[0],x,ratio_calc=True))
	f3=h3.max()

	sanction4=sanction['DateofBirth']
	sanction4=sanction4.fillna('Unknown')
	sec4=df['DateofBirth']
	h4=sanction2.apply(lambda x:levenshtein_ratio_and_distance(sec4[0],x,ratio_calc=True))
	DOB=h4.max()


	sanction5=sanction['Address']
	sanction5=sanction5.fillna('Unknown')
	sec5=df['Address']
	h5=sanction5.apply(lambda x:levenshtein_ratio_and_distance(sec5[0],x,ratio_calc=True))
	f4=h5.max()

	sanction6=sanction['Country']
	sanction6=sanction6.fillna('Unknown')
	sec6=df['Country']
	h6=sanction6.apply(lambda x:levenshtein_ratio_and_distance(sec6[0],x,ratio_calc=True))
	f6=h6.max()

	sanction7=sanction['CountryCode']
	sanction7=sanction7.fillna('Unknown')
	sec7=df['CountryCode']
	h7=sanction7.apply(lambda x:levenshtein_ratio_and_distance(sec7[0],x,ratio_calc=True))
	f12=h7.max()

	sanction8=sanction['PassportNumber']
	sanction8=sanction8.fillna('Unknown')
	sec8=df['PassportNumber']
	h8=sanction8.apply(lambda x:levenshtein_ratio_and_distance(sec8[0],x,ratio_calc=True))
	f8=h8.max()

	sanction9=sanction['Gender']
	sanction9=sanction9.fillna('Unknown')
	sec9=df['Gender']
	h9=sanction9.apply(lambda x:levenshtein_ratio_and_distance(sec9[0],x,ratio_calc=True))
	f5=h9.max()

	sanction10=sanction['ExpiryDate']
	sanction10=sanction10.fillna('Unknown')
	sec10=df['ExpiryDate']
	h10=sanction10.apply(lambda x:levenshtein_ratio_and_distance(sec10[0],x,ratio_calc=True))
	EDate=h10.max()

	sanction11=sanction['PlaceofIssue']
	sanction11=sanction11.fillna('Unknown')
	sec11=df['PlaceofIssue']
	h11=sanction11.apply(lambda x:levenshtein_ratio_and_distance(sec11[0],x,ratio_calc=True))
	f11=h11.max()

	sanction12=sanction['PlaceofBirth']
	sanction12=sanction12.fillna('Unknown')
	sec12=df['PlaceofBirth']
	h12=sanction12.apply(lambda x:levenshtein_ratio_and_distance(sec12[0],x,ratio_calc=True))
	f7=h12.max()


	WN=0.76
	FN=0.72
	LN=0.80
	Addr=0.59
	Coun=0.59
	POB=0.75
	PNo=0.47
	Gen=1.0
	EDate=0.88
	POI=0.69
	CounDes=0.6
	n = 0
	if(WN>f1):
		n+=0.166
		if(FN>f2):
			n+=0.055
			if (LN>f3):
				n+=0.055
				if (Addr>f4):
					n+=0.166
					if (Gen>f5):
						n+=0.055
						if (Coun>f6):
							n+=0.055
							if (POB>f7):
								n+=0.055
								if (PNo>f8):
									n+=0.166
									if (EDate>f10):
										n+=0.055
										if (POI>f11):
											n+=0.055
											if (CounDes>f12):
												n+=0.055
#	print(n)
	if 0 <=n <= 0.4:
		e="You are eligible to apply for Loan"
	elif 0.4 <=n <= 0.6:
 		e="You can only apply for PPP loan at the moment"
	elif 0.6 <=n <= 0.7:
		e="You need to come in contact with representative for further vetting"
	elif n>0.7:
		e="You are higly liable and ineligible to apply for loan"

	return [str(n),e]



@app.route('/downloads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],
  							   filename)
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)

    app.debug = True
    app.run()
