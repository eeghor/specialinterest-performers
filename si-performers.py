from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
import sys
import os

class SpiPerformers:

	def __init__(self, perf_kind):

		self.PERFS = perf_kind
		self.WIKICAT_URL = 'https://en.wikipedia.org/wiki/Category:'
		self.DATADIR = 'data'

		self.CATS = {'life_coaches': ['Life_coaches'], 	
					 'motivational_speakers': ['Motivational_speakers'],
					 'spoken_word_artists': [f'{nat.capitalize()}_spoken_word_artists' for nat in 'american british'.split()],
					 'professional_magicians': ['Professional_magicians'],
					 'hypnotists': [f'{nat.capitalize()}_hypnotists' for nat in 'american australian british'.split()],
					 'lgbt_comedians': ['LGBT_comedians'], 
					 'ventriloquists': ['Ventriloquists'],
					 'psychics': [f'{nat.capitalize()}_psychics' for nat in 'american australian british irish'.split()],
					 'stunt_performers': [f'{nat.capitalize()}_stunt_performers' for nat in 'american australian british'.split()]}

		self.URLS = [f'{self.WIKICAT_URL}{_}' for _ in self.CATS[self.PERFS]]

		self.perfs_names = set()

	def get(self):

		for url in self.URLS:

			print(url)

			soup = BeautifulSoup(requests.get(url).text, 'lxml')	
			
			possible_class_names = ['mw-category-group', 'mw-content-ltr']

			for pc in possible_class_names:

				_found_divs = soup.find_all('div', class_=pc)

				if not _found_divs:
					continue
				else:
					for _ in _found_divs:
						for li_ in _.find_all('li'):
							self.perfs_names.add(unidecode(li_.text.lower().split('(')[0].strip()))
					break

		return self

	def save(self):

		fname = f'{self.PERFS}.txt'

		if not os.path.exists(self.DATADIR):
			os.mkdir(self.DATADIR)

		if self.perfs_names:
			with open(os.path.join(self.DATADIR, fname), 'w') as f:
				for _ in self.perfs_names:
					f.write(f'{_}\n')

		print(f'saved {len(self.perfs_names)} {self.PERFS} to file {fname}')


if __name__ == '__main__':

	sp = (SpiPerformers('stunt_performers')
						.get()
						.save())
