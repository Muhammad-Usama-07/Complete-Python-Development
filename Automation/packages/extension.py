import os

def add_proxy(endpoint, port, username, password):
    folder_name = os.path.join(os.path.dirname(__file__), '..', 'proxies', username)

    # manifest_json = '''
    #     {
    #         "version": "1.0.0",
    #         "manifest_version": 2,
    #         "name": "Proxy Auth Extension",
    #         "permissions": [
    #         "proxy",
    #         "tabs",
    #         "unlimitedStorage",
    #         "storage",
    #         "<all_urls>",
    #         "webRequest",
    #         "webRequestBlocking"
    #         ],
    #         "background": {
    #         "scripts": ["background.js"]
    #         },
    #         "minimum_chrome_version": "22.0.0"
    #     }
    # '''
    manifest_json = '''
        {
        "version": "1.0.0",
        "manifest_version": 3,
        "name": "Proxy Auth Extension",
        "permissions": [
            "proxy",
            "storage",
            "webRequest",
            "webRequestAuthProvider"
        ],
        "background": {
            "service_worker": "background.js"
        },
        "host_permissions": ["<all_urls>"]
    }
    '''


    # background_js = """
    #     var config = {
    #         mode: "fixed_servers",
    #         rules: {
    #         singleProxy: {
    #             scheme: "http",
    #             host: "%s",
    #             port: parseInt(%s)
    #         },
    #         bypassList: ["localhost"]
    #         }
    #     };
        
    #     chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        
    #     function callbackFn(details) {
    #         return {
    #         authCredentials: {
    #             username: "%s",
    #             password: "%s"
    #         }
    #         };
    #     }
        
    #     chrome.webRequest.onAuthRequired.addListener(
    #         callbackFn,
    #         { urls: ["<all_urls>"] },
    #         ["blocking"]
    #     );
    
    # """ % (endpoint, port, username, password)
    background_js = """
    chrome.runtime.onInstalled.addListener(() => {
        let config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
            }
        };

        chrome.proxy.settings.set({ value: config, scope: "regular" }, function() {
            console.log("Proxy settings applied");
        });
    });

    chrome.webRequest.onAuthRequired.addListener(
        (details) => {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        },
        { urls: ["<all_urls>"] },
        ["blocking"]
    );
    """ % (endpoint, port, username, password)

    

    os.makedirs(folder_name, exist_ok=True)
    print('proxie folder created ------------------')

    # Write the contents to the respective files 
    with open(os.path.join(folder_name, 'manifest.json'), 'w') as file:
        file.write(manifest_json)

    with open(os.path.join(folder_name, 'background.js'), 'w') as file:
        file.write(background_js)

    # print(f"Folder '{folder_name}' created with the required files.")
    absolute_path = os.path.abspath(folder_name)
    return absolute_path
