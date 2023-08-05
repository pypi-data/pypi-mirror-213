from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

with open("RELEASE.md", 'r', encoding='utf-8') as f:
    release = f.read()

setup(
    author="Subhradeep Rang",
    author_email="srang992@gmail.com",
    python_requires='>=3.7',
    classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
    ],
    description="Package containing icons taken from ionicons website.",
    long_description=readme + "\n\n" + release,
    long_description_content_type='text/markdown',
    license="MIT license",
    keywords='ionicons_python',
    name='ionicons_python',
    version='1.0.3',
    packages=find_packages(),
    package_data={'ionicons_python': ['icons/*.svg', 'colored_icons/*.svg']},
    url='https://github.com/srang992/ionicons_python',
    zip_safe=False,
)