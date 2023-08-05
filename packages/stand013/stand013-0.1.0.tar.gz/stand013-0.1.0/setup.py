# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['stand013']

package_data = \
{'': ['*'], 'stand013': ['schemas/*']}

install_requires = \
['lxml>=4.6.3,<5.0.0', 'typer>=0.3.2,<0.4.0', 'xmlschema>=1.6.4,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6,<5.0']}

entry_points = \
{'console_scripts': ['stand013 = stand013.cli:app']}

setup_kwargs = {
    'name': 'stand013',
    'version': '0.1.0',
    'description': 'STAND13 file format parsing, writing, and validation.',
    'long_description': '# python-stand013\n\npython-stand013 is a Python app and library for parsing, writing, and validation\nof the [STAND013](https://stand.no/) file format.\n\n## Features\n\nThe following is a list of python-stand013\'s existing and planned features.\n\n- Validation\n  - [x] `ORDERS` purchase orders\n  - [x] `ORDRSP` purchase order responses\n  - [x] `DESADV` delivery notes\n- Parsing\n  - [ ] `ORDERS` purchase orders\n  - [ ] `ORDRSP` purchase order responses\n  - [ ] `DESADV` delivery notes\n- Writing\n  - [ ] `ORDERS` purchase orders\n  - [ ] `ORDRSP` purchase order responses\n  - [ ] `DESADV` delivery notes\n\n## Installation\n\npython-stand013 requires Python 3.7 or newer. It can be installed from PyPI using e.g. pip:\n\n```\npython3 -m pip install stand013\n```\n\n## Usage as command line tool\n\nThe `stand013` executable can be used to validate ORDERS, ORDRSP, and DESADV\nfiles. The file type to validate is automatically detected.\n\nExample of successful validation:\n\n```\n❯ stand013 validate tests/examples/ordrsp.xml\nFile: tests/examples/ordrsp.xml\nDocument type: ORDRSP\nXML Schema validation: passed\n❯\n```\n\nExample of unrecognized file format:\n\n```\n❯ stand013 validate /etc/passwd\nFile: /etc/passwd\nDocument type: Failed to detect\n❯\n```\n\nExample of invalid file:\n\n```\n❯ stand013 validate DESADV-failing.xml\nFile: DESADV-failing.xml\nDocument type: DESADV\nXML Schema validation: failed\n\n  failed validating {} with XsdAttributeGroup([\'MessageOwner\', \'MessageType\', \'MessageVersion\']):\n\n  Reason: missing required attribute \'MessageOwner\'\n\n  Schema:\n\n    <xsd:complexType xmlns:xsd="http://www.w3.org/2001/XMLSchema" name="DeliveryNoteType">\n      <xsd:sequence>\n        <xsd:element name="MessageNumber" type="xsd:string" minOccurs="0">\n          <xsd:annotation>\n            <xsd:documentation>Unikt nr som identifiserer meldingen innenfor en utveksling</xsd:documentation>\n          </xsd:annotation>\n        </xsd:element>\n        <xsd:element name="MessageTimestamp" type="xsd:dateTime">\n          <xsd:annotation>\n            <xsd:documentation>Meldingens dato (YYYY-MM-DDTHH:MM:SS) Sendetidspunkt</xsd:documentation>\n          </xsd:annotation>\n        </xsd:element>\n        <xsd:element name="DeliveryNoteHeader" type="DeliveryNoteHeaderType">\n          <xsd:annotation>\n            <xsd:documentation>Pakkseddel hode</xsd:documentation>\n          </xsd:annotation>\n        </xsd:element>\n        <xsd:element name="DeliveryNoteDetails" type="DeliveryNoteDetailsType" maxOccurs="unbounded">\n          <xsd:annotation>\n            <xsd:documentation>Pakkseddel detaljer</xsd:documentation>\n      ...\n      ...\n    </xsd:complexType>\n\n  Instance:\n\n    <DeliveryNote xmlns="http://www.ean-nor.no/schemas/eannor">\n      <MessageOwner>GS1NOR</MessageOwner>\n      <MessageType>DELIVERYNOTE</MessageType>\n      <MessageVersion>STAND013 v.1.0</MessageVersion>\n      <MessageTimestamp>2021-05-31T09:49:00</MessageTimestamp>\n      ...\n      ...\n    </DeliveryNote>\n\n  Path: /Interchange/DeliveryNote\n\n❯\n```\n\n## Usage as library\n\nTODO: Pending support for parsing and writing STAND013 files.\n\n## XML schema changes\n\nThe bundled XML schemas in `src/stand013/schemas/` have been retrieved from\nhttps://stand.no/en/home/downloads/. We\'re currently including the May 2020\nrevision of the XML schemas.\n\nWe\'ve done the following changes to the XML schemas to make them work for our use case.\n\n- Commit 7bdb761d378a4ec2922a1ea14048b614e4cd08e1: Fix references to the\n  `STAND013-Components_v1p1.xsd` file. This file is in the same directory as the\n  other schemas, not in `../Components/`. This is true both for the Zip file at stand.no and in python-stand013.\n\n- Commit bd9e138ac6275ccabe7ce0907157a3a83d0b5ea1: Renamed\n  `STAND013 DeliveryNote_v1p1.xsd` to `STAND013-DeliveryNote_v1p1.xsd` so that\n  the reference from `STAND013-DeliveryNote_Interchange_v1p1.xsd` works, and the\n  file name matches the other XML schemas.\n\n- Commit 955dfb86974d78f64d4da1dfdc72b0e27897a2a4: Change type for `ORDERS`\'\n  `Interchange/Order/OrderHeader/OrderResponse` from `MessageResponseType` (an\n  enum with the values `AC`, `AE`, or `NE`) to a new `OrderResponseType` enum\n  with `Z1` as the only possible value. This matches the format documentation,\n  and is necessary to be able to validate any `ORDERS` using the XML schemas.\n',
    'author': 'Stein Magnus Jodal',
    'author_email': 'stein.magnus.jodal@oda.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kolonialno/python-stand013',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
