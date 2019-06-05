from flask import Flask, jsonify, request

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
		return 'True'
	else:
		return 'False'

# GET /store
@app.route('/books')
def hello_world():
	# json object to show all books on record
	return jsonify({'books': books})

app.run(port=5000)
