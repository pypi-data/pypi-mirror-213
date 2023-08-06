from setuptools import setup, find_packages

setup(
    name='django-dellavrite',
    version='0.1',
    description='Cheat for ws',
    packages=find_packages(),
    package_data={
        'django-dellavrite': [
            'back/app/migrations/*.py',
            'back/app/migrations/__pycache__/*',
            'back/app/__pycache__/*',
            'back/laba228_back/__pycache__/*',
            'front/assets/*',
            'front/public/*',
            'front/src/components/*',
            'front/src/css/*',
            'front/src/http/*',
        ],
    },
    author_email='delavrite@gmail.com',
    zip_safe=False
)
