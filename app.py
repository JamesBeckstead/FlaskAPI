from flask import Flask, jsonify

app = Flask(__name__)

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
	return jsonify(return_value)

# GET /store
@app.route('/books')
def hello_world():
	return jsonify({'books': books})

app.run(port=5000)