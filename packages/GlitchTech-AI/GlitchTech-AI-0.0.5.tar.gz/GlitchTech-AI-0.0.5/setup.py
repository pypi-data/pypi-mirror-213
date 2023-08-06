from setuptools import setup

# python setup.py sdist
# twine upload dist/*

setup(name='GlitchTech-AI',
      version='0.0.5',
      description='Basic utility to interface with OpenAI via command line or terminal.',
      keywords='openai cli terminal glitchtech',
      author='Clutch_Reboot',
      author_email='clutchshadow26@gmail.com',
      license='GNU General Public License v3.0',
      packages=[
            'glitchtech_ai',
            'glitchtech_ai.tools',
      ],
      py_modules=[
            'glitchtech_ai.glitchtech_ai'
      ],
      entry_points={
            'console_scripts': [
                  'glitchtech-ai = glitchtech_ai:main'
            ]
      },
      zip_safe=False,
      long_description=open('README.md', 'rt').read(),
      long_description_content_type='text/markdown',
      python_requires='>=3.10',
      install_requires=[
            'requests'
      ],
      project_urls={
            "Source": "https://github.com/ClutchReboot/openai-cli",
      },
      )
