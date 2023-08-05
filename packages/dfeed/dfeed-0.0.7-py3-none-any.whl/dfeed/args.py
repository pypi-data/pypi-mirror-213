#!/usr/bin/env python3


class Args:
    @classmethod
    def define_args(cls, args):
        cls.__args = {key: val for key, val in args.__dict__.items()}

    @classmethod
    def getBool(cls, key):
        return cls.__args[key]

    @classmethod
    def getInt(cls, key):
        retVal = cls.__args[key]
        return int(retVal) if retVal is not None else -1

    @classmethod
    def getStr(cls, key):
        retVal = cls.__args[key]
        return str(retVal) if retVal is not None else ""

    @classmethod
    def add_feed(cls, feed: str):
        if cls.__args["feed"] == "":
            cls.__args["feed"] = feed
        else:
            cls.__args["feed"] = f"{cls.__args['feed']},{feed}"
