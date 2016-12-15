# -*- coding: utf-8 -*-

from __future__ import absolute_import, division

import sys
import ndef
import pytest
import uuid

class TestDeviceAddress:
    cls = 'ndef.bluetooth.DeviceAddress'

    @pytest.mark.parametrize("address", [
        '01:02:03:04:05:06', '01-02-03-04-05-06', '01-02:03-04:05-06'])
    def test_init_address_format(self, address):
        obj = ndef.bluetooth.DeviceAddress(address)
        assert isinstance(obj, ndef.bluetooth.DeviceAddress)
        assert obj == ndef.bluetooth.DeviceAddress(address)
        assert obj.addr == '01:02:03:04:05:06'
        assert obj.type == 'public'

    @pytest.mark.parametrize("address_type", ['public', 'random'])
    def test_init_address_type(self, address_type):
        obj = ndef.bluetooth.DeviceAddress('01:02:03:04:05:06', address_type)
        assert isinstance(obj, ndef.bluetooth.DeviceAddress)
        assert obj.addr == '01:02:03:04:05:06'
        assert obj.type == address_type

    def test_format_str(self):
        obj = ndef.bluetooth.DeviceAddress('01:02:03:04:05:06', 'public')
        assert str(obj) == '01:02:03:04:05:06 (public)'
        obj = ndef.bluetooth.DeviceAddress('01:02:03:04:05:06', 'random')
        assert str(obj) == '01:02:03:04:05:06 (random)'

    def test_format_repr(self):
        obj = ndef.bluetooth.DeviceAddress('01:02:03:04:05:06', 'public')
        assert repr(obj) == self.cls + "('01:02:03:04:05:06', 'public')"
        obj = ndef.bluetooth.DeviceAddress('01:02:03:04:05:06', 'random')
        assert repr(obj) == self.cls + "('01:02:03:04:05:06', 'random')"

    def test_encode(self):
        obj = ndef.bluetooth.DeviceAddress('01:02:03:04:05:06')
        assert obj.encode() == b'\x06\x05\x04\x03\x02\x01\x00'
        assert obj.encode('LE') == b'\x06\x05\x04\x03\x02\x01\x00'
        assert obj.encode(context='LE') == b'\x06\x05\x04\x03\x02\x01\x00'
        assert obj.encode('EP') == b'\x06\x05\x04\x03\x02\x01'
        assert obj.encode(context='EP') == b'\x06\x05\x04\x03\x02\x01'
        obj = ndef.bluetooth.DeviceAddress('01:02:03:04:05:06', 'random')
        assert obj.encode() == b'\x06\x05\x04\x03\x02\x01\x01'

    @pytest.mark.parametrize("octets, address_type", [
        (b'\x06\x05\x04\x03\x02\x01', 'public'),
        (b'\x06\x05\x04\x03\x02\x01\x00', 'public'),
        (b'\x06\x05\x04\x03\x02\x01\x01', 'random'),
    ])
    def test_decode(self, octets, address_type):
        obj = ndef.bluetooth.DeviceAddress.decode(octets)
        assert isinstance(obj, ndef.bluetooth.DeviceAddress)
        assert obj.addr == '01:02:03:04:05:06'
        assert obj.type == address_type

    @pytest.mark.parametrize("octets, errstr", [
        (b'\x06\x05\x04\x03\x02', "can't be decoded from 5 octets"),
        (b'\x06\x05\x04\x03\x02\x01\x00\x00', "can't be decoded from 8 octets"),
    ])
    def test_decode_fail(self, octets, errstr):
        with pytest.raises(ndef.DecodeError) as excinfo:
            obj = ndef.bluetooth.DeviceAddress.decode(octets)
        assert str(excinfo.value) == self.cls + ' ' + errstr


class TestDeviceClass:
    cls = 'ndef.bluetooth.DeviceClass'

    @pytest.mark.parametrize("cod, major_dc, minor_dc, major_sc", [
        (0x000000, "Miscellaneous", "Uncategorized", ()),
        (0x800000, "Miscellaneous", "Uncategorized", ("Information",)),
        (0x400000, "Miscellaneous", "Uncategorized", ("Telephony",)),
        (0x200000, "Miscellaneous", "Uncategorized", ("Audio",)),
        (0x100000, "Miscellaneous", "Uncategorized", ("Object Transfer",)),
        (0x080000, "Miscellaneous", "Uncategorized", ("Capturing",)),
        (0x040000, "Miscellaneous", "Uncategorized", ("Rendering",)),
        (0x020000, "Miscellaneous", "Uncategorized", ("Networking",)),
        (0x010000, "Miscellaneous", "Uncategorized", ("Positioning",)),
        (0x008000, "Miscellaneous", "Uncategorized", ("Reserved (bit 15)",)),
        (0x004000, "Miscellaneous", "Uncategorized", ("Reserved (bit 14)",)),
        (0x002000, "Miscellaneous", "Uncategorized", ("Limited Discoverable Mode",)),
        (0x001000, "Reserved 10000b", "Undefined 000000b", ()),
        (0x000800, "Toy", "Reserved 000000b", ()),
        (0x000400, "Audio / Video", "Uncategorized", ()),
        (0x000200, "Phone", "Uncategorized", ()),
        (0x000100, "Computer", "Uncategorized", ()),
        (0x000080, "Miscellaneous", "Reserved 100000b", ()),
        (0x000040, "Miscellaneous", "Reserved 010000b", ()),
        (0x000020, "Miscellaneous", "Reserved 001000b", ()),
        (0x000010, "Miscellaneous", "Reserved 000100b", ()),
        (0x000008, "Miscellaneous", "Reserved 000010b", ()),
        (0x000004, "Miscellaneous", "Reserved 000001b", ()),
        (0x000002, None, None, None),
        (0x000001, None, None, None),
    ])
    def test_init(self, cod, major_dc, minor_dc, major_sc):
        obj = ndef.bluetooth.DeviceClass(cod)
        assert isinstance(obj, ndef.bluetooth.DeviceClass)
        assert obj == ndef.bluetooth.DeviceClass(cod)
        assert obj.major_device_class == major_dc
        assert obj.minor_device_class == minor_dc
        assert obj.major_service_class == major_sc

    @pytest.mark.parametrize("cod, strstr", [
        (0x000000, "Miscellaneous - Uncategorized - Unspecified"),
        (0x800000, "Miscellaneous - Uncategorized - Information"),
        (0x280000, "Miscellaneous - Uncategorized - Capturing and Audio"),
        (0x008000, "Miscellaneous - Uncategorized - Reserved (bit 15)"),
        (0x000040, "Miscellaneous - Reserved 010000b - Unspecified"),
        (0x001000, "Reserved 10000b - Undefined 000000b - Unspecified"),
        (0x000800, "Toy - Reserved 000000b - Unspecified"),
        (0x200410, "Audio / Video - Microphone - Audio"),
        (0x000104, "Computer - Desktop workstation - Unspecified"),
        (0x000001, "Unknown format 000000000000000000000001b"),
    ])
    def test_format_str(self, cod, strstr):
        obj = ndef.bluetooth.DeviceClass(cod)
        assert str(obj) == strstr

    def test_format_repr(self):
        obj = ndef.bluetooth.DeviceClass(0x123456)
        assert repr(obj) == self.cls + "(0x123456)"

    @pytest.mark.parametrize("cod, octets", [
        (0x000000, b'\x00\x00\x00'),
        (0x123456, b'\x56\x34\x12'),
    ])
    def test_encode(self, cod, octets):
        obj = ndef.bluetooth.DeviceClass(cod)
        assert obj.encode() == octets

    @pytest.mark.parametrize("cod, errstr", [
        (0x1000000, "can't encode 16777216 into class of device octets"),
        (-1, "can't encode -1 into class of device octets"),
    ])
    def test_encode_fail(self, cod, errstr):
        obj = ndef.bluetooth.DeviceClass(cod)
        with pytest.raises(ndef.EncodeError) as excinfo:
            obj.encode()
        assert str(excinfo.value) == self.cls + ' ' + errstr

    @pytest.mark.parametrize("octets", [b'\x00\x00\x00', b'\x56\x34\x12',])
    def test_decode(self, octets):
        obj = ndef.bluetooth.DeviceClass.decode(octets)
        assert obj.encode() == octets

    @pytest.mark.parametrize("octets, errstr", [
        (2 * b'\x00', "can't decode class of device from 2 octets"),
        (4 * b'\x00', "can't decode class of device from 4 octets"),
    ])
    def test_decode_fail(self, octets, errstr):
        with pytest.raises(ndef.DecodeError) as excinfo:
            ndef.bluetooth.DeviceClass.decode(octets)
        assert str(excinfo.value) == self.cls + ' ' + errstr


class TestServiceClass:
    cls = "ndef.bluetooth.ServiceClass"

    @pytest.mark.parametrize("arg, uuid", [
        (0x1101, uuid.UUID("00001101-0000-1000-8000-00805f9b34fb")),
        ("Serial Port", uuid.UUID("00001101-0000-1000-8000-00805f9b34fb")),
        ("00001101-0000-1000-8000-00805f9b34fb",
         uuid.UUID("00001101-0000-1000-8000-00805f9b34fb")),
    ])
    def test_init(self, arg, uuid):
        obj = ndef.bluetooth.ServiceClass(arg)
        assert isinstance(obj, eval(self.cls))
        assert obj.uuid == uuid

    def test_format_repr(self):
        obj = ndef.bluetooth.ServiceClass(0x1101)
        assert repr(obj) == self.cls + "('00001101-0000-1000-8000-00805f9b34fb')"

    def test_uuid_name(self):
        obj = ndef.bluetooth.ServiceClass(0x1101)
        assert obj.name == "Serial Port"
        obj = ndef.bluetooth.ServiceClass('00000000-0000-1000-8000-00805f9b34fb')
        assert obj.name == '00000000-0000-1000-8000-00805f9b34fb'
        obj = ndef.bluetooth.ServiceClass('00000000-0000-0000-0000-000000000000')
        assert obj.name == '00000000-0000-0000-0000-000000000000'

    def test_get_uuid_names(self):
        assert isinstance(ndef.bluetooth.ServiceClass.get_uuid_names(), tuple)
        assert len(ndef.bluetooth.ServiceClass.get_uuid_names()) == 68

    @pytest.mark.parametrize("arg, octets", [
        (0x1101, b'\x01\x11'),
        (0x10001101, b'\x01\x11\x00\x10'),
        ('61626364-3031-3233-3435-363738394142', b'dcba1032456789AB'),
    ])
    def test_encode(self, arg, octets):
        obj = ndef.bluetooth.ServiceClass(arg)
        assert obj.encode() == octets

    @pytest.mark.parametrize("octets", [
        b'\x01\x11', b'\x01\x11\x00\x10', b'dcba1032456789AB',
    ])
    def test_decode(self, octets):
        obj = ndef.bluetooth.ServiceClass.decode(octets)
        assert obj.encode() == octets

    @pytest.mark.parametrize("octets, errstr", [
        (b'\x01', "can't decode service class uuid from 1 octets"),
        (b'\x01\x11\x00', "can't decode service class uuid from 3 octets"),
        (b'dcba1032456789A', "can't decode service class uuid from 15 octets"),
        (b'dcba1032456789ABC', "can't decode service class uuid from 17 octets"),
    ])
    def test_decode_fail(self, octets, errstr):
        with pytest.raises(ndef.DecodeError) as excinfo:
            ndef.bluetooth.ServiceClass.decode(octets)
        assert str(excinfo.value) == self.cls + ' ' + errstr


class TestBluetoothEasyPairingRecord:
    cls = "ndef.bluetooth.BluetoothEasyPairingRecord"

    def test_init(self):
        obj = ndef.BluetoothEasyPairingRecord('01:02:03:04:05:06')
        assert isinstance(obj, eval(self.cls))
        assert obj.device_address.addr == '01:02:03:04:05:06'
        adr = ndef.bluetooth.DeviceAddress('01:02:03:04:05:06')
        eir = ((0x08, b'My Blue'), (0x09, b'My Bluetooth Device'))
        obj = ndef.BluetoothEasyPairingRecord(adr, *eir)
        assert isinstance(obj, eval(self.cls))
        assert obj.device_address.addr == '01:02:03:04:05:06'
        assert len(obj.keys()) == len(obj.values()) == len(obj.items()) == 2
        assert obj.get(0x08) == b'My Blue'
        assert obj.get('Shortened Local Name') == b'My Blue'
        assert obj.get(0x09) == b'My Bluetooth Device'
        assert obj.get('Complete Local Name') == b'My Bluetooth Device'
        assert 0x01 not in obj
        assert obj.setdefault('Flags', b'\x00') == b'\x00'
        for key in obj:
            assert obj.get(key) is not None

    @pytest.mark.parametrize("key, name", [
        (0x01, 'Flags'),
        (0x02, 'Incomplete List of 16-bit Service Class UUIDs'),
        (0x03, 'Complete List of 16-bit Service Class UUIDs'),
        (0x04, 'Incomplete List of 32-bit Service Class UUIDs'),
        (0x05, 'Complete List of 32-bit Service Class UUIDs'),
        (0x06, 'Incomplete List of 128-bit Service Class UUIDs'),
        (0x07, 'Complete List of 128-bit Service Class UUIDs'),
        (0x08, 'Shortened Local Name'),
        (0x09, 'Complete Local Name'),
        (0x0D, 'Class of Device'),
        (0x0E, 'Simple Pairing Hash C'),
        (0x0E, 'Simple Pairing Hash C-192'),
        (0x0F, 'Simple Pairing Randomizer R'),
        (0x0F, 'Simple Pairing Randomizer R-192'),
        (0x10, 'Security Manager TK Value'),
        (0x11, 'Security Manager Out of Band Flags'),
        (0x22, 'LE Secure Connections Confirmation Value'),
        (0x23, 'LE Secure Connections Random Value'),
        (0x1B, 'LE Bluetooth Device Address'),
        (0x1C, 'LE Role'),
        (0x1D, 'Simple Pairing Hash C-256'),
        (0x1E, 'Simple Pairing Randomizer R-256'),
        (0xFF, 'Manufacturer Specific Data'),
    ])
    def test_key_name_mapping(self, key, name):
        adr = '01:02:03:04:05:06'
        obj = ndef.BluetoothEasyPairingRecord(adr, (key, b'abc'))
        assert name in obj.attribute_names
        assert obj[name] == b'abc'

    def test_key_value_error(self):
        adr = '01:02:03:04:05:06'
        with pytest.raises(ValueError) as excinfo:
            ndef.BluetoothEasyPairingRecord(adr).get('invalid name')
        assert str(excinfo.value) == "unknown attribute name 'invalid name'"

    def test_attr_device_name(self):
        obj = ndef.BluetoothEasyPairingRecord('01:02:03:04:05:06')
        assert obj.device_name == ''
        obj[0x08] = b'My Blue'
        assert 0x08 in obj and 0x09 not in obj
        assert obj.device_name == 'My Blue'
        obj[0x09] = b'My Bluetooth Device'
        assert 0x08 in obj and 0x09 in obj
        assert obj.device_name == 'My Bluetooth Device'
        obj.device_name = 'My Bluetooth Device'
        assert obj[0x09] == b'My Bluetooth Device'
        assert 0x08 not in obj
        obj.device_name = 'My Device'
        assert obj[0x09] == b'My Device'
        assert 0x08 not in obj

    def test_attr_device_class(self):
        obj = ndef.BluetoothEasyPairingRecord('01:02:03:04:05:06')
        assert isinstance(obj.device_class, ndef.bluetooth.DeviceClass)
        assert obj.device_class.major_device_class == 'Miscellaneous'
        assert obj.device_class.minor_device_class == 'Uncategorized'
        assert obj.device_class.major_service_class == ()
        obj.device_class = 0x20041C
        assert obj.device_class.major_device_class == 'Audio / Video'
        assert obj.device_class.minor_device_class == 'Portable Audio'
        assert obj.device_class.major_service_class == ('Audio',)
        obj.device_class = ndef.bluetooth.DeviceClass(0x0C06C0)
        assert obj.device_class.major_device_class == 'Imaging'
        assert obj.device_class.minor_device_class == 'Scanner/Printer'
        assert obj.device_class.major_service_class == ('Rendering', 'Capturing')

    def test_attr_service_class_list(self):
        obj = ndef.BluetoothEasyPairingRecord('01:02:03:04:05:06')
        assert obj.service_class_list == []
        obj[0x02] = b'\x01\x11'
        obj[0x03] = b'\x02\x11'
        obj[0x04] = b'\x01\x11\x00\x10'
        obj[0x05] = b'\x02\x11\x00\x10'
        obj[0x06] = b'\0\0\0\0\1\1\2\2\3\3\4\4\4\4\4\4'
        obj[0x07] = b'\1\0\0\0\1\1\2\2\3\3\4\4\4\4\4\4'
        assert obj.service_class_list == [
            ndef.bluetooth.ServiceClass('00001101-0000-1000-8000-00805f9b34fb'),
            ndef.bluetooth.ServiceClass('00001102-0000-1000-8000-00805f9b34fb'),
            ndef.bluetooth.ServiceClass('10001101-0000-1000-8000-00805f9b34fb'),
            ndef.bluetooth.ServiceClass('10001102-0000-1000-8000-00805f9b34fb'),
            ndef.bluetooth.ServiceClass('00000000-0101-0202-0303-040404040404'),
            ndef.bluetooth.ServiceClass('00000001-0101-0202-0303-040404040404'),
        ]

    def test_meth_add_service_class(self):
        obj = ndef.BluetoothEasyPairingRecord('01:02:03:04:05:06')
        assert obj.service_class_list == []
        obj.add_service_class(0x1101)
        assert obj.get(0x02) == b'\x01\x11'
        assert obj.get(0x03) is None
        obj.add_service_class(0x1102, complete=True)
        assert obj.get(0x02) is None
        assert obj.get(0x03) == b'\x01\x11\x02\x11'
        obj.add_service_class(0x10001101)
        assert obj.get(0x04) == b'\x01\x11\x00\x10'
        assert obj.get(0x05) is None
        obj.add_service_class(0x10001102, complete=True)
        assert obj.get(0x04) is None
        assert obj.get(0x05) == b'\x01\x11\x00\x10\x02\x11\x00\x10'
        sc_1 = ndef.bluetooth.ServiceClass(str(uuid.uuid4()))
        sc_2 = ndef.bluetooth.ServiceClass(str(uuid.uuid4()))
        obj.add_service_class(sc_1)
        assert obj.get(0x06) == sc_1.uuid.bytes_le
        assert obj.get(0x07) is None
        obj.add_service_class(sc_2, complete=True)
        assert obj.get(0x06) is None
        assert obj.get(0x07) == sc_1.uuid.bytes_le + sc_2.uuid.bytes_le

    def test_meth_get_simple_pairing_hash(self):
        obj = ndef.BluetoothEasyPairingRecord('01:02:03:04:05:06')
        assert obj.get_simple_pairing_hash() is None
        assert obj.get_simple_pairing_hash('C-192') is None
        assert obj.get_simple_pairing_hash('C-256') is None
        obj[0x0E] = b'\1' + 15 * b'\0'
        obj[0x1D] = b'\2' + 15 * b'\0'
        assert obj.get_simple_pairing_hash() == 1
        assert obj.get_simple_pairing_hash('C-192') == 1
        assert obj.get_simple_pairing_hash('C-256') == 2

    def test_meth_set_simple_pairing_hash(self):
        obj = ndef.BluetoothEasyPairingRecord('01:02:03:04:05:06')
        obj.set_simple_pairing_hash(1, 'C-192')
        assert obj[0x0E] == b'\1' + 15 * b'\0'
        obj.set_simple_pairing_hash(2, 'C-256')
        assert obj[0x1D] == b'\2' + 15 * b'\0'
        obj.set_simple_pairing_hash(3)
        assert obj[0x0E] == b'\3' + 15 * b'\0'

    def test_meth_get_simple_pairing_randomizer(self):
        obj = ndef.BluetoothEasyPairingRecord('01:02:03:04:05:06')
        assert obj.get_simple_pairing_randomizer() is None
        assert obj.get_simple_pairing_randomizer('R-192') is None
        assert obj.get_simple_pairing_randomizer('R-256') is None
        obj[0x0F] = b'\1' + 15 * b'\0'
        obj[0x1E] = b'\2' + 15 * b'\0'
        assert obj.get_simple_pairing_randomizer() == 1
        assert obj.get_simple_pairing_randomizer('R-192') == 1
        assert obj.get_simple_pairing_randomizer('R-256') == 2

    def test_meth_set_simple_pairing_randomizer(self):
        obj = ndef.BluetoothEasyPairingRecord('01:02:03:04:05:06')
        obj.set_simple_pairing_randomizer(1, 'R-192')
        assert obj[0x0F] == b'\1' + 15 * b'\0'
        obj.set_simple_pairing_randomizer(2, 'R-256')
        assert obj[0x1E] == b'\2' + 15 * b'\0'
        obj.set_simple_pairing_randomizer(3)
        assert obj[0x0F] == b'\3' + 15 * b'\0'

    def test_encode(self):
        obj = ndef.BluetoothEasyPairingRecord('01:02:03:04:05:06')
        assert obj.type == 'application/vnd.bluetooth.ep.oob'
        assert obj.data == b'\x08\x00\x06\x05\x04\x03\x02\x01'
        obj = ndef.BluetoothEasyPairingRecord('01:02:03:04:05:06', (255, b'ab'))
        assert obj.type == 'application/vnd.bluetooth.ep.oob'
        assert obj.data == b'\x0c\x00\x06\x05\x04\x03\x02\x01\x03\xffab'

    @pytest.mark.parametrize("octets", [
        'd2200c6170706c69636174696f6e2f766e642e626c7565746f6f74682e65702e6f6f62'
        '0c0006050403020103ff6162',
        'd2200d6170706c69636174696f6e2f766e642e626c7565746f6f74682e65702e6f6f62'
        '0d000605040302010003ff6162',
    ])
    def test_decode(self, octets):
        octets = bytearray.fromhex(octets)
        record = next(ndef.message_decoder(octets))
        assert isinstance(record, eval(self.cls))
        assert record.type == 'application/vnd.bluetooth.ep.oob'
        assert record.device_address.addr == '01:02:03:04:05:06'
        assert len(record.items()) == 1
        assert record.get(0xFF) == b'ab'

    @pytest.mark.parametrize("octets, errstr", [
        ('d2200c6170706c69636174696f6e2f766e642e626c7565746f6f74682e65702e6f6f62'
         '0d0006050403020103ff6162',
         'oob data length 13 exceeds payload size 12'),
        ('d2200d6170706c69636174696f6e2f766e642e626c7565746f6f74682e65702e6f6f62'
         '0c0006050403020103ff616200',
         'payload size 13 exceeds oob data length 12'),
    ])
    def test_decode_fail(self, octets, errstr):
        octets = bytearray.fromhex(octets)
        with pytest.raises(ndef.DecodeError) as excinfo:
            next(ndef.message_decoder(octets))
        assert str(excinfo.value) == self.cls + ' ' + errstr

    def test_format(self):
        adr = ndef.bluetooth.DeviceAddress('01:02:03:04:05:06')
        eir = ((0x08, b'Blue'), (0x09, b'Blue Device'))
        obj = ndef.BluetoothEasyPairingRecord(adr, *eir)
        if sys.version_info < (3,):
            txt = "(0x08, 'Blue'), (0x09, 'Blue Device')"
        else:
            txt = "(0x08, b'Blue'), (0x09, b'Blue Device')"
        assert format(obj, 'args') == txt
        txt = "Attributes 0x08 0x09"
        assert format(obj, 'data') == txt
        txt = "NDEF Bluetooth Easy Pairing Record ID '' Attributes 0x08 0x09"
        assert format(obj) == txt
            


class TestBluetoothLowEnergyRecord:
    cls = "ndef.bluetooth.BluetoothLowEnergyRecord"

    def test_init(self):
        obj = ndef.BluetoothLowEnergyRecord()
        assert isinstance(obj, eval(self.cls))
        assert len(obj.keys()) == len(obj.values()) == len(obj.items()) == 0
        obj = ndef.BluetoothLowEnergyRecord((0x08, b'My Blue'), (0xFF, b'abc'))
        assert len(obj.keys()) == len(obj.values()) == len(obj.items()) == 2
        assert obj.get(0x08) == b'My Blue'
        assert obj.get('Shortened Local Name') == b'My Blue'
        assert obj.get(0xFF) == b'abc'
        assert obj.get('Manufacturer Specific Data') == b'abc'
        assert 0x01 not in obj
        assert obj.setdefault('Flags', b'\x00') == b'\x00'
        for key in obj:
            assert obj.get(key) is not None

    @pytest.mark.parametrize("key, name", [
        (0x01, 'Flags'),
        (0x02, 'Incomplete List of 16-bit Service Class UUIDs'),
        (0x03, 'Complete List of 16-bit Service Class UUIDs'),
        (0x04, 'Incomplete List of 32-bit Service Class UUIDs'),
        (0x05, 'Complete List of 32-bit Service Class UUIDs'),
        (0x06, 'Incomplete List of 128-bit Service Class UUIDs'),
        (0x07, 'Complete List of 128-bit Service Class UUIDs'),
        (0x08, 'Shortened Local Name'),
        (0x09, 'Complete Local Name'),
        (0x0D, 'Class of Device'),
        (0x0E, 'Simple Pairing Hash C'),
        (0x0E, 'Simple Pairing Hash C-192'),
        (0x0F, 'Simple Pairing Randomizer R'),
        (0x0F, 'Simple Pairing Randomizer R-192'),
        (0x10, 'Security Manager TK Value'),
        (0x11, 'Security Manager Out of Band Flags'),
        (0x22, 'LE Secure Connections Confirmation Value'),
        (0x23, 'LE Secure Connections Random Value'),
        (0x1B, 'LE Bluetooth Device Address'),
        (0x1C, 'LE Role'),
        (0x1D, 'Simple Pairing Hash C-256'),
        (0x1E, 'Simple Pairing Randomizer R-256'),
        (0xFF, 'Manufacturer Specific Data'),
    ])
    def test_key_name_mapping(self, key, name):
        obj = ndef.BluetoothLowEnergyRecord((key, b'abc'))
        assert name in obj.attribute_names
        assert obj[name] == b'abc'

    def test_key_value_error(self):
        with pytest.raises(ValueError) as excinfo:
            ndef.BluetoothLowEnergyRecord().get('invalid name')
        assert str(excinfo.value) == "unknown attribute name 'invalid name'"

    @pytest.mark.parametrize("device_address", [
        "01:02:03:04:05:06", ("01:02:03:04:05:06", "public"),
        ndef.bluetooth.DeviceAddress("01:02:03:04:05:06", "public"),
    ])
    def test_attr_device_address(self, device_address):
        obj = ndef.BluetoothLowEnergyRecord()
        assert obj.device_address is None
        obj.device_address = device_address
        assert obj.device_address.addr == "01:02:03:04:05:06"
        assert obj.device_address.type == "public"

    def test_encode(self):
        obj = ndef.BluetoothLowEnergyRecord()
        assert obj.type == 'application/vnd.bluetooth.le.oob'
        assert obj.data == b''
        obj.device_address = ("01:02:03:04:05:06", "public")
        assert obj.data == b'\x08\x1b\x06\x05\x04\x03\x02\x01\x00'
        obj['Manufacturer Specific Data'] = b'abc'
        assert obj.data == b'\x08\x1b\x06\x05\x04\x03\x02\x01\x00\x04\xffabc'

    @pytest.mark.parametrize("octets", [
        'd2200d6170706c69636174696f6e2f766e642e626c7565746f6f74682e6c652e6f6f62'
        '081b0605040302010003ff6162',
        'd2200e6170706c69636174696f6e2f766e642e626c7565746f6f74682e6c652e6f6f62'
        '081b060504030201000003ff6162',
    ])
    def test_decode(self, octets):
        octets = bytearray.fromhex(octets)
        record = next(ndef.message_decoder(octets))
        assert isinstance(record, eval(self.cls))
        assert record.type == 'application/vnd.bluetooth.le.oob'
        assert record.device_address.addr == '01:02:03:04:05:06'
        assert len(record.items()) == 2
        assert record.get(0xFF) == b'ab'



