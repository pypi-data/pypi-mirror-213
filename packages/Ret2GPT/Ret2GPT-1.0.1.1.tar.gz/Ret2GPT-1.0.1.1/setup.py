from setuptools import setup, find_packages

str_version = '1.0.1.1'
name = 'Ret2GPT'
requires_list = open(f'{name}/requirements.txt', 'r', encoding='utf8').readlines()
requires_list = [i.strip() for i in requires_list]

setup(name='Ret2GPT',
      version=str_version,
      description='Ret2GPT: Advanced AI-powered binary analysis tool leveraging OpenAI\'s LangChain technology, revolutionizing CTF Pwners\' experience in binary file interpretation and vulnerability detection.',
      url='https://github.com/DDizzzy79/Ret2GPT',
      author='Retr0',
      author_email='retr0@retr0.blog',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires= requires_list,
      python_requires='>=3',
      entry_points={
        'console_scripts': [
            'Ret2GPT=Ret2GPT.main:main',
        ],
    },
    )