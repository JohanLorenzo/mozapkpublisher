import argparse
import json
import logging
import sys

from mozapkpublisher import googleplay, store_l10n
from mozapkpublisher.base import Base, ArgumentParser
from mozapkpublisher.exceptions import WrongArgumentGiven

logger = logging.getLogger(__name__)


class UpdateLocale(Base):
    def __init__(self, config=None):
        self.config = self._parse_config(config)

    @classmethod
    def _init_parser(cls):
        cls.parser = ArgumentParser(
            description="WIP",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        googleplay.add_general_google_play_arguments(cls.parser)

        cls.parser.add_argument('--locale', help='Locale to update')
        cls.parser.add_argument('--store_l10n_json', type=argparse.FileType(), help='file which contains the l10n json content', required=True)
        cls.parser.add_argument('version_codes', metavar='version code', help='Version codes to update', nargs='+')

    def run(self):
        edit_service = googleplay.EditService(
            self.config.service_account, self.config.google_play_credentials_file.name, self.config.package_name,
            self.config.dry_run
        )
        locale = self.config.locale
        whatsnew = json.load(self.config.store_l10n_json).get('whatsnew')

        for version_code in self.config.version_codes:
            edit_service.update_apk_listings(locale, version_code, body={'recentChanges': whatsnew})
            logger.info(u'Locale "{}" what\'s new has been updated to "{}"'.format(locale, whatsnew))

        edit_service.commit_transaction()


def main(name=None):
    if name not in ('__main__', None):
        return

    from mozapkpublisher import main_logging
    main_logging.init()

    try:
        UpdateLocale().run()
    except WrongArgumentGiven as e:
        UpdateLocale.parser.print_help(sys.stderr)
        sys.stderr.write('{}: error: {}\n'.format(UpdateLocale.parser.prog, e))
        sys.exit(2)

main(__name__)
