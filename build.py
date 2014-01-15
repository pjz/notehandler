import os
import sys
import os.path
from optparse import make_option
from fabricate import main, run, shell, autoclean
from subprocess import check_output

# Core Executables
# ================

name = 'notehandler'

RUN_DEPS = [ 'cmdpy', 'evernote' ]

TEST_DEPS = [ 'coverage', 'pytest' ]


def _virt(cmd, envdir='env'):
    return os.path.join(envdir, 'bin', cmd)

ENV_ARGS = [
            'virtualenv',
            '--distribute',
            '--unzip-setuptools',
            '--prompt=[%s] ' % name,
            ]

def dev():
    if os.path.exists('env'): return
    args = ENV_ARGS + [ 'env' ]
    run(*args)

    for dep in RUN_DEPS + TEST_DEPS:
        run(_virt('pip'), 'install', dep)
    run(_virt('python'), 'setup.py', 'develop')

def clean_dev():
    shell('rm', '-rf', 'env')

def clean():
    autoclean()
    shell('find', '.', '-name', '*.pyc', '-delete')
    clean_dev()
    clean_test()
    clean_build()

# Testing
# =======

def test():
    dev()
    run(_virt('py.test'), 'tests/', ignore_status=True, silent=False)

def analyse():
    dev()
    run(_virt('py.test'),
            '--junitxml=testresults.xml',
            '--cov-report', 'term',
            '--cov-report', 'xml',
            '--cov', name,
            'tests/',
            ignore_status=False)
    print('done!')

def clean_test():
    clean_dev()
    shell('rm', '-f', '.coverage', 'coverage.xml', 'testresults.xml', 'pylint.out')

# Build
# =====

def build():
    run(main.options.python, 'setup.py', 'bdist_egg', 'bdist_wheel')

def clean_build():
    shell(main.options.python, 'setup.py', 'clean', '-a')
    shell('rm', '-rf', 'dist')

def _require_y(prompt, failmsg=''):
    yn = raw_input(prompt).lower()
    if yn not in [ 'y', 'yes' ]:
        print failmsg
        sys.exit(1)


def release():
    if main.options.release is None:
        print("Must specify a version to release with --release <version>")
        sys.exit(1)

    rel = main.options.release

   
    if rel in check_output(['git', 'tag', '-l'],universal_newlines=True).split('\n'):
        print("Version %s is already git tagged." % rel)
        sys.exit(1)

    _require_y("Release version %s ?" % rel)

    open("version.txt", "w").write(rel)
    run(main.options.python, 'setup.py', 'sdist', '--formats=zip,gztar,bztar', 'upload')
    run(main.options.python, 'setup.py', 'bdist_wheel', 'upload')
    shell('git', 'commit', 'version.txt', '-m', 'Release %s' % rel, silent=False) 
    shell('git', 'tag', rel, silent=False)
    open("version.txt", "a").write('-dev')
    shell('git', 'commit', 'version.txt', '-m', 'Bump to %s-dev' % rel, silent=False) 
    shell('git', 'push', silent=False)
    shell('git', 'push', '--tags', silent=False)
    clean_build()
    print("Released!")

def show_targets():
    print("""Valid targets:

    show_targets (default) - this
    build - build an egg
    dev - set up an environment able to run tests in env/
    test - run the unit tests
    pylint - run pylint on the source
    analyse - run the unit tests with code coverage enabled
    clean - remove all build artifacts
    clean_{dev,test} - clean some build artifacts
    release - requres --version and pypi upload rights

    """)
    sys.exit()

extra_options = [ make_option('--python', action="store", dest="python", default="python")
                , make_option('--release', action="store", dest="release", default=None)
                ]

main( extra_options=extra_options
    , default='show_targets'
    , ignoreprefix="python"
     )
