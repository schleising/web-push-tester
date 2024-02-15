"""Send a push notification to the push subscriptions

This script sends a push notification to the push subscriptions in the database

Example:
    To send a push notification with the title "Test", message "This is a test" and urgency "normal" run the following command:
    
            $ python main.py --title "Test" --message "This is a test" --urgency "normal"

## Command line arguments

The following command line arguments are available:

Option|Short Option|Description
-|-|-
`--title`|`-t`|The title of the push notification
`--message`|`-m`|The message of the push notification
`--urgency`|`-u`|The urgency of the push notification
"""

from datetime import datetime
import json
from typing import Annotated

import typer
from rich import print
from pydantic import BaseModel
from pymongo import MongoClient
from pywebpush import webpush, WebPushException
from requests import Response


class DbInfo(BaseModel):
    """Information about the database

    Attributes:
        host (str): The host of the database
        port (int): The port of the database
        connection_timeout (int): The connection timeout of the database
        database (str): The name of the database
        collection (str): The name of the collection
    """

    host: str
    port: int
    connection_timeout: int
    database: str
    collection: str


class Keys(BaseModel):
    """Keys for a push subscription

    Attributes:
        p256dh (str): The p256dh key
        auth (str): The auth key
    """

    p256dh: str
    auth: str


class Subscription(BaseModel):
    """A push subscription

    Attributes:
        endpoint (str): The endpoint of the subscription
        expirationTime (str | None): The expiration time of the subscription
        keys (Keys): The keys of the subscription
    """

    endpoint: str
    expirationTime: str | None
    keys: Keys


def get_push_subscriptions() -> list[Subscription] | None:
    """Get the push subscriptions from the database

    Returns:
        list[Subscription] | None: The push subscriptions or None if there was an error
    """
    # Read the database info
    with open("secrets/db_info.json", "r") as file:
        db_info = DbInfo.model_validate_json(file.read())

    # Get the client using the database info and a 1 second timeout
    client = MongoClient(
        host=db_info.host,
        port=db_info.port,
        serverSelectionTimeoutMS=db_info.connection_timeout,
    )

    # Send a test ping to the server
    try:
        print(client.server_info())
    except Exception as ex:
        print(f"[red]Failed to connect to the database: {ex}[/]")
        return None

    # Get the database
    database = client.get_database(db_info.database)

    # Get the collection
    collection = database.get_collection(db_info.collection)

    # Get the clients
    clients = collection.find()

    # Convert the clients to a list of Subscription Models
    subscriptions = [Subscription(**client) for client in clients]

    # Return the subscriptions
    return subscriptions


def send_push_notification(
    subscription: Subscription, title: str, message: str, urgency: str = "normal"
) -> Response | None:
    """Send a push notification to a subscription

    Args:
        subscription (Subscription): The subscription to send the push notification to
        title (str): The title of the push notification
        message (str): The message of the push notification
        urgency (str, optional): The urgency of the notification. Defaults to "normal".

    Returns:
        Response | None: The response from the push notification or None if there was an error
    """
    # Set the subscription
    subscription_info = subscription.model_dump()

    # Set the vapid claims
    with open("secrets/claims.json", "r") as file:
        claims = json.load(file)

    # Send the push notification
    try:
        response = webpush(
            subscription_info=subscription_info,
            data=json.dumps(
                {
                    "title": title,
                    "body": message,
                    "icon": "/icons/tools/converter/android-chrome-192x192.png",
                    "badge": "/icons/tools/converter/badge-192x192.png",
                }
            ),
            headers={"Urgency": urgency},
            vapid_private_key="secrets/private_key.pem",
            vapid_claims=claims,
        )

        # Return the response if it is a Response object otherwise return None
        if isinstance(response, Response):
            return response
        else:
            return None
    except WebPushException as ex:
        # Print the exception
        print(f"WebPushException: {ex}")
        return None


def send(
    title: Annotated[str, typer.Option("--title", "-t")] = "Test",
    message: Annotated[str, typer.Option("--message", "-m")] = "This is a test",
    urgency: Annotated[str, typer.Option("--urgency", "-u")] = "normal",
):
    """Send a push notification to the push subscriptions

    Args:
        title (str, optional): The title of the push notification. Defaults to "Test".
        message (str, optional): The message of the push notification. Defaults to "This is a test".
        urgency (str, optional): The urgency of the push notification. Defaults to "normal".
    """
    # Get the subscriptions
    subscriptions = get_push_subscriptions()

    # Return if there was an error getting the subscriptions
    if subscriptions is None:
        return

    # Get the current time in hours, minutes and seconds with no milliseconds and convert to a string using strftime
    current_time = datetime.now().strftime("%H:%M:%S")

    # Print the current time
    print(f"[blue]Current Time: {current_time}[/]")
    print()

    # Print the title, message and urgency
    print(f"[blue]Title: {title}[/]")
    print(f"[blue]Message: {message}[/]")
    print(f"[blue]Urgency: {urgency}[/]")
    print()

    # Send a push notification to each subscription
    for subscription in subscriptions:
        # Print the subscription
        print(f"[blue]Sending push notification to {subscription.endpoint}[/]")
        print()
        print(subscription)
        print()

        # Send the push notification
        response = send_push_notification(
            subscription,
            title,
            f"{current_time}\n{message}\nUrgency: {urgency}",
            urgency,
        )

        if response is not None:
            # Print the response
            if response.status_code == 201:
                print("[green]Push notification sent successfully[/]")
            else:
                print(
                    f"[red]Push notification failed with status code {response.status_code}[/]"
                )
        else:
            print("[red]Push notification failed[/]")

        print()


if __name__ == "__main__":
    # Run the send function using Typer CLI
    typer.run(send)
