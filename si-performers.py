from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
import sys

class SpiPerformers:

	def __init__(self, perf_kind):

		self.PERFS = perf_kind
		self.WIKICAT_URL = 'https://en.wikipedia.org/wiki/Category:'

		self.CATS = {'life_coaches': 'Life_coaches', 'motivational_speakers': 'Motivational_speakers',
						'american_spoken_word_artists': 'American_spoken_word_artists',
						'british_spoken_word_artists': 'British_spoken_word_artists',
						'professional_magicians': 'Professional_magicians',
						'american_hypnotists': 'American_hypnotists',
						'british_hypnotists': 'British_hypnotists',
						'lgbt_comedians': 'LGBT_comedians'}
		self.URL = f'{self.WIKICAT_URL}{self.CATS[self.PERFS]}'

		self.perfs_names = set()

	def get(self):

		soup = BeautifulSoup(requests.get(self.URL).text, 'lxml')	

		for _ in soup.find_all('div', class_='mw-category-group'):
			for li_ in _.find_all('li'):
				self.perfs_names.add(unidecode(li_.text.lower().split('(')[0].strip()))

		return self

	def save(self):

		fname = f'{self.PERFS}.txt'

		if self.perfs_names:
			with open(fname, 'w') as f:
				for _ in self.perfs_names:
					f.write(f'{_}\n')

		print(f'saved {len(self.perfs_names)} {self.PERFS} to file {fname}')


if __name__ == '__main__':

	sp = SpiPerformers('lgbt_comedians').get().save()
