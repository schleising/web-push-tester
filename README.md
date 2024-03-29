# Web Push Tester
This is a simple web push notification tester

You need to have your notification subscriptions in a Mongodb database. The database information is stored in the `db_info.json` file in the secrets folder.

## How to use
1. Clone the repository
2. Install the dependencies
3. Add the following files to the secrets folder:
    - `private_key.pem`: The private key for the VAPID keys
    - `public_key.pem`: The public key for the VAPID keys
    - `claims.json`: The claims for the VAPID keys
    - `db_info.json`: The database information
    - See the documentation for more information on the contents of these files
4. Run the following command to send a push notification:
    ```bash
    python3 main.py --title "Title" --message "Message" --ttl 3600 --urgency "normal"
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

## Documentation
The documentation for this project can be found [here](https://schleising.github.io/web-push-tester/)
