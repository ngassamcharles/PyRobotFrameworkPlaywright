import os

def get_browserstack_capabilities():
    username = os.environ.get('BROWSERSTACK_USERNAME')
    access_key = os.environ.get('BROWSERSTACK_ACCESS_KEY')
    browserstack_local = os.environ.get('BROWSERSTACK_LOCAL', 'false')
    browserstack_local_identifier = os.environ.get('BROWSERSTACK_LOCAL_IDENTIFIER', '')
    build_name = os.environ.get('BROWSERSTACK_BUILD_NAME', 'Robot Framework Playwright Build')
    build_number = os.environ.get('BROWSERSTACK_BUILD_NUMBER', '')

    # Configuration pour Playwright avec BrowserStack
    capabilities = {
        'browser': 'chrome',
        'browser_version': 'latest',
        'os': 'Windows',
        'os_version': '10',
        'name': 'BStack-[Robot Framework] Test',
        'build': build_name,
        'buildName': build_number,
        'browserstack.username': username,
        'browserstack.accessKey': access_key,
        'browserstack.local': browserstack_local,
        'browserstack.localIdentifier': browserstack_local_identifier
    }

    return capabilities
