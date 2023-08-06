 
<!-- # django-singleton -->

[![Documentation Status](https://readthedocs.org/projects/django-singleton2/badge/?version=latest)](https://django-singleton2.readthedocs.io/en/latest/?badge=latest)

- [The app](#the-app)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
- [The process of creating the app](#the-process-of-creating-the-app)
  - [Operating System](#operating-system)
  - [Project Structure](#project-structure)
  - [setup a sensible environment (part 1)](#setup-a-sensible-environment-part-1)
    - [pyenv](#pyenv)
    - [poetry](#poetry)
    - [tox](#tox)
    - [pytest](#pytest)
    - [black](#black)
    - [sphinx](#sphinx)
  - [bootstrap your repository](#bootstrap-your-repository)
    - [bootstrapping the app](#bootstrapping-the-app)
    - [boostrapping the project to develop against](#boostrapping-the-project-to-develop-against)
    - [bootstrapping the documentation](#bootstrapping-the-documentation)
  - [setup a sensible environment (part 2)](#setup-a-sensible-environment-part-2)
  - [coding](#coding)
    - [connect the app to the example-project](#connect-the-app-to-the-example-project)
    - [documenting the code](#documenting-the-code)
    - [testing the code](#testing-the-code)
    - [versioning the code](#versioning-the-code)
    - [packaging \& publishing the code](#packaging--publishing-the-code)
  - [continuous integration (workflows)](#continuous-integration-workflows)
- [I AM HERE](#i-am-here)
      - [tox](#tox-1)
      - [github actions](#github-actions)
    - [publish](#publish)

-----

# The app

A singleton is a class that can only be instanciated a single time.  `SingletonMixin` turns any Django Model into a singleton.  

## Installation

Install with pip or your favorite Python package manager.

```
pip install django-singleton2
```

Add "singleton2" to your `INSTALLED_APPS`

```
INSTALLED_APPS = [
  ...
  'singleton2',
]
```

## Configuration

Update _settings.py_ if you feel like it:

```
SINGLETON_RAISE_ERROR_ON_SAVE = True|False
```

The default value is False.

## Usage

```
from django.db import models
from singleton2.models import SingletonMixin

class MySingletonModel(SingletonMixin, models.Model):
  pass

my_singleton_instance = MySingletonModel.load()
```

Validation errors will ocurr if you try to save more than one instance of a singleton via a form (such as in the Django Admin).  These will be handled by normal Django form processing.  

If you try to save more than one instance of a singleton outside of a form then nothing will happen, unless `SINGLETON_RAISE_ERROR_ON_SAVE` is set to True in which case an exception will be raised.


> **Note** that the app is called "django-singleton2" because there is an existing [django-singleton](https://github.com/defbyte/django-singleton) app which does the same thing and works perfectly well.  

-----

# The process of creating the app

All the stuff that other people seem to already know is described here.

## Operating System

I do all of my coding on Linux because I'm not insane.  I use Xubuntu because Ubuntu is pretty standard, but I'm used to having lousy hardware and XFCE takes less processing power than Unity.  Plus, I'm used to it.

These days, a lot of development is done in Docker.  So the underlying OS doesn't really matter.  Still, if I can avoid virutalization I will.  This Django Reusable App does not rely on Docker for development purposes.

## Project Structure

First create the repository in GiHub.  In theory this can be done from the command line using [gh]([https://cli.github.com/), but honestly, I find using the GitHub website GUI a lot more straightforward.  Plus doing it this way can automatically create the "README.md" and "LICENCE" files for you.  

Once that has been done, clone this repository into your local filesystem and then setup the basic directory structure:

```
git clone git@github.com:allynt/django-singleton2.git django-singleton
mkdir -p django-singleton/singleton2
mkdir -p django-singleton/example-project
mkdir -p django-singleton/docs
mkdir -p django-singleton/.github
cd django-singleton/
```

This provides us with a place to store the app, an example project to develop against, documentation, and workflows for CI.

Note that the repository already comes with a ".gitingore" file.  This has been generated from [gitignore.io](https://www.toptal.com/developers/gitignore/api/django,linux,python) with a few extra bits tacked onto the end:

```
# static & media files
example-project/_static/*
example-project/_media/*

# pytest output
example-project/pytest-report.html
example-project/output.json
example-project/archive

# local environment variables
.env.*

# in progress files
*.bak
*.orig
```
You should override this according to your needs.

Now that that's all out of the way run

```
git add .
git commit -m "initial commit"
git push
```

to make sure that github and your local filesystem are in sync.

Since you're using github, now would be as good a time as any to create some templates to help potential collaborators.  I have created issue templates for "bug_reports" and "feature_requests" as well as a pull request template.  Again, this could have been done by manually creating files in ".github" but I find working with the GitHub GUI simpler (and it lets me build upon their existing templates).

I also created a CODE_OF_CONDUCT.md file (as per [here](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-code-of-conduct-to-your-project)) and a CONTRIBUTING.md file (as per [here](https://github.com/nayafia/contributing-template)).

Now that that's all out of the way run

```
git pull
```

to make sure that github and your local filesystem are in sync *again*.

## setup a sensible environment (part 1)

In order to develop code efficiently I use some standard Python tooling.

### pyenv

I use **pyenv** to manage my Python versions.

To install pyenv first make sure the dependencies are installed:

```
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl
```

Then install pyenv itself:
```
$ curl https://pyenv.run | bash
```

and add the following to "~/.bashrc":

```
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Reload the shell and install your favorite versions of python.  Then instruct pyenv which version to use in the repository; I'm using "3.10.0" at the time of writing.

`pyenv local 3.10.0`

This should create a "django-singleton2/.python-version" file.

### poetry

Python package management is hard.  There is also no one standard way of doing it.  Like most developers, I started with **pip** and migrated to **pipenv** and toyed with **piptools** and embraced **poetry** and am intrigued by **pdm** (but dissappointed that [PEP582](https://peps.python.org/pep-0582/) was not endorsed - that would have made working w/ code inside _and_ outside Docker containers much easier).  Poetry handles virtual environments and package dependency management as well as building and publishing code.  To install it simply run:

```
curl -sSL https://install.python-poetry.org | python3 -
poetry self update
poetry completions bash >> ~/.bash_completion
```

Note that the resultant completions file doesn’t work in all versions of bash; multi-word case statements have to be encased in quotes.

Next setup some config:

```
poetry config virtualenvs.in-project true`
```

This ensures that all virtual environments will be located in the project directory in a directory called ".venv".  This is very useful for integrating your virtual environments with your IDEs as we'll see later on.

From here on, when I instruct you to install a specific python package you should use poetry to be doing this.  All the installed packages will be recorded in a "pyproject.toml" file.  As you develop it is a good idea to generate a "poetry.lock" file that locks all dependencies to a specific version.  

I would say that this is essential when developing a Django Project but not when developing a Django Reusable App.  Anybody that uses it will incorporate it into their own "poetry.lock" file.  And, anyway, tox will reinstall dependencies during testing as we'll see later.  

Don't forget to run `poetry init` to create your virtual environment and get the whole process started.
### tox

**Tox** allows me to test my app across multiple library versions.  When writing Django Resuable Apps, the main libraries you care about are Python and Django, obviously.  If this were a more complex app, I might choose to test against multiple versions of other libraries such as Django Rest Framework.

Installing tox with poetry is very straightforward:

`poetry add --group dev tox="*"`

Note that this installs it as a "dev" dependency which means that poetry will not bundle the tox package when building districution of our app.  

tox is configured with a tox.ini file.  For a start I recommend:

```
[tox]
envlist = py{38,310}-django{32,40,41}
isolated_build = true

[testenv]
allowlist_externals = 
    poetry
deps =
    pytest
commands_pre = 
    poetry install --no-root --sync
commands =
    poetry run pytest ./example-project
```

I will add to this file throughout this document.  And I will write more about tox in the testing section.

### pytest

Django comes with its own testing framework.  And it's pretty good.  If you are content with it that's fine.  I like to have a bit more control over my test runners.  And I like the way that pytest uses fixtures.  And I've just gotten used to it over the years.  So I use **pytest**. 

`poetry add --group dev pytest pytest-django pytest-html-reporter factory-boy`

There are several useful [pytest plugins](https://docs.pytest.org/en/7.2.x/reference/plugin_list.html) you can add if you like.

I'll write more about pytest in the testing section.

### black

I use **black** for linting because I like my code to be pretty.  Install it like this:

`poetry add --group dev black`

I have usually used **yapf** (Yet Another Python Formatter) because it can be configured and there are just a few personal stylistic idiosynchrasies that bug me.  But when writing a Django Reusable App where other developers might contribute, I concede that it makes sense to use something that can't be configured and therefore makes it impossible to get into arguments about coding style.  Hence, **black**.

### sphinx


I use **sphinx** for documenting my code.  This will automatically parse docstings in code as follows::

```
class MyClass(object):
  """
  I am a docstring for the class
  """

  def my_function(self, *args, **kwargs):
    """
    I am another docstring for the function
    """
    pass

  
  my_variable = True
  """
  I am yet another docstring for the variable
  (notice how I come after the definition)
  """
  
  pass
```

When I have comments that I don't need to be documented, I use the following syntax:

```
def my_complex_function(*args, **kwargs):
  for i in range(100):
    # this is a complex process that I want to leave a comment about, but I don't need sphinx to parse it
    do_something(i)
```

Install sphinx, and some associated packages that I like, using

`poetry add --group docs sphinx sphinx-rtd-theme myst-parser`

By default sphinx can parse ReStructuredText documents.  `myst-parser` allows it to parse MarkDown (which is not only more intuitive, it is also what GitHub wrote your README file in).  And `sphinx-rtd-theme` incorporates the standard theme used by ReadTheDocs - which is where our documentation is going to wind up (assuming this app is going to be public).

## bootstrap your repository

Recall that we created some empty directories at the root of our repository.  We can now flesh them out with actual content.  I have created several templates that can be used to help with this process.  If you don't like my templates, then just use the standard bootstrapping tools.  If you find my templates too complex, then just copy this repository and change the bits you don't like.

### bootstrapping the app

This is easy.  Just run:

`django-admin startapp --template=https://github.com/allynt/django-reusable-app-template/archive/master.zip singleton2` 

and the "singleton2" directory will be populated with the stubs needed to develop your app. 

This is a pretty standard Django App with the following tweaks:

* "apps.py" tries to register any checks and signals associated w/ the app
* "checks.py" includes some standard checks I run against all my apps; these can be expanded as needed
* "conf.py" includes app-specific configuration using the **django-appconf** reusable app
* "urls.py" includes an empty `urlpatterns` array that will be referenced by the example-project below

### boostrapping the project to develop against

This is also easy:

`django-admin startproject --template=https://github.com/allynt/django-reusable-app-project-template/archive/master.zip example example-project` 

to populate the "example-project" directory.

When developing a Resuable Django App, there are different approaches to testing and building migrations.  I've come across a lot of apps that just don't document this at all.  I've come across others that have special scripts which *fake* a Django Project (ie: just a minimal "settings.py" file) to run `django.setup()` with so that the app can be loaded in order to generate migrations.  But I feel like it makes sense to use a *real* Django Project so that you can interact with your app naturally.  

Therefore the "example-project" that I create can be run just like any other Django Project.  It will allow me to generate migrations.  And it will allow me to run tests (located in "example-project/example/tests").  But, crucially, it will also allow me to hack about and make sure I understand exactly how the app works.

I am quite partial to many of the ideas recommended by Cookiecuter Django and so this example-project uses some of their ideas.

* a separate app called "config" where all project-level configurations like "settings.py" and "urls.py" go
* an app called "example" where all the code that will use the Django Resuable App goes - this includes a "tests" module 
* some custom additions to the "settings.py" file, including the use of **django-environ** to read environment variables

### bootstrapping the documentation

As mentioned above I use sphinx for the documentation.  I have provided a template that tweaks the default documentation structure - including linking the README.md file and autogenerated documentation to the index page.  This template is available at [https://github.com/allynt/django-reusable-app-sphinx-template](https://github.com/allynt/django-reusable-app-sphinx-template).  At the time of writing, the sphinx CLI cannot use a remote template, therefore this repository must first be cloned locally and then the following command

`cd docs && sphinx-quickstart --templatedir=django-reusable-app-sphinx-template/templates .` will create some initial documentation.

You can add any additional documentation files you want within the "doc" directory.  Just make sure to include a reference to it underneath the `:toc` directive in "index.rst".  
## setup a sensible environment (part 2)

An IDE makes life a lot easier.  I use **VSCode**.  I have therefore included a ".vscode/settings.json" file (and a generic ".editorconfig" file) to configure a few nice features.  My configuration includes a path to the virtual environment created by poetry (".venv") in order to do code-completion as well as linting. 

In theory, keeping these files with the repository not only makes it easier for *me* to code, it makes it less likely for *you* to push code that conflicts with my style.

> *TODO* Although, I may also add a github action to automatically lint all incoming code.

I also have some particularly useful VSCode plugins installed:
* MS Python (this will install loads of other useful plugins)
* Markdown all in one
* Better comments
* Better ToML
* DotENV
* Intellicode
* Tabnine

*Actually, I use a few more plugins for full-stack development, but these are the ones that are relevant for creating Django Resuable Apps.*

## coding

So that is most of the setup required before finally diving into actual coding.  There are a few other things that are needed to actually run, test, document, publish, etc. the code.

### connect the app to the example-project

Obviously, we need to tell **example-project** about **django-singleton2**.  This is very straightforward, just add the following to "example-project/config/settings.py":

```
LOCAL_APPS = [
    "singleton2",
    "example",
]
```

If your app is more complex then there will probably be some additional configuration needed, such as adding your views to "example-project/config/urls.py", etc.

You also need to make sure that all of your app's dependencies are installed:

`poetry add django django-appconf django-environ`

Now try running `poetry run ./example-project/manage.py runserver` and see if something appears at "localhost:8000".  If not, you messed up.

### documenting the code

I have already discussed using **sphinx** to automatically generate some nice documentation.  I am going to host my documentation on readthedocs because I deserve it.  This requires registering the repository with readthedocs.  There is probably a way to do this on the command line, but I just signed up for an account on readthedocs.org and then manaually used their GUI to import this repostiroy.  

Having done that, it might look pretty if you add their badge to the README.md file:

```
[![Documentation Status](https://readthedocs.org/projects/django-singleton2/badge/?version=latest)](https://django-singleton2.readthedocs.io/en/latest/?badge=latest)
```

I am using tox to generate documentation because *why not*?  I have added a separate section to the "tox.ini" file to deal w/ this.  Now, the [official tox documentation](https://tox.wiki/en/latest/example/documentation.html#sphinx) recommends bypassing the Makefile generated by `sphinx-quickstart` but I disagree.  Why *wouldn't* I want to continue using the official approved way of generating documentation?  All I want to do w/ tox is to eventually integrate this into CI and just run `poetry run tox -e docs`.

Anyway, doing things the "official" way got pretty complicated b/c of dependencies.  So I added `make` to the commands in "allowlist_externals" and added the following section:

```
[testenv:docs]
deps = 
    sphinx
    sphinx-rtd-theme
    myst-parser
changedir = docs
commands = 
    make clean
    make html SPHINXOPTS="-v"
```

In order for this to work I had to create a ".readthedocs.yml" file which points to "docs/requirements.txt" in order to specify exactly what dependencies are required to run the codebase (since it needs to be loaded for auto-generated documentation).  Although readthedocs *can* parse the "pyproject.toml" file, it ignores grouped dependencies.  So to populate "docs/requirements.txt" I ran `poetry export -f requirments.txt --only docs --output docs/requirements.txt`.

Having done all of this will result in https://django-singleton2.readthedocs.io being auto-generated whenever the master branch is pushed to.

If you want additional auto-generated code documentation, just modify "docs/singleton2.rst" to specify which modules / classes / methods should be included.
### testing the code

As mentioned earlier, I use **pytest** as my test runner and **tox** to coordinate testing across multiple environments.  This all requires a bit more config.  First make sure **pytest-django** and **factory-boy** are installed.  These make pytest work a bit nicer w/ Django.  The general syntax I use for a test is:

> *TODO* Add test artefacts from pytest-html-reporter

```
import factory
import pytest

from example.models import ExampleSingletonModel

class ExampleSingletonModelFactory(factory.django.DjangoModelFactory):
    """
    creates an instance of ExampleSingletonModel w/ random field values to use in tests
    """
    class Meta:
        model = ExampleSingletonModel

    name = factory.Faker("word")

@pytest.mark.django_db
class TestSingleton:
    """
    collection of test methods that hit the Django database
    """
    def test_something(self):
        singleton = ExampleSingletonModelFactory()
        assert singleton_1.pk is not None
```

Using pytest requires a "pytest.ini" file w/ the following minimal content:

```
[pytest]
DJANGO_SETTINGS_MODULE=config.settings
python_files = tests.py test_*.py *_tests.py
addopts = --nomigrations
```

This tells pytest how to start Django and which files to run. (It also instructs it not to bother running any unmigrated migrations.)

To run the tests simply run the following command:

```
poetry run pytest ./example-project
```
 
Or, better yet, add a new section to "tox.ini":

```
[testenv:coverage]
skip_install = true
deps =
    coverage
commands =
    poetry run pytest --cov=singleton2 ./example-project
```
If you like you can add a test-coverage report using the **pytest-cov** library.  I am undecided as to whether this is a good idea.  I feel like using it as a measure of test quality gives a false sence of security.  And, anyway, aiming for 100% coverage is unrealistic.  What is important is testing the *relevant* bits of code under *realistic* use-cases.


To run a coverage report simply run the following command:

```
poetry run pytest --cov=singleton2 ./example-project
```

This will measure the coverage of all code under "singleton2" (it focuses on the app and excludes the example-project).  Some of the modules within "singleton2" don't really need to be included in a coverage report.  Therefore we can add the following section to "tox.ini"


configuration file ".coveragerc":

```
[run]
omit = singleton2/migrations/*, singleton2/tests/*
```

### versioning the code

### packaging & publishing the code

Assuming this is a _real_ Django Reusable App you will want to publish to PyPi.

This requires creating an account on [pypi.org](pypi.org) and creating an API token, then adding that token to your poetry credentials:

`poetry config pypi-token.pypi <token>`

Once that is configured, packaging and publishing can be done in a single step: `poetry publish --build`.
## continuous integration (workflows)

# I AM HERE
  

I'll talk about how to configure the documentation below.
I AM HERE

TODO:
* distributed tox (just use the -p flag) - done
* get tox to build documentation - done but turns out its a bad idea
* push documentation to readthedocs - done
* look into documentation on github pages (for private repositories)
* prevent tox from including docs dependencies for tests - done but don't like solution
* run tox on PRs -done
* https://pypi.org/project/tox-gh-actions/
* dynamic versioning: https://github.com/mtkennerly/poetry-dynamic-versioning
* badges


#### tox

Tox allows me to test a matrix of package versions.  The obvious thing to do is to test it against different versions of Python & Django.  To speed things up you can run tox in parallel via `poetry run tox -p all` (although this doesn't provide as much output).

#### github actions

So I want to use poetry to run tox which uses pytest as the runner automatically whenever code is pushed to github.  I do this using github actions and the clever library tox-gh-actions as well as github's publically available [Install Poetry Action](https://github.com/marketplace/actions/install-poetry-action)
  
`mkdir -p .github/workflows`

The section in tox.ini maps github action matrices to tox environments.  For example in the workflow file:

```
strategy:
    matrix:
      python-version: ["3.8", "3.10"]
```

defines 2 versions of python and the corresponding section in the tox config file:

```
[gh-actions]
python =
    3.8: py38
    3.10: py310
```

maps those to the existing "py38" and "py310" arguments at the top of the tox config file.

### publish

use dev-py
