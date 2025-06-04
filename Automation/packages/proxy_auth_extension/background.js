var config = {
    mode: "fixed_servers",
    rules: {
      singleProxy: {
        scheme: "http",
        host: "38.75.72.92",
        port: parseInt(29842)
      },
      bypassList: ["localhost"]
    }
  };
  
  chrome.proxy.settings.set({ value: config, scope: "regular" }, function () {});
  
  function callbackFn(details) {
    return {
      authCredentials: {
        username: "ehenry01",
        password: "HGFnbhgf"
      }
    };
  }
  
  chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    { urls: ["<all_urls>"] },
    ["blocking"]
  );
  