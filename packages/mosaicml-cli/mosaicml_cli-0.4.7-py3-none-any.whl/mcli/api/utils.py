"""
Utils for all api folders
"""

import logging
import os
import ssl

from mcli.utils.utils_logging import WARN, FormatString, format_string

logger = logging.getLogger(__name__)

LINK = 'https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate'


def check_python_certificates():
    certificates_exist = os.path.exists(ssl.get_default_verify_paths().openssl_cafile)
    if not certificates_exist:
        command = 'bash /Applications/Python*/Install\\ Certificates.command'
        command = format_string(command, FormatString.BLUE)
        message = ('Python SSL Certificates are not installed. '
                   'These are required to make HTTPs requests against MosaicML services.')
        message = format_string(message, FormatString.RED)
        link = format_string(LINK, FormatString.BLUE)
        logger.error(f'{message}\n\n{WARN}If you are on macOS, please run the '
                     f'following command to install them: \n{command}\n\n'
                     f'For other operating systems, please see: \n{link}')
