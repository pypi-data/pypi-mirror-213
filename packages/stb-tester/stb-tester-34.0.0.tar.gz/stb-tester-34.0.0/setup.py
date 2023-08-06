# coding: utf-8

import setuptools


long_description = """\
# Stb-tester

**Automated User Interface Testing for Set-Top Boxes & Smart TVs**

Copyright © 2018-2023 Stb-tester.com Ltd. All rights reserved.

This package contains the "stbt" Python APIs that you can use in test-scripts
written for running on the [Stb-tester Platform]. The primary purpose of this
package is to make the stbt library easy to install locally for IDE linting &
autocompletion.

This package doesn't support video-capture, so `stbt.get_frame()` and
`stbt.frames()` won't work -- but you will be able to run `stbt.match()` if you
specify the `frame` parameter explicitly, for example by loading a screenshot
from disk with `stbt.load_image()`.

This package doesn't include remote-control integrations, so `stbt.press()` and
similar functions won't work.

This package doesn't bundle the Tesseract OCR engine, so `stbt.ocr()` and
`stbt.match_text()` won't work.

Premium (non-open source) APIs, such as `stbt.get_rms_volume()` and other
audio-related APIs, are included as stubs to support IDE linting &
autocompletion, but without a working implementation.

[Stb-tester Platform]: https://stb-tester.com
"""

setuptools.setup(
    name="stb-tester",
    version="34.0.0",
    author="Stb-tester.com Ltd.",
    author_email="support@stb-tester.com",
    description="Automated GUI testing for Set-Top Boxes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://stb-tester.com",
    packages=["stbt"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.10",
    install_requires=[
        "stbt_core~=34.0",
    ],
)
