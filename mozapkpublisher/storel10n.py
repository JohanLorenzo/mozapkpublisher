from mozapkpublisher.utils import load_json_url


class StoreL10n(object):
    """ Manage the localization of the Google play store
    """

    l10n_api_url = "https://l10n.mozilla-community.org/stores_l10n/"
    all_locales_url = l10n_api_url + "api/google/listing/{channel}/"
    locale_url = l10n_api_url + "api/google/translation/{channel}/{locale}/"
    mapping_url = l10n_api_url + "api/google/localesmapping/?reverse"

    def __init__(self):
        self.mappings = []

    def get_list_locales(self, package_name):
        """ Get all the translated locales supported by Google play
        So, locale unsupported by Google play won't be downloaded
        Idem for not translated locale
        """
        return load_json_url(self.all_locales_url.format(channel=package_name))

    def get_translation(self, package_name, locale):
        """ Get the translation for a locale
        """
        return load_json_url(self.locale_url.format(channel=package_name, locale=locale))

    def load_mapping(self):
        """ Download and load the locale mapping
        """
        self.mappings = load_json_url(self.mapping_url)

    def locale_mapping(self, locale):
        """ Google play and Mozilla don't have the exact locale code
        Translate them
        """
        if locale in self.mappings:
            return self.mappings[locale]
        else:
            return locale
