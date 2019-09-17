import sys
import traceback
from gurux_common.io import Parity, StopBits, BaudRate
from gurux_serial import GXSerial
from gurux_net import GXNet
from gurux_dlms.enums import ObjectType
from GXSettings import GXSettings
from GXDLMSReader import GXDLMSReader

class smartclient():
    @classmethod
    def main(cls, args):
        # args: the command line arguments
        reader = None
        settings = GXSettings()
        try:
            # //////////////////////////////////////
            #  Handle command line parameters.
            ret = settings.getParameters(args)
            if ret != 0:
                return
            # //////////////////////////////////////
            #  Initialize connection settings.
            if isinstance(settings.media, GXSerial):
                if settings.iec:
                    settings.media.baudrate = BaudRate.BAUD_RATE_300
                    settings.media.bytesize = 7
                    settings.media.parity = Parity.EVEN
                    settings.media.stopbits = StopBits.ONE
                else:
                    settings.media.baudrate = BaudRate.BAUD_RATE_9600
                    settings.media.bytesize = 8
                    settings.media.parity = Parity.NONE
                    settings.media.stopbits = StopBits.ONE
            elif not isinstance(settings.media, GXNet):
                raise Exception("Unknown media type.")
            # //////////////////////////////////////
            reader = GXDLMSReader(settings.client, settings.media, settings.trace)
            if settings.readObjects:
                reader.initializeConnection()
                reader.getAssociationView()
                for k, v in settings.readObjects:
                    val = reader.read(settings.client.objects.findByLN(ObjectType.NONE, k), v)
                    reader.showValue(v, val)
            else:
                reader.readAll()
        except Exception:
            traceback.print_exc()
        finally:
            if reader:
                try:
                    reader.close()
                except Exception:
                    traceback.print_exc()
            print("Ended.")

if __name__ == '__main__':
    smartclient.main(sys.argv)