
class Item:
    position: 0
    title: ''
    reviews: 0
    price: ''

    def __init__(self, position=0, title='', reviews=0, price=''):
        self.position = position
        self.title = title
        self.reviews = reviews
        self.price = price