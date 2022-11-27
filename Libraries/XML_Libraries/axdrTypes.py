import logging, sys
import struct
import axdrDecode
import math


# Generic class for an A-XDR type
# Contains the A-XDR string which is decoded when calling the getValue method
class AxdrType:
    axdrstring = None

    def __init__(self, axdrrepr, length):
        self.axdrstring = axdrrepr

    # Get the A-XDR string encoding
    def getAxdr(self):
        return self.axdrstring

    # Get the length of the A-XDR string in characters
    def getLength(self):
        if self.axdrstring is not None:
            return len(self.axdrstring)

    # Get the decoded value for the A-XDR string
    # For complex type (array, string), it is a list of AxdrType-derived objects
    def getValue(self):
        return None

    # True if the type is complex (array or structure)
    def isComplex(self):
        return False

    # decodes variable length
    # returns a tuple with (length of the length encoding, length of the string itself)
    @staticmethod
    def decodeLength(instring):
        first_byte = int(instring[2:4], 16)
        found_length = None
        if first_byte < 0x80:
            found_length = (1, first_byte)
        elif first_byte == 0x81:
            if len(instring) >= 6:
                found_length = (2, int(instring[4:6], 16))
        elif first_byte == 0x82:
            if len(instring) >= 8:
                found_length = (3, int(instring[4:8], 16))
        elif first_byte == 0x83:
            if len(instring) >= 10:
                found_length = (4, int(instring[4:10], 16))
        elif first_byte == 0x84:
            if len(instring) >= 12:
                found_length = (5, int(instring[4:12], 16))
        return found_length


# Implements each specific A-XDR type
class AxdrNulldata(AxdrType):
    def __init__(self, axdrrepr, length):
        if length < 2:
            logging.error("wrong length for null-data : %d", length)
        else:
            self.axdrstring = axdrrepr[:2]


class AxdrBoolean(AxdrType):
    def __init__(self, axdrrepr, length):
        if length < 4:
            logging.error("wrong length for boolean : %d", length)
        elif not (axdrrepr[2:4] == "00" or axdrrepr[2:4] == "01"):
            logging.error("wrong value for boolean : %s", axdrrepr[2:4])
        else:
            self.axdrstring = axdrrepr[:4]

    def getValue(self):
        if self.axdrstring is not None:
            if self.axdrstring[2:4] == '00':
                return False
            else:
                return True


class AxdrInt32(AxdrType):
    def __init__(self, axdrrepr, length):
        if length < 10:
            logging.error("wrong length for Int32 : %d", length)
        else:
            self.axdrstring = axdrrepr[:10]

    def getValue(self):
        if self.axdrstring is not None:
            return struct.unpack(">i", bytes.fromhex(self.axdrstring[2:11]))[0]


class AxdrUInt32(AxdrType):
    def __init__(self, axdrrepr, length):
        if length < 10:
            logging.error("wrong length for UInt32 : %d", length)
        else:
            self.axdrstring = axdrrepr[:10]

    def getValue(self):
        if self.axdrstring is not None:
            return struct.unpack(">I", bytes.fromhex(self.axdrstring[2:11]))[0]


class AxdrInt8(AxdrType):
    def __init__(self, axdrrepr, length):
        if length < 4:
            logging.error("wrong length for Int8 : %d", length)
        else:
            self.axdrstring = axdrrepr[:4]

    def getValue(self):
        if self.axdrstring is not None:
            return struct.unpack(">b", bytes.fromhex(self.axdrstring[2:4]))[0]


class AxdrUInt8(AxdrType):
    def __init__(self, axdrrepr, length):
        if length < 4:
            logging.error("wrong length for UInt8 : %d", length)
        else:
            self.axdrstring = axdrrepr[:4]

    def getValue(self):
        if self.axdrstring is not None:
            return struct.unpack(">B", bytes.fromhex(self.axdrstring[2:4]))[0]


class AxdrInt16(AxdrType):
    def __init__(self, axdrrepr, length):
        if length < 6:
            logging.error("wrong length for Int16 : %d", length)
        else:
            self.axdrstring = axdrrepr[:6]

    def getValue(self):
        if self.axdrstring is not None:
            return struct.unpack(">h", bytes.fromhex(self.axdrstring[2:6]))[0]


class AxdrUInt16(AxdrType):
    def __init__(self, axdrrepr, length):
        if length < 6:
            logging.error("wrong length for UInt16 : %d", length)
        else:
            self.axdrstring = axdrrepr[:6]

    def getValue(self):
        if self.axdrstring is not None:
            return struct.unpack(">H", bytes.fromhex(self.axdrstring[2:6]))[0]


class AxdrInt64(AxdrType):
    def __init__(self, axdrrepr, length):
        if length < 18:
            logging.error("wrong length for Int64 : %d", length)
        else:
            self.axdrstring = axdrrepr[:18]

    def getValue(self):
        if self.axdrstring is not None:
            return struct.unpack(">q", bytes.fromhex(self.axdrstring[2:19]))[0]


class AxdrUInt64(AxdrType):
    def __init__(self, axdrrepr, length):
        if length < 18:
            logging.error("wrong length for UInt64 : %d", length)
        else:
            self.axdrstring = axdrrepr[:18]

    def getValue(self):
        if self.axdrstring is not None:
            return struct.unpack(">Q", bytes.fromhex(self.axdrstring[2:19]))[0]


# Same implementation as the previous ones
class AxdrEnum(AxdrUInt8):
    pass


class AxdrDeltaInt8(AxdrInt8):
    pass


class AxdrDeltaUInt8(AxdrUInt8):
    pass


class AxdrDeltaInt16(AxdrInt16):
    pass


class AxdrDeltaUInt16(AxdrUInt16):
    pass


class AxdrDeltaInt32(AxdrInt32):
    pass


class AxdrDeltaUInt32(AxdrUInt32):
    pass


class AxdrString(AxdrType):
    def __init__(self, axdrrepr, length):
        stringlength = self.decodeLength(axdrrepr)
        logging.debug("string length : %d %d", stringlength[0], stringlength[1])
        if stringlength is not None and length < stringlength[0] * 2 + stringlength[1] * 2 + 2:
            logging.error("wrong length for String : %d", length)
        else:
            self.axdrstring = axdrrepr[:stringlength[0] * 2 + stringlength[1] * 2 + 2]

    def getValue(self):
        if self.axdrstring is not None:
            stringlength = self.decodeLength(self.axdrstring)
            substring = self.axdrstring[stringlength[0] * 2 + 2:stringlength[0] * 2 + stringlength[1] * 2 + 2]
            logging.debug("substring %s", substring)
            return bytes.fromhex(substring)


# Same implementation as AxdrString
class AxdrVisibleString(AxdrString):
    pass


class AxdrUTF8String(AxdrString):
    pass


class AxdrArray(AxdrType):
    list = []

    def __init__(self, axdrrepr, length):
        self.list = []
        arraylength = self.decodeLength(axdrrepr)
        logging.debug("array length : %d %d", arraylength[0], arraylength[1])

        if arraylength is not None and arraylength[1] < 0:
            logging.error("wrong length for Array : %d", length)
        else:
            # Recursively decode the elements of the array
            decoder = axdrDecode.axdrDecode()
            pointer = arraylength[0] * 2 + 2
            decoded_elements = 0
            self.axdrstring = axdrrepr[:pointer]

            while decoded_elements < arraylength[1]:
                element = decoder.decode(axdrrepr[pointer:])
                if element is not None:
                    self.list.append(element)
                    self.axdrstring = self.axdrstring + element.getAxdr()
                    pointer = pointer + element.getLength()
                else:
                    logging.error("missing element : %d", decoded_elements)
                decoded_elements = decoded_elements + 1

    def getValue(self):
        return self.list
    
    def isComplex(self):
        return True


# Same implementation for structure
class AxdrStructure(AxdrArray):
    pass


class AxdrBitstring(AxdrType):
    def __init__(self, axdrrepr, length):
        self.list = []
        stringlength = self.decodeLength(axdrrepr)
        logging.debug("bitstring length : %d %d", stringlength[0], stringlength[1])

        if stringlength is not None and length < stringlength[0] * 2 + math.ceil(stringlength[1] / 8) * 2 + 2:
            logging.error("wrong length for Bitstring : %d", length)
        else:
            self.axdrstring = axdrrepr[:stringlength[0] * 2 + math.ceil(stringlength[1] / 8) * 2 + 2]

    def getValue(self):
        if self.axdrstring is not None:
            stringlength = self.decodeLength(self.axdrstring)
            substring = self.axdrstring[
                        stringlength[0] * 2 + 2: stringlength[0] * 2 + math.ceil(stringlength[1] / 8) * 2 + 2]

            formatstr = '0' + str(math.ceil(stringlength[1] / 8) * 8) + 'b'
            logging.debug(substring + " " + formatstr)
            binstring = format(int(substring, 16), formatstr)

            return binstring[:stringlength[1]]

class AxdrDate(AxdrType):
    def __init__(self, axdrrepr, length):
        if length < 12:
            logging.error("wrong length for Date : %d", length)
        else:
            self.axdrstring = axdrrepr[:12]

    def getValue(self):
        # YYYYMMDDww
        if self.axdrstring is not None:
            return str(int(self.axdrstring[2:6],16))+"-"+str(int(self.axdrstring[6:8],16))+"-"+str(int(self.axdrstring[8:10],16))

class AxdrTime(AxdrType):
    def __init__(self, axdrrepr, length):
        if length < 10:
            logging.error("wrong length for Time : %d", length)
        else:
            self.axdrstring = axdrrepr[:10]

    def getValue(self):
        # HHMMSShh
        if self.axdrstring is not None:
            return str(int(self.axdrstring[2:4],16))+":"+str(int(self.axdrstring[4:6],16))+":"+str(int(self.axdrstring[6:8],16))

class AxdrDateTime(AxdrType):
    def __init__(self, axdrrepr, length):
        if length < 26:
            logging.error("wrong length for DateTime : %d", length)
        else:
            self.axdrstring = axdrrepr[:26]

    def getValue(self):
        # YYYYMMDDwwHHMMSShhVVVVss
        if self.axdrstring is not None:
            return str(int(self.axdrstring[2:6],16))+"-"+str(int(self.axdrstring[6:8],16))+"-"+str(int(self.axdrstring[8:10],16))+" "+\
                   str(int(self.axdrstring[12:14],16))+":"+str(int(self.axdrstring[14:16],16))+":"+str(int(self.axdrstring[16:18],16))
