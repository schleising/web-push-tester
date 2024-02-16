This script sends a push notification to push subscriptions in a MongoDB database

!!! Example
    To send a push notification with the title "Test", message "This is a test" and urgency "normal" run the following command:
    
    ```bash
    $ python main.py --title "Test" --message "This is a test" --ttl 3600 --urgency "normal"
    ```

## Command line arguments

The following command line arguments are available:

Option|Short Option|Description
-|-|-
`--title`|`-t`|The title of the push notification
`--message`|`-m`|The message of the push notification
`--ttl`|`-l`|The time to live of the push notification
`--urgency`|`-u`|The urgency of the push notification
`--require-interaction`|`-r`|Whether the push notification requires interaction
`--push_data_file`|`-p`|The file containing the push data, badge, icon and url

## File formats and database model

### Generating the public and private key

!!! Example
    To generate the public and private key run the following command:

    ```bash
    $ vapid --gen
    ```

    To get the Application Server Key (VAPID public key) run the following command:

    ```bash
    $ vapid --applicationServerKey
    ```

The public and private key should be stored in the `secrets` directory with the following names:

- `public_key.pem`
- `private_key.pem`

The private key should be kept secret and the Application Server Key (VAPID public key) should be used in the frontend.

The Application Server Key is the encoded version of the public key in `public_key.pem` in URL safe base64 format, this can be used in the frontend to subscribe to push notifications using the following JavaScript code:

!!! Example
    ```javascript
    navigator.serviceWorker.ready.then(function(registration) {
        return registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array(applicationServerKey)
        });
    }).then(function(subscription) {
        // Send the subscription to the server to store it in the database
    });

    // Function to convert base64 string to Uint8Array
    function urlBase64ToUint8Array(base64String) {
        var padding = '='.repeat((4 - base64String.length % 4) % 4);
        var base64 = (base64String + padding)
            .replace(/\-/g, '+')
            .replace(/_/g, '/');

        var rawData = window.atob(base64);
        var outputArray = new Uint8Array(rawData.length);

        for (var i = 0; i < rawData.length; i++) {
            outputArray[i] = rawData.charCodeAt(i);
        }

        return outputArray;
    }
    ```

`db_info.json`

```json
{
    "host": "localhost",
    "port": 27017,
    "connection_timeout": 1000,
    "database": "database",
    "collection": "collection",
}
```

`claims.json`

```json
{
    "sub": "mailto:mail@example.com",
}
```

Database model for the Subscriptions:

```json
{
    "endpoint": "https://fcm.googleapis.com/fcm/send/...",
    "expirationTime": null,
    "keys": {
        "p256dh": "key",
        "auth": "key"
    }
}
```
