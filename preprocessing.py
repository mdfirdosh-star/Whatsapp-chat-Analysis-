import re
import pandas as pd
import streamlit as st


def preprocess(data):

    # Date pattern
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:[\s\u202f]?(?:AM|PM|am|pm))?\s-\s"

    # Messages aur dates alag
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({
        "user_message": messages,
        "message_date": dates
    })

    # Special space remove/normalize
    df["message_date"] = (
        df["message_date"]
        .str.replace("\u202f", " ", regex=False)
        .str.replace(" - ", "", regex=False)
        .str.strip()
    )

    users = []
    msgs = []

    for message in df["user_message"]:

        # Name ya Number dono handle karega
        entry = re.split(r"^([^:]+):\s", message)

        if len(entry) > 2:
            users.append(entry[1].strip())
            msgs.append(entry[2].strip())

        else:
            users.append("group_notification")
            msgs.append(message.strip())

    df["user"] = users
    df["message"] = msgs

    df.drop(columns=["user_message"], inplace=True)

    # Datetime conversion
    df["message_date"] = pd.to_datetime(
        df["message_date"],
        errors="coerce"
    )

    # Date features
    df["year"] = df["message_date"].dt.year
    df["month"] = df["message_date"].dt.month_name()
    df["num_month"] = df["message_date"].dt.month
    df["day"] = df["message_date"].dt.day
    df["hour"] = df["message_date"].dt.hour
    df["minute"] = df["message_date"].dt.minute

    # Original date column remove
    df.drop(columns=["message_date"], inplace=True)

    return df