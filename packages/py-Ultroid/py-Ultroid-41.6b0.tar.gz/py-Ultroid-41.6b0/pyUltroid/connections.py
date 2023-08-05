# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import os
import time

from redis import StrictRedis
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError
from telethon.sessions import StringSession

from .dB.database import Var


def connect_redis():
    err = ""
    if ":" not in Var.REDIS_URI:
        err += "\nWrong REDIS_URI. Quitting...\n"
    if "http" in Var.REDIS_URI:
        err += "Remove http or https from REDIS_URI. Quitting...\n"
    if "/" in Var.REDIS_URI:
        err += "Your REDIS_URI should start with redis.xxx. Quitting...\n"
    if err is not "":
        print(err)
        exit(1)
    redis_info = Var.REDIS_URI.split(":")
    DB = StrictRedis(
        host=redis_info[0],
        port=redis_info[1],
        password=Var.REDIS_PASSWORD,
        charset="utf-8",
        decode_responses=True,
    )
    print("Getting Connection With Redis Database")
    return DB


def redis_connection():
    our_db = connect_redis()
    time.sleep(6)
    try:
        our_db.ping()
    except BaseException:
        connected = False
        print("Can't connect to Redis Database.... Restarting....")
        for x in range(1, 6):
            our_db = connect_redis()
            time.sleep(5)
            try:
                if our_db.ping():
                    connected = True
                    break
            except BaseException as conn:
                print(
                    f"{type(conn)}\nConnection Failed ...  Trying To Reconnect {x}/5 .."
                )
        if not connected:
            print("Redis Connection Failed.....")
            exit(1)
        else:
            print("Reconnected To Redis Server Succesfully")
    print("Succesfully Established Connection With Redis DataBase.")
    return our_db


def session_file():
    if os.path.exists("client-session.session"):
        _session = "client-session"
    elif Var.SESSION:
        _session = StringSession(Var.SESSION)
    else:
        print("No String Session found. Quitting...")
        exit(1)
    return _session


def client_connection():
    try:
        client = TelegramClient(session_file(), Var.API_ID, Var.API_HASH)
    except AuthKeyDuplicatedError:
        print("String Session Expired. Please Create New String Session. Quitting...")
        exit(1)
    except Exception as ap:
        print(f"ERROR - {ap}")
        exit(1)
    return client


def vc_connection(udB):
    vc_client = None
    if udB.get("VC_SESSION"):
        try:
            vc_client = TelegramClient(
                StringSession(udB.get("VC_SESSION")),
                api_id=Var.API_ID,
                api_hash=Var.API_HASH,
            )
        except AuthKeyDuplicatedError:
            print("ERROR - Please create a new VC string Session !")
        except Exception as vcerr:
            print(str(vcerr))
    return vc_client
