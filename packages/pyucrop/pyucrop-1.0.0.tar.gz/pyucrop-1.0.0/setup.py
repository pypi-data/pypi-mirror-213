import setuptools
with open(r'C:\Users\User\Desktop\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='pyucrop',
	version='1.0.0',
	author='Redpiar',
	author_email='Regeonwix@gmail.com',
	description='test',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['pyucrop'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)