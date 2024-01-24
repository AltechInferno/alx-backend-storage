#!/usr/bin/env python3
'''changes all topics of a collection based on name
'''
def update_topics(mongo_collection, name, topics):
    '''changes all topics of a collection's document based on
        the name.
    '''
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
