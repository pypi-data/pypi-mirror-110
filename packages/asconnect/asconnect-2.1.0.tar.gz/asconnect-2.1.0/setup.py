# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asconnect', 'asconnect.models']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=3.0.0,<4.0.0',
 'deserialize>=1.2.0,<2.0.0',
 'pyjwt>=1.7.0,<2.0.0',
 'requests>=2.20.0,<3.0.0',
 'tenacity>=6.2.0,<7.0.0']

setup_kwargs = {
    'name': 'asconnect',
    'version': '2.1.0',
    'description': 'A wrapper around the Apple App Store Connect APIs',
    'long_description': '# asconnect\n\nasconnect is a Python wrapper around the [Apple App Store Connect REST APIs](https://developer.apple.com/documentation/appstoreconnectapi).\n\nThis wrapper does not cover every API, but does cover the basics, including:\n\n* Uploading a build\n* Creating a new TestFlight version\n* Setting TestFlight review information\n* Creating a new app store version\n* Setting the app review information\n* Submitting for app review\n\n## Getting Started\n\n### Installation\n\nThe package is available on PyPI, so you can run `pip install asconnect` to get the latest version.\n\n### Creating a client\n\nTo begin, you need to [generate a key](https://developer.apple.com/documentation/appstoreconnectapi/creating_api_keys_for_app_store_connect_api), then get it\'s ID, the contents of the key itself, and the issuer ID.\n\nOnce you have those, you can create a new client by running:\n\n```python\nclient = asconnect.Client(key_id="...", key_contents="...", issuer_id="...")\n```\n\n### Getting your App\n\nMost operations require an app identifier. This is not the same as the bundle ID you choose, but is an ID generated by Apple. The easiest way to get this is to run this code:\n\n```python\napp = client.app.get_from_bundle_id("com.example.my_bundle_id")\n```\n\n### Uploading a Build\n\nUploading a build isn\'t technically part of the App Store Connect APIs, but a wrapper around altool is included to make things as easy as possible. Let\'s upload a build for your app:\n\n```python\nclient.build.upload(\n  ipa_path="/path/to/the/app.ipa",\n  platform=asconnect.Platform.ios,\n)\n```\n\nAnd if you want to wait for your build to finish processing:\n\n```python\nbuild = client.build.wait_for_build_to_process("com.example.my_bundle_id", build_number)\n```\n\n`build_number` is the build number you gave your build when you created it. It\'s used by the app store to identify the build.\n\n### App Store Submission\n\nLet\'s take that build, create a new app store version and submit it,\n\n```python\n# Create a new version\nversion = client.app.create_new_version(version="1.2.3", app_id=app.identifier)\n\n# Set the build for that version\nclient.version.set_build(version_id=version.identifier, build_id=build.identifier)\n\n# Submit for review\nclient.version.submit_for_review(version_id=version.identifier)\n```\n\nIt\'s that easy. Most of the time at least. If you don\'t have previous version to inherit information from you\'ll need to do things like set screenshots, reviewer info, etc. All of which is possible through this library.\n### Phased Distribution\n```python\n# Create a new version\nversion = client.app.create_new_version(version="1.2.3", app_id=app.identifier)\n\n# Start a versions\' phased release, the initial state of which is INACTIVE\nphased_release = client.version.create_phased_release(version_id=version.identifier)\n\n# Check on a phased release\nphased_release = client.version.get_phased_release(version_id=version.identifier)\n\n# Advance or modify a phased release\nphased_release = client.version.patch_phased_release(phased_release_id=phased_release.identifier, phased_release_state=PhasedReleaseState.active)\nphased_release = client.version.patch_phased_release(phased_release_id=phased_release.identifier, phased_release_state=PhasedReleaseState.pause)\nphased_release = client.version.patch_phased_release(phased_release_id=phased_release.identifier, phased_release_state=PhasedReleaseState.complete)\n\n# Delete\nclient.version.delete_phased_release(phased_release_id=phased_release.identifier)\n```\n# Getting Started\n\nFor development `asconnect` uses [`poetry`](https://github.com/python-poetry/poetry)\n\n# Contributing\n\nThis project welcomes contributions and suggestions.  Most contributions require you to agree to a\nContributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us\nthe rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.\n\nWhen you submit a pull request, a CLA bot will automatically determine whether you need to provide\na CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions\nprovided by the bot. You will only need to do this once across all repos using our CLA.\n\nThis project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).\nFor more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or\ncontact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.\n',
    'author': 'Dale Myers',
    'author_email': 'dalemy@microsoft.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/microsoft/asconnect',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
