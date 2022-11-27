import logging, sys
import axdrTypes

# A-XDR decoder
class axdrDecode:
    axdrString = ''
    decoded = None
    axdrLen = 0

    def __init__(self):
        pass

    # Decodes an A-XDR hex string and returns an AxdrType-derived object in return
    def decode(self,axdrToDecode):
        self.axdrString = str(axdrToDecode)
        self.axdrLen = len(self.axdrString)
        self.decoded = None

        # Decode the leading tag
        if self.axdrLen>=2:
            tag = int(self.axdrString[0:2], 16)

            logging.debug("tag=%d", tag)

            # Build an object for each supported tag
            if tag == 0:
                logging.debug("null-data")
                self.decoded=axdrTypes.AxdrNulldata(self.axdrString,self.axdrLen)

            elif tag == 1:
                logging.debug("array")
                self.decoded = axdrTypes.AxdrArray(self.axdrString, self.axdrLen)

            elif tag == 2:
                logging.debug("structure")
                self.decoded = axdrTypes.AxdrStructure(self.axdrString, self.axdrLen)

            elif tag == 3:
                logging.debug("boolean")
                self.decoded=axdrTypes.AxdrBoolean(self.axdrString,self.axdrLen)

            elif tag == 4:
                logging.debug("bitstring")
                self.decoded = axdrTypes.AxdrBitstring(self.axdrString, self.axdrLen)

            elif tag == 5:
                logging.debug("int32")
                self.decoded = axdrTypes.AxdrInt32(self.axdrString, self.axdrLen)

            elif tag == 6:
                logging.debug("uint32")
                self.decoded = axdrTypes.AxdrUInt32(self.axdrString, self.axdrLen)

            elif tag == 9:
                logging.debug("string")
                self.decoded = axdrTypes.AxdrString(self.axdrString, self.axdrLen)

            elif tag == 10:
                logging.debug("visiblestring")
                self.decoded = axdrTypes.AxdrVisibleString(self.axdrString, self.axdrLen)

            elif tag == 12:
                logging.debug("utf32string")
                self.decoded = axdrTypes.AxdrUTF8String(self.axdrString, self.axdrLen)

            elif tag == 13:
                logging.debug("bcd")
            elif tag == 15:
                logging.debug("int8")
                self.decoded = axdrTypes.AxdrInt8(self.axdrString, self.axdrLen)

            elif tag == 16:
                logging.debug("int16")
                self.decoded = axdrTypes.AxdrInt16(self.axdrString, self.axdrLen)

            elif tag == 17:
                logging.debug("uint8")
                self.decoded = axdrTypes.AxdrUInt8(self.axdrString, self.axdrLen)

            elif tag == 18:
                logging.debug("uint16")
                self.decoded = axdrTypes.AxdrUInt16(self.axdrString, self.axdrLen)

            elif tag == 19:
                logging.debug("compact")
            elif tag == 20:
                logging.debug("int64")
                self.decoded = axdrTypes.AxdrInt64(self.axdrString, self.axdrLen)

            elif tag == 21:
                logging.debug("uint64")
                self.decoded = axdrTypes.AxdrUInt64(self.axdrString, self.axdrLen)

            elif tag == 22:
                logging.debug("enum")
                self.decoded = axdrTypes.AxdrEnum(self.axdrString, self.axdrLen)

            elif tag == 23:
                logging.debug("float32")
            elif tag == 24:
                logging.debug("float64")
            elif tag == 25:
                logging.debug("date-time")
                self.decoded = axdrTypes.AxdrDateTime(self.axdrString, self.axdrLen)

            elif tag == 26:
                logging.debug("date")
                self.decoded = axdrTypes.AxdrDate(self.axdrString, self.axdrLen)

            elif tag == 27:
                logging.debug("time")
                self.decoded = axdrTypes.AxdrTime(self.axdrString, self.axdrLen)

            elif tag == 28:
                logging.debug("delta-int8")
                self.decoded = axdrTypes.AxdrDeltaInt8(self.axdrString, self.axdrLen)

            elif tag == 29:
                logging.debug("delta-int16")
                self.decoded = axdrTypes.AxdrDeltaInt16(self.axdrString, self.axdrLen)

            elif tag == 30:
                logging.debug("delta-int32")
                self.decoded = axdrTypes.AxdrDeltaInt32(self.axdrString, self.axdrLen)

            elif tag == 31:
                logging.debug("delta-uint8")
                self.decoded = axdrTypes.AxdrDeltaUInt8(self.axdrString, self.axdrLen)

            elif tag == 32:
                logging.debug("delta-uint16")
                self.decoded = axdrTypes.AxdrDeltaUInt16(self.axdrString, self.axdrLen)

            elif tag == 33:
                logging.debug("delta-uint32")
                self.decoded = axdrTypes.AxdrDeltaUInt32(self.axdrString, self.axdrLen)

            elif tag == 255:
                logging.debug("dont-care")
            else:
                logging.error('unknown tag')

            # Return the decoded object
            return self.decoded
        else:
            logging.error('string too short %s', self.axdrString)