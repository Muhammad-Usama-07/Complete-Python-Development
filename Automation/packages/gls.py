# class GeolocationSpoofer:
#     def __init__(self, latitude, longitude, accuracy):
#         """
#         Initialize geolocation spoofing
        
#         Args:
#             latitude (float): Latitude to spoof
#             longitude (float): Longitude to spoof
#             accuracy (float): Location accuracy
#         """
#         self.latitude = latitude
#         self.longitude = longitude
#         self.accuracy = accuracy
        
#         # Comprehensive spoofing method
#         self.geolocation_script = f"""
#         // Advanced Geolocation Spoofing
#         (function() {{
#             // Deep object property overrides
#             const spoofedLocation = {{
#                 latitude: {latitude},
#                 longitude: {longitude},
#                 accuracy: {accuracy}
#             }};

#             // Multiple level of geolocation API manipulation
#             const originalGetCurrentPosition = navigator.geolocation.getCurrentPosition;
#             const originalWatchPosition = navigator.geolocation.watchPosition;

#             // Override getCurrentPosition
#             navigator.geolocation.getCurrentPosition = function(successCallback, errorCallback, options) {{
#                 const fakePosition = {{
#                     coords: {{
#                         latitude: spoofedLocation.latitude,
#                         longitude: spoofedLocation.longitude,
#                         accuracy: spoofedLocation.accuracy,
#                         altitude: null,
#                         altitudeAccuracy: null,
#                         heading: null,
#                         speed: null
#                     }},
#                     timestamp: Date.now()
#                 }};
                
#                 successCallback(fakePosition);
#             }};

#             // Override watchPosition
#             navigator.geolocation.watchPosition = function(successCallback, errorCallback, options) {{
#                 const fakePosition = {{
#                     coords: {{
#                         latitude: spoofedLocation.latitude,
#                         longitude: spoofedLocation.longitude,
#                         accuracy: spoofedLocation.accuracy,
#                         altitude: null,
#                         altitudeAccuracy: null,
#                         heading: null,
#                         speed: null
#                     }},
#                     timestamp: Date.now()
#                 }};
                
#                 successCallback(fakePosition);
#                 return 1; // Fake watch ID
#             }};

#             // Additional global property spoof
#             Object.defineProperty(window, 'latitude', {{
#                 value: {latitude},
#                 writable: false
#             }});
#             Object.defineProperty(window, 'longitude', {{
#                 value: {longitude},
#                 writable: false
#             }});

#             console.log('Geolocation spoofing activated');
#         }})();
#         """
    
#     def spoof_geolocation(self, driver):
#         """
#         Apply geolocation spoofing script to the provided driver
        
#         Args:
#             driver (uc.Chrome): The Chrome WebDriver instance
        
#         Returns:
#             uc.Chrome: The WebDriver with geolocation spoofing applied
#         """
#         # Inject geolocation spoofing script
#         driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
#             'source': self.geolocation_script
#         })
#         result = driver.execute_script('''
#             return new Promise((resolve) => {
#                 navigator.geolocation.getCurrentPosition(
#                     (position) => {
#                         resolve({
#                             latitude: position.coords.latitude,
#                             longitude: position.coords.longitude,
#                             accuracy: position.coords.accuracy,
#                             windowLatitude: window.latitude,
#                             windowLongitude: window.longitude
#                         });
#                     },
#                     (error) => {
#                         resolve({ error: error.message });
#                     }
#                 );
#             });
#             ''')
#         print('result: ', result)
#         return driver
    
    

       
    

# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# import time
# # Test script to execute the spoofing
# def test_geolocation_spoofer():
#     # Geolocation coordinates to spoof
#     latitude = 37.7749  # Example: San Francisco
#     longitude = -122.4194
#     accuracy = 1  # Accuracy in meters

#     # Initialize GeolocationSpoofer
#     spoofer = GeolocationSpoofer(latitude, longitude, accuracy)

#     # Setup undetected Chrome WebDriver
#     options = uc.ChromeOptions()
#     options.headless = False  # Set to True to run headlessly
#     driver = uc.Chrome(options=options)

#     # Apply geolocation spoofing
#     driver = spoofer.spoof_geolocation(driver)
#     # Navigate to a website that uses geolocation (for testing)
#     driver.get("https://www.google.com/maps")

#     # Wait to check the spoofed location
#     time.sleep(10)  # Adjust the sleep time as needed for observing behavior

#     # Close the browser after the test
#     driver.quit()

# # Run the test
# if __name__ == "__main__":
#     test_geolocation_spoofer()

import undetected_chromedriver as uc
import time

class GeolocationSpoofer:
    def __init__(self, latitude=21.4362544, longitude=39.6817383, accuracy=1):
        """
        Initialize geolocation spoofing
        
        Args:
            latitude (float): Latitude to spoof
            longitude (float): Longitude to spoof
            accuracy (float): Location accuracy
        """
        self.latitude = latitude
        self.longitude = longitude
        self.accuracy = accuracy
        
        # Comprehensive spoofing method
        self.geolocation_script = f"""
        // Advanced Geolocation Spoofing
        (function() {{
            // Deep object property overrides
            const spoofedLocation = {{
                latitude: {latitude},
                longitude: {longitude},
                accuracy: {accuracy}
            }}; 

            // Multiple level of geolocation API manipulation
            const originalGetCurrentPosition = navigator.geolocation.getCurrentPosition;
            const originalWatchPosition = navigator.geolocation.watchPosition;

            // Override getCurrentPosition
            navigator.geolocation.getCurrentPosition = function(successCallback, errorCallback, options) {{
                const fakePosition = {{
                    coords: {{
                        latitude: spoofedLocation.latitude,
                        longitude: spoofedLocation.longitude,
                        accuracy: spoofedLocation.accuracy,
                        altitude: null,
                        altitudeAccuracy: null,
                        heading: null,
                        speed: null
                    }},
                    timestamp: Date.now()
                }};
                
                successCallback(fakePosition);
            }};

            // Override watchPosition
            navigator.geolocation.watchPosition = function(successCallback, errorCallback, options) {{
                const fakePosition = {{
                    coords: {{
                        latitude: spoofedLocation.latitude,
                        longitude: spoofedLocation.longitude,
                        accuracy: spoofedLocation.accuracy,
                        altitude: null,
                        altitudeAccuracy: null,
                        heading: null,
                        speed: null
                    }},
                    timestamp: Date.now()
                }};
                
                successCallback(fakePosition);
                return 1; // Fake watch ID
            }};

            // Additional global property spoof
            Object.defineProperty(window, 'latitude', {{
                value: {latitude},
                writable: false
            }});
            Object.defineProperty(window, 'longitude', {{
                value: {longitude},
                writable: false
            }});

            console.log('Geolocation spoofing activated');
        }})();
        """
        
    def spoof_geolocation(self, driver):
        """
        Apply geolocation spoofing script to the provided driver
        
        Args:
            driver (uc.Chrome): The Chrome WebDriver instance
        
        Returns:
            uc.Chrome: The WebDriver with geolocation spoofing applied
        """
        # Inject geolocation spoofing script
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': self.geolocation_script
        })
        # print('--- spoof_geolocation: ')
        return driver
    
    def create_driver(self):
        """
        Create undetected chrome driver with geolocation spoofing
        
        Returns:
            uc.Chrome: Configured WebDriver
        """
        # Chrome options
        options = uc.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Create driver
        driver = uc.Chrome(options=options)
        
        # Inject geolocation spoofing script
        self.spoof_geolocation(driver)
        
        return driver

    def test_geolocation(self):
        """
        Test geolocation spoofing
        
        This will automatically trigger the geolocation spoofing as soon as the page loads.
        """
        # Create driver
        driver = self.create_driver()
        
        try:
            # Load a blank page or any page that doesn't request geolocation
            driver.get('about:blank')  # You can load any page here
            
            # Inject code to request geolocation immediately after the page loads
            driver.execute_script("""
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        console.log('Geolocation accessed:', position.coords.latitude, position.coords.longitude);
                    }, 
                    function(error) {
                        console.log('Geolocation error:', error);
                    }
                );
            """)
            
            # Wait for geolocation request to be processed
            time.sleep(3)
            
            # Verify geolocation
            result = driver.execute_script(''' 
            return new Promise((resolve) => {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        resolve({
                            latitude: position.coords.latitude,
                            longitude: position.coords.longitude,
                            accuracy: position.coords.accuracy,
                            windowLatitude: window.latitude,
                            windowLongitude: window.longitude
                        });
                    },
                    (error) => {
                        resolve({ error: error.message });
                    }
                );
            });
            ''')
            
            # print("Spoofed Geolocation Results:")
            # print(result)
            driver.get('https://www.google.com/maps')  # You can load any page here
            
            # Keep browser open for inspection
            input("Press Enter to close the browser...")
        
        finally:
            # Close the browser
            driver.quit()

# Usage example
def main():
    # New York City coordinates
    spoofer = GeolocationSpoofer(
        latitude = 40.7301, 
        longitude = -74.0060
    )
    
    # Test geolocation spoofing
    spoofer.test_geolocation()

if __name__ == '__main__':
    main()
