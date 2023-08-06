# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asklora', 'asklora.brokerage', 'asklora.exceptions', 'asklora.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic-xml[lxml]==0.6.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'python-gnupg>=0.5.0,<0.6.0',
 'requests>=2.28.1,<3.0.0',
 'sseclient-py>=1.7.2,<2.0.0',
 'structlog>=22.3.0,<23.0.0']

setup_kwargs = {
    'name': 'asklora-portal',
    'version': '1.1.10',
    'description': 'portal to use various api data service',
    'long_description': '# Asklora Portal\n\nShared utilities and helper classes used in Asklora projects\n\n## Contents\n\n1. Clients for external services (MarketData, Broker, PriceData, DAMECAClient, DAMFBClient) and their supporting classes (DAM, pydantic models for xml serialising and de-serialising)\n2. Helper classes (SingletonMeta, ExtendedEnum, PGPHelper)\n3. Helper functions (deep_get, get_file_size, get_file_sha1)\n\n## Information on specific sections\n\n### Broker, PriceData and MarketData client\n\n#### required .env config when importing these\n\n- `BROKER_API_URL=brokerurl`\n- `MARKET_API_URL=market url`\n- `BROKER_KEY=key`\n- `BROKER_SECRET=secret`\n\n#### usage\n\n```python\nfrom asklora import Broker\n\nbroker = Broker()\nbroker.create_account(...)\n```\n\nor you can use our Portal class to get the specific model\n\n```python\nimport asklora\n\nportal = asklora.Portal()\n\nrest = portal.get_broker_client() # get a REST client for trade, user, position , order\nmarketrest = portal.get_market_client() # get a REST client for market data\neventclient = portal.get_event_client() # get an event client for trade, user, position, order\n```\n\n### PriceData (for IEX)\n\n#### required .env config\n\n- `IEX_API_URL`\n- `IEX_TOKEN`\n\n#### usage\n\n```python\nfrom asklora import PriceData\n\nprice_data = PriceData()\nprice_data.get_lastestPrice("MSFT")\n```\n\n### DAMECAClient and DAMFBClient\n\n#### required .env config\n\n- `DAM_URL`\n- `DAM_CSID`\n\n#### usage\n\nFor these clients, you can find the Pydantic models needed by some of the class methods in the `models` and `enums` module.\n\nfor example, in the `DAMECAClient`, in the `generate_application_payload` method, the first argument accepts `DAMApplicationPayload` model that will automatically processed to xml the API endpoint needs.\n\n### examples\n\n- DAMECAClient\n\n  ```python\n  from asklora import DAMECAClient, PGPHelper\n  from asklora.models import DAMApplicationPayload\n\n  client = DAMECAClient()\n\n  # Build payload\n  payload = DAMApplicationPayload(\n      user_id=56,\n      first_name="Jane",\n      last_name="Smith",\n      ...\n  )\n\n  # Needed for encryption\n  pgp_helper = PGPHelper(\n      private_key_path=...,\n      public_key_path=...,\n      remote_public_key_path=...,\n  )\n\n  # Send the request\n  client.create_account(payload, pgp_helper=pgp_helper)\n  ```\n\n- DAMFBClient\n\n  ```python\n  from asklora import DAMFBClient, PGPHelper\n  from asklora.models import InstructionSet, InternalCashTransfer, CancelTransaction\n\n  client = DAMFBClient()\n\n  instruction_set = InstructionSet(\n      instructions=[\n          InternalCashTransfer(\n             id=4,\n             source="U199516",\n             destination="U34516",\n             amount=1000,\n             currency="USD",\n          ),\n          CancelTransaction(\n             id=5,\n             ib_instr_id="3",\n             reason="Wrong destination",\n          ),\n      ]\n  )\n  pgp_helper = PGPHelper(\n      private_key_path=...,\n      public_key_path=...,\n      remote_public_key_path=...,\n  )\n\n  client.create_instruction(instruction_set, pgp_helper=pgp_helper)\n\n  # if needed, you can also send xml directly\n  payload = """<?xml version="1.0" encoding="UTF-8"?>\n  <instruction_set\n    xmlns="http://www.interactivebrokers.com/fbfb_instruction_set"\n    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n    xsi:schemaLocation="http://www.interactivebrokers.com/fbfb_instruction_set fbfb_instruction_set.xsd "\n    creation_date="2019-01-11" id="2450" version="1">\n    <close_account id="2450">\n        <client_ib_acct_id>U1234567</client_ib_acct_id>\n        <close_reason> No longer needed </close_reason>\n    </close_account>\n  </instruction_set>"""\n\n  client.create_instruction(payload, pgp_helper=pgp_helper)\n  ```\n\n- Both\n\n  You can also initialise one or both of the classes above like this:\n\n  ```python\n  from asklora import IBClient\n\n  eca_client = IBClient.get_ECA_client()\n  fb_client = IBClient.get_FB_client()\n  ```\n',
    'author': 'redloratech',
    'author_email': 'rede.akbar@loratechai.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
