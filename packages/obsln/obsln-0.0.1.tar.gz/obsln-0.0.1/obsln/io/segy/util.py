# Copyright 2020 Bateared Collie
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# 

from struct import pack, unpack

from obsln.core.util.libnames import _load_cdll


# Import shared libsegy
clibsegy = _load_cdll("segy")


def unpack_header_value(endian, packed_value, length, special_format):
    """
    Unpacks a single value.
    """
    # Use special format if necessary.
    if special_format:
        fmt = ('%s%s' % (endian, special_format)).encode('ascii', 'strict')
        return unpack(fmt, packed_value)[0]
    # Unpack according to different lengths.
    elif length == 2:
        format = ('%sh' % endian).encode('ascii', 'strict')
        return unpack(format, packed_value)[0]
    # Update: Seems to be correct. Two's complement integers seem to be
    # the common way to store integer values.
    elif length == 4:
        format = ('%si' % endian).encode('ascii', 'strict')
        return unpack(format, packed_value)[0]
    # The unassigned field. Since it is unclear how this field is
    # encoded it will just be stored as a string.
    elif length == 8:
        return packed_value
    # Should not happen
    else:
        raise Exception


def _pack_attribute_nicer_exception(obj, name, format):
    """
    packs obj.name with the given format but raises a nicer error message.
    """
    x = getattr(obj, name)
    try:
        return pack(format, x)
    except Exception as e:
        msg = ("Failed to pack header value `%s` (%s) with format `%s` due "
               "to: `%s`")
        try:
            format = format.decode()
        except AttributeError:
            pass
        raise ValueError(msg % (name, str(x), format, e.args[0]))
