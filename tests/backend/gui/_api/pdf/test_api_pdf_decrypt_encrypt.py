# tests\backend\gui\_api\pdf\test_api_pdf_decrypt_encrypt.py

import platform
import pytest

from pathlib import Path


# user-provided imports
from file_conversor.backend.pdf import PyPDFBackend

from file_conversor.backend.gui._api.pdf.decrypt import api_pdf_decrypt, EXTERNAL_DEPENDENCIES
from file_conversor.backend.gui._api.pdf.encrypt import api_pdf_encrypt

from file_conversor.backend.gui import FlaskApiStatus, FlaskRoute

from tests.utils import Test, DATA_PATH, app_cmd


@pytest.mark.skipif(not Test.dependencies_installed(EXTERNAL_DEPENDENCIES), reason="External dependencies not installed")
class TestAPIPdfDecryptEncrypt:
    def test_decrypt_encrypt(self, tmp_path: Path):
        input_file = DATA_PATH / "test.pdf"
        enc_file = tmp_path / "test_encrypted.pdf"
        output_file = enc_file.with_name("test_encrypted_decrypted.pdf")
        password = "1234"

        url = FlaskRoute.get_url(api_pdf_encrypt)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(input_file),
            ]),
            "output-dir": str(tmp_path.resolve()),

            'pdf-encryption-algorithm': PyPDFBackend.EncryptionAlgorithm.AES_256.value,
            'decrypt-password': "null",
            'owner-password': password,
            'user-password': "null",

            'annotate': "off",
            'fill_forms': "off",
            'modify': "off",
            'modify_pages': "off",
            'copy': "off",
            'accessibility': "off",
            'print_lq': "off",
            'print_hq': "off",

            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert enc_file.exists()

        url = FlaskRoute.get_url(api_pdf_decrypt)
        reply = Test.flask_api(url, data={
            "input-files": str([
                str(enc_file),
            ]),
            "output-dir": str(tmp_path.resolve()),
            "password": password,
            "overwrite-output": "true",
        })
        status = Test.flask_api_status(FlaskApiStatus(**reply))
        assert output_file.exists()
