import re
import os
import shutil

from fabric.api import task, local, abort


@task
def script(name, filename=None):
    package = local('python setup.py --name', capture=True)
    if filename is None:
        filename = re.sub(r'[^a-z0-9]+', '_', name)
    scripts = os.path.join(package, 'scripts')
    filepath = os.path.join(scripts, filename + '.py')
    entry = '{} = {}.scripts.{}:main\n'.format(name, package, filename)

    if os.path.exists(filepath):
        abort('Script "{}" already exists.'.format(filename))
    elif not os.path.exists(scripts):
        os.makedirs(scripts)
        open(os.path.join(scripts, '__init__.py'), 'w').close()

    shutil.copyfile(
        os.path.join('fabtasks', 'templates', 'script.py'),
        filepath
    )

    with open('entry-points.ini', 'a') as fh:
        fh.write(entry)
