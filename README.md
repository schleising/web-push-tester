# Web Push Tester
This is a simple web push notification tester

## How to use
1. Clone the repository
2. Install the dependencies
3. Add the following files to the secrets folder:
    - `private_key.pem`: The private key for the VAPID keys
    - `public_key.pem`: The public key for the VAPID keys
    - `claims.json`: The claims for the VAPID keys
    - `db_info.json`: The database information
4. Run the following command to send a push notification:
    ```bash
    python3 main.py --title "Title" --message "Message" --urgency "normal"
    ```

## Command line arguments

The following command line arguments are available:

Option|Short Option|Description
-|-|-
`--title`|`-t`|The title of the push notification
`--message`|`-m`|The message of the push notification
`--urgency`|`-u`|The urgency of the push notification

## Documentation
The documentation for this project can be found [here](https://schleising.github.io/web-push-tester/)
