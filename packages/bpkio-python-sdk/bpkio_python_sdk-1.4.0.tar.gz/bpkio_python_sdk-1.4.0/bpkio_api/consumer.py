from importlib.metadata import version

import uplink

__version__ = version("bpkio-python-sdk")


class BpkioSdkConsumer(uplink.Consumer):
    def __init__(self, base_url="", **kwargs):
        super().__init__(base_url, **kwargs)

        user_agent = f"bpkio-python-sdk/{__version__}"

        if "user_agent" in kwargs:
            user_agent = kwargs["user_agent"] + " " + user_agent

        # Set this header for all requests of the instance.
        self.session.headers["User-Agent"] = user_agent
