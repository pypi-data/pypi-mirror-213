from setuptools import setup, find_packages


setup(
	name='docketanalyzer',
	version='0.0.1',   
	description='',
	url='https://github.com/docketanalyzer/docketanalyzer',
	author='Nathan Dahlberg',
	package_dir={'': 'src'},
	packages=find_packages('src'),
	install_requires=[
		'click',
		'pathlib',
		'simplejson',
	],
	entry_points={
		'console_scripts': [
			'docketanalyzer = docketanalyzer:cli',
		],
	},
)

