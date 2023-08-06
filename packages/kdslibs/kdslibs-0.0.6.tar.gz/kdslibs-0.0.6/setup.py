import setuptools

with open("README.md", "r") as fh:
	description = fh.read()

setuptools.setup(
	name="kdslibs",
	version="0.0.6",
	author="KDS",
	author_email="akdiwahar@gmail.com",
	packages=["kdslibs"],
	description="A sample test package",
	long_description=description,
	long_description_content_type="text/markdown",
	url="https://github.com/akdiwahar/kds",
	license='MIT',
	python_requires='>=3.8',
	install_requires=[]
)

