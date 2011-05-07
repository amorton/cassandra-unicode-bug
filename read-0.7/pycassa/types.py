from datetime import datetime
import struct
import time
import warnings

__all__ = ['Column', 'DateTime', 'DateTimeString', 'Float64', 'FloatString',
           'Long', 'Int64', 'IntString', 'String']

class Column(object):
    """Base class for typed columns."""
    def __init__(self, default=None):
        self.default = default

class DateTime(Column):
    """Column for :class:`datetime` objects stored as long timestamps."""
    def __init__(self, *args, **kwargs):
        Column.__init__(self, *args, **kwargs)
        self.struct = struct.Struct('q')

    def pack(self, val):
        if not isinstance(val, datetime):
            raise TypeError('expected datetime, %s found' % type(val).__name__)
        return self.struct.pack(int(time.mktime(val.timetuple())))

    def unpack(self, val):
        return datetime.fromtimestamp(self.struct.unpack(val)[0])

class DateTimeString(Column):
    """
    Column for :class:`datetime` objects stored as ``%Y-%m-%d %H:%M:%S``

    """
    format = '%Y-%m-%d %H:%M:%S'
    def pack(self, val):
        if not isinstance(val, datetime):
            raise TypeError('expected datetime, %s found' % type(val).__name__)
        return val.strftime(self.format)

    def unpack(self, val):
        return datetime.strptime(val, self.format)

class Float64(Column):
    """Column for 64bit floats."""
    def __init__(self, *args, **kwargs):
        Column.__init__(self, *args, **kwargs)
        self.struct = struct.Struct('d')

    def pack(self, val):
        if not isinstance(val, float):
            raise TypeError('expected float, %s found' % type(val).__name__)
        return self.struct.pack(val)

    def unpack(self, val):
        return self.struct.unpack(val)[0]

class FloatString(Column):
    """Column for floats stored as strings."""
    def pack(self, val):
        if not isinstance(val, float):
            raise TypeError('expected float, %s found' % type(val).__name__)
        return str(val)

    def unpack(self, val):
        return float(val)

class Long(Column):
    """
    Column for 64bit ints.

    This uses big-endian encoding, which is the normal encoding for integers
    in Cassandra.

    """
    def __init__(self, *args, **kwargs):
        Column.__init__(self, *args, **kwargs)
        self.struct = struct.Struct('>q')

    def pack(self, val):
        if not isinstance(val, (int, long)):
            raise TypeError('expected int or long, %s found' % type(val).__name__)
        return self.struct.pack(val)

    def unpack(self, val):
        return self.struct.unpack(val)[0]


class Int64(Column):
    """
    Column for 64bit ints.

    This uses native-endian encoding, which is little-endian on x86 and
    x86-64 architectures.  This means it is not compatible with Cassandra's
    LongType, and some clients may not decode the values properly.

    .. deprecated:: 1.0.6
       Use :class:`Long` instead

    """
    def __init__(self, *args, **kwargs):
        warnings.warn("Int64 is not compatible with Cassandra's LongType and is deprecated; " +
                      "use Long instead.", DeprecationWarning)
        Column.__init__(self, *args, **kwargs)
        self.struct = struct.Struct('q')

    def pack(self, val):
        if not isinstance(val, (int, long)):
            raise TypeError('expected int or long, %s found' % type(val).__name__)
        return self.struct.pack(val)

    def unpack(self, val):
        return self.struct.unpack(val)[0]

class IntString(Column):
    """Column for ints stored as strings."""
    def pack(self, val):
        if not isinstance(val, (int, long)):
            raise TypeError('expected int or long, %s found' % type(val).__name__)
        return str(val)

    def unpack(self, val):
        return int(val)

class String(Column):
    """Column for :class:`str` or :class:`unicode` objects."""
    def pack(self, val):
        if not isinstance(val, basestring):
            raise TypeError('expected str or unicode, %s found' % type(val).__name__)
        return val

    def unpack(self, val):
        return val
