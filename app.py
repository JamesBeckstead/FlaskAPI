from flask import Flask, jsonify, request, Response
import json
app = Flask(__name__)

# list of dictionaries containing books
books = [
	{
		'name': 'Green Eggs and Ham',
		'price': 7.99,
		'isbn': 97839400165
	},
	{
		'name': 'The Cat in the Hat',
		'price': 6.99,
		'isbn': 9782371000193
	} 
]

def valid_book_details(book_data):
	if ('name' in book_data 
			and 'price' in book_data 
				and 'isbn' in book_data):
		return True
	else:
		return False

# GET /books/isbn#
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
	return_value = {}
	for book in books:
		if book['isbn'] == isbn:
			return_value = {
				'name': book['name'],
				'price': book['price']
			}
	# must call jsonify to convert dict to json object
	return jsonify(return_value)

def valid_put_request_data(put_data):
	if ('name' in put_data and 'price' in put_data):
		return True
	else:
		return False

#PUT /books/1234567890
# example
# {
# 	'name': name_of_book,
# 	'price': 0.99
# }
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
	request_data = request.get_json()
	if (not valid_put_request_data(request_data)):
		invalidBookErrorMsg = {
			'error': "Valid book ojbect must be passed to this request",
			'helpString': "Data should be as follows: {'name': name_of_book, 'price':1.99}"
		}
		response = Response(json.dumps(invalidBookErrorMsg), status=400, mimetype='application/json')
		return response
	new_book = {
		'name': request_data['name'],
		'price': request_data['price'],
		'isbn': isbn
	}
	i = 0
	for book in books:
		currentIsbn = book['isbn']
		if currentIsbn == isbn:
			books[i] = new_book
		i += 1
	response = Response('', status=204)
	return response


# POST /books
# data should be sent in json as below
# {
# 	'name': 'F',
# 	'price': 6.99,
# 	'isbn': 0123456789
# }
@app.route('/books', methods=['POST'])
def add_book():
	# retrieve the json object
	book_data = request.get_json()
	# confirm it is a valid book
	if valid_book_details(book_data):
		new_book = {
			'name': book_data['name'],
			'price': book_data['price'],
			'isbn': book_data['isbn']
		}
		# insert the book at the top of the list
		# top of list for ease of testing
		books.insert(0, new_book)
		# return string becuase Flask automatically sets code to
		# test/html and status code to 200
		# return 'True'
		# clearer response to user
		response = Response('', status=201, mimetype='application/json')
		response.headers['Location'] = "/books/" + str(new_book['isbn'])
		return response
	else:
		# 
		invalidBookErrorMsg = {
			'error': "invalid book object was passed in request",
			'helpString': "Data must be as follows:{'name': 'bookname', 'price': 7.99, isbn: 1234567890"
		}
		response = Response(json.dumps(invalidBookErrorMsg), status=400, mimetype='appliation/json')
		return response

# GET /store
@app.route('/books')
def hello_world():
	# json object to show all books on record
	return jsonify({'books': books})

#PATCH /books
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
	request_data = request.get_json()
	updated_book = {}
	if ('name' in request_data):
		updated_book['name'] = request_data['name']
	if ('price' in request_data):
		updated_book['price'] = request_data['price']
	for book in books:
		if book['isbn'] == isbn:
			book.update(updated_book)
	response = Response('', status=204)
	response.headers['Location'] = '/books/' + str(isbn)
	return response

app.run(port=5000)
