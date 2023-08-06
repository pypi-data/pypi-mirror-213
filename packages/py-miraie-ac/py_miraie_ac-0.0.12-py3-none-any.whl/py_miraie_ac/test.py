"""Test class"""
import asyncio
import time
from broker import MirAIeBroker
from api import MirAIeAPI
from enums import AuthType



class Test:
    """TEST"""
    __test = 1

    def __init__(self):
        self.__test = 2

    async def cb1(self, cbbroker: callable):
        """Stuff"""
        await asyncio.sleep(3)
        cbbroker("user", "pwd")

    def start(self):
        """Test method"""

        broker: MirAIeBroker = MirAIeBroker()
        broker.set_topics(["0a0392ff-f302-4d61-aa6a-5205120db688/a00962c502/a163ec014599/status"])
        broker.init_broker(username="", password="",  get_access_token_callback=self.cb1)
        broker.connect()

        while True:
            time.sleep(5)


            # officeAc: Device

            # time.sleep(10)
            # for deviceId, device in home.devices.items():
            #     print("Found device: ", device.friendly_name)

            #     if(device.friendly_name == "Office AC"):
            #         officeAc = device
            #         break
            
            # time.sleep(1)
            # officeAc.set_temperature(25)
            # officeAc.set_swing_mode(SwingMode.ONE)
            #officeAc.turnOff()



#test = Test()
#test.start()





async def start():
    """Test"""
    async with MirAIeAPI(auth_type=AuthType.MOBILE, login_id="", password="") as api:
        await api.initialize()

        while True:
            await asyncio.sleep(5)

asyncio.get_event_loop().run_until_complete(start())
