# Copyright 2013, 2014, 2015, 2016, 2017, 2020, 2022 Andrzej Cichocki

# This file is part of pyven.
#
# pyven is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyven is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyven.  If not, see <http://www.gnu.org/licenses/>.

import setuptools

def long_description():
    with open('README.md') as f:
        return f.read()

# Copyright 2013, 2014, 2015, 2016, 2017, 2020, 2022 Andrzej Cichocki

# This file is part of pyven.
#
# pyven is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyven is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyven.  If not, see <http://www.gnu.org/licenses/>.

class SourceInfo:

    class PYXPath:

        suffixes = '.pyx', '.c'

        def __init__(self, module, path):
            self.module = module
            self.path = path

        def buildrequires(self):
            if self.path.endswith('.pyx'):
                yield 'Cython'

        def make_ext(self):
            g = {}
            with open(self.path + 'bld') as f: # Assume project root.
                exec(f.read(), g)
            return g['make_ext'](self.module, self.path)

    def __init__(self, rootdir):
        import os, setuptools, subprocess
        self.packages = setuptools.find_packages(rootdir)
        extpaths = {}
        def addextpaths(dirpath, moduleprefix):
            names = sorted(os.listdir(os.path.join(rootdir, dirpath)))
            for suffix in self.PYXPath.suffixes:
                for name in names:
                    if name.endswith(suffix):
                        module = "%s%s" % (moduleprefix, name[:-len(suffix)])
                        if module not in extpaths:
                            extpaths[module] = self.PYXPath(module, os.path.join(dirpath, name))
        addextpaths('.', '')
        for package in self.packages:
            addextpaths(package.replace('.', os.sep), "%s." % package)
        extpaths = extpaths.values()
        if extpaths and os.path.isdir(os.path.join(rootdir, '.git')): # We could be an unpacked sdist.
            check_ignore = subprocess.Popen(['git', 'check-ignore'] + [p.path for p in extpaths], cwd = rootdir, stdout = subprocess.PIPE)
            ignoredpaths = set(check_ignore.communicate()[0].decode().splitlines())
            assert check_ignore.wait() in [0, 1]
            self.extpaths = [path for path in extpaths if path.path not in ignoredpaths]
        else:
            self.extpaths = extpaths

# Copyright 2013, 2014, 2015, 2016, 2017, 2020, 2022 Andrzej Cichocki

# This file is part of pyven.
#
# pyven is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyven is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyven.  If not, see <http://www.gnu.org/licenses/>.

def lazy(clazz, init, *initbefore):
    from threading import Lock
    initlock = Lock()
    init = [init]
    def overridefactory(name):
        orig = getattr(clazz, name)
        def override(*args, **kwargs):
            with initlock:
                if init:
                    init[0](obj)
                    del init[:]
            return orig(*args, **kwargs)
        return override
    Lazy = type('Lazy', (clazz, object), {name: overridefactory(name) for name in initbefore})
    obj = Lazy()
    return obj

# FIXME: The idea was to defer anything Cython/numpy to pyximport time, but this doesn't achieve that.
def cythonize(extensions):
    def init(ext_modules):
        ordinary = []
        cythonizable = []
        for e in extensions:
            (cythonizable if any(s.endswith('.pyx') for s in e.sources) else ordinary).append(e)
        if cythonizable:
            from Cython.Build import cythonize
            ordinary += cythonize(cythonizable)
        ext_modules[:] = ordinary
    return lazy(list, init, '__getitem__', '__iter__', '__len__')

def ext_modules():
    extensions = [path.make_ext() for path in sourceinfo.extpaths]
    return dict(ext_modules = cythonize(extensions)) if extensions else {}

sourceinfo = SourceInfo('.')
setuptools.setup(
        name = 'Leytonium',
        version = '10',
        description = 'Tools for developing git-managed software',
        long_description = long_description(),
        long_description_content_type = 'text/markdown',
        url = 'https://github.com/combatopera/Leytonium',
        author = 'Andrzej Cichocki',
        packages = sourceinfo.packages,
        py_modules = [],
        install_requires = ['aridity>=62', 'autopep8>=1.5.4', 'awscli>=1.19.53', 'docutils>=0.15.2', 'importlib-metadata>=2.1.1', 'lagoon>=24', 'PyGObject>=3.42.2', 'pytz>=2020.4', 'pyven>=90', 'PyYAML>=5.2', 'setuptools>=44.1.1', 'termcolor>=1.1.0', 'Unidecode>=1.3.2'],
        package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld', '*.arid', '*.aridt', '*.bash']},
        scripts = [],
        entry_points = {'console_scripts': ['diffuse=diffuse.diffuse:main', 'abandon=leytonium.abandon:main', 'agi=leytonium.agi:main', 'agil=leytonium.agil:main', 'autopull=leytonium.autopull:main', 'awslogs=leytonium.awslogs:main', 'bashrc=leytonium.bashrc:main', 'br=leytonium.br:main', 'brown=leytonium.brown:main', 'ci=leytonium.ci:main', 'co=leytonium.co:main', 'd=leytonium.d:main', 'dp=leytonium.dp:main', 'drclean=leytonium.drclean:main', 'drop=leytonium.drop:main', 'drst=leytonium.drst:main', 'dup=leytonium.dup:main', 'dx=leytonium.dx:main', 'dxx=leytonium.dxx:main', 'eb=leytonium.eb:main', 'encrypt=leytonium.encrypt:main', 'examine=leytonium.examine:main', 'extractaudio=leytonium.extractaudio:main', 'fetchall=leytonium.fetchall:main', 'fixemails=leytonium.fixemails:main', 'gag=leytonium.gag:main', 'gimports=leytonium.gimports:main', 'git-completion-path=leytonium.git_completion_path:main', 'git-functions-path=leytonium.git_functions_path:main', 'gt=leytonium.gt:main', 'halp=leytonium.halp:main', 'hgcommit=leytonium.hgcommit:main', 'insertshlvl=leytonium.insertshlvl:main', 'isotime=leytonium.isotime:main', 'ks=leytonium.ks:main', 'mdview=leytonium.mdview:main', 'multimerge=leytonium.multimerge:main', 'n=leytonium.n:main', 'next=leytonium.next:main', 'pb=leytonium.pb:main', 'pd=leytonium.pd:main', 'prepare=leytonium.prepare:main', 'publish=leytonium.publish:main', 'pullall=leytonium.pullall:main', 'pushall=leytonium.pushall:main', 'rd=leytonium.rd:main', 'rdx=leytonium.rdx:main', 'readjust=leytonium.readjust:main', 'reks=leytonium.reks:main', 'ren=leytonium.ren:main', 'resimp=leytonium.resimp:main', 'rol=leytonium.rol:main', 'rx=leytonium.rx:main', 'scrape85=leytonium.scrape85:main', 'scrub=leytonium.scrub:main', 'setparent=leytonium.setparent:main', 'shove=leytonium.shove:main', 'show=leytonium.show:main', 'showstash=leytonium.showstash:main', 'slam=leytonium.slam:main', 'spamtrash=leytonium.spamtrash:main', 'splitpkgs=leytonium.splitpkgs:main', 'squash=leytonium.squash:main', 'st=leytonium.st:main', 'stacks=leytonium.stacks:main', 'stmulti=leytonium.stmulti:main', 't=leytonium.t:main', 'taskding=leytonium.taskding:main', 'tempvenv=leytonium.tempvenv:main', 'touchb=leytonium.touchb:main', 'unpub=leytonium.unpub:main', 'unslam=leytonium.unslam:main', 'upgrade=leytonium.upgrade:main', 'vpn=leytonium.vpn:main', 'vunzip=leytonium.vunzip:main', 'watchdesk=leytonium.watchdesk:main']},
        **ext_modules())
