from PyCRC.CRCCCITT import CRCCCITT
import binascii


def calculate_crc(bytes):
    crc = CRCCCITT(version='FFFF').calculate(binascii.hexlify(bytearray(bytes)).decode('hex'))
    return [(crc >> 8) & 0xff, crc & 0xff]
