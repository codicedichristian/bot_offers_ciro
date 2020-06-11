
class Item:
    position: 0
    title: ''
    reviews: 0
    link: ''
    price: ''

    def __init__(self, position=0, title='', reviews=0, link='', price=''):
        self.position = position
        self.title = title
        self.reviews = reviews
        self.link = link
        self.price = price
        