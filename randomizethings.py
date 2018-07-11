import scrython
import random
from ratelimiter import RateLimiter

@RateLimiter(max_calls=10, period=1)
def query_legendary_creatures(page_num):
    legendary_names = []
    search_results = scrython.cards.Search(q="t:legendary t:creature", page=page_num)
    for card in search_results.data():
        legendary_names.append(card['name'])
    return {'names': legendary_names, 'has_more': search_results.has_more()}

more = True
legendary_cards = []
page_count = 1
while(more):
    query_results = query_legendary_creatures(page_count)
    legendary_cards.extend(query_results['names'])
    more = query_results['has_more']
    page_count += 1
random.shuffle(legendary_cards)
with open('shuffled_legendaries.txt', 'w') as file:
    while len(legendary_cards) > 1:
        card1 = legendary_cards.pop()
        card2 = legendary_cards.pop()
        file.write('{0} : {1}\n'.format(card1, card2))
    if len(legendary_cards) == 1:
        file.write('{0} does not get a partner :_('.format(legendary_cards.pop))
    
