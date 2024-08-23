import random
topics_list ='''
humanbody 

'''.split(' ')



def query_generator():
	return f"Create a youtube short about {topics_list[random.randint(0,len(topics_list)-1)].strip()} with prompt.every facts must be unique it should not be repeated."