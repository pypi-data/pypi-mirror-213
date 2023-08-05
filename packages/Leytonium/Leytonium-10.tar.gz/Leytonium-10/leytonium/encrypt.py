# Copyright 2020 Andrzej Cichocki

# This file is part of Leytonium.
#
# Leytonium is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Leytonium is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Leytonium.  If not, see <http://www.gnu.org/licenses/>.

'Encrypt a secret using gpg for use in aridity config.'
from . import initlogging
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from base64 import b64encode
from lagoon.binary import gpg
from socket import gethostname
import logging

log = logging.getLogger(__name__)

def main():
    initlogging()
    config = ConfigCtrl().loadappconfig(main, 'encrypt.arid')
    parser = ArgumentParser()
    parser.add_argument('-p', default = getattr(config.autoprofile, gethostname(), None))
    parser.add_argument('text')
    parser.parse_args(namespace = config.cli)
    profilekey = config.profilekey
    log.info("Profile: %s", profilekey)
    recipients = list(getattr(config.profile, profilekey).recipient)
    log.info("Recipients: %s", recipients)
    print(b64encode(gpg.__no_auto_key_locate.__encrypt(*sum((['--recipient', r] for r in recipients), []), input = config.text.encode('ascii'))).decode())

if '__main__' == __name__:
    main()
