import os
import shutil
from zipfile import ZipFile

import Utilities.constant as const


def unzip():
    try:
        with ZipFile('Resources\\Implant.zip') as zf:
            zf.extractall(pwd=b'LYy09s(yPdXc)')

        if os.path.exists("Implant"):
            shutil.move("Implant", "Resources\\Implant")

            const.success_message("Implant SourceCode Extracted")

        else:
            const.error_message("Error: During Implant SourceCode Extraction")

    except Exception as ex:
        const.error_exception("Error: ", ex)
