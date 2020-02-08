import os
import socket

from mock import mock

from pyngrok import ngrok, installer
from pyngrok.exception import PyngrokNgrokInstallError
from .testcase import NgrokTestCase

__author__ = "Alex Laird"
__copyright__ = "Copyright 2020, Alex Laird"
__version__ = "2.0.2"


class TestInstaller(NgrokTestCase):
    def test_installer(self):
        # GIVEN
        if os.path.exists(ngrok.DEFAULT_NGROK_PATH):
            os.remove(ngrok.DEFAULT_NGROK_PATH)
        self.assertFalse(os.path.exists(ngrok.DEFAULT_NGROK_PATH))

        # WHEN
        ngrok.connect(config_path=self.config_path)

        # THEN
        self.assertTrue(os.path.exists(ngrok.DEFAULT_NGROK_PATH))

    def test_config_provisioned(self):
        # GIVEN
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        self.assertFalse(os.path.exists(self.config_path))

        # WHEN
        ngrok.connect(config_path=self.config_path)

        # THEN
        self.assertTrue(os.path.exists(self.config_path))

    @mock.patch("pyngrok.installer.urlopen")
    def test_installer_download_fails(self, mock_urlopen):
        # GIVEN
        magic_mock = mock.MagicMock()
        magic_mock.getcode.return_value = 500
        mock_urlopen.return_value = magic_mock

        if os.path.exists(ngrok.DEFAULT_NGROK_PATH):
            os.remove(ngrok.DEFAULT_NGROK_PATH)
        self.assertFalse(os.path.exists(ngrok.DEFAULT_NGROK_PATH))

        # WHEN
        with self.assertRaises(PyngrokNgrokInstallError):
            ngrok.connect(config_path=self.config_path)

        # THEN
        self.assertFalse(os.path.exists(ngrok.DEFAULT_NGROK_PATH))

    @mock.patch("pyngrok.installer.urlopen")
    def test_installer_retry(self, mock_urlopen):
        # GIVEN
        installer.DEFAULT_RETRY_COUNT = 1
        mock_urlopen.side_effect = socket.timeout("The read operation timed out")

        if os.path.exists(ngrok.DEFAULT_NGROK_PATH):
            os.remove(ngrok.DEFAULT_NGROK_PATH)
        self.assertFalse(os.path.exists(ngrok.DEFAULT_NGROK_PATH))

        # WHEN
        with self.assertRaises(PyngrokNgrokInstallError):
            ngrok.connect(config_path=self.config_path)

        # THEN
        self.assertEqual(mock_urlopen.call_count, 2)
        self.assertFalse(os.path.exists(ngrok.DEFAULT_NGROK_PATH))
