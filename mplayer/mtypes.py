
# Copyright (C) 2013 LiuLang <gsushzhsosgsu@gmail.com>
#
# Copyright (C) 2011  Darwin M. Bautista <djclue917@gmail.com>
#
# This file is part of mplayer.py.
#
# mplayer.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mplayer.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with mplayer.py.  If not, see <http://www.gnu.org/licenses/>.

class MPlayerType(object):
    """The base MPlayer type.

    This class and its subclasses aren't really types. They simply encapsulate
    all the information regarding a specific MPlayer type. In particular:

    name - human-readable name of the type
    type - valid Python type(s) for this type (for use with isinstance())
    convert - a callable which converts MPlayer responses
              to the corresponding Python object
    adapt - a callable which adapts a Python object into a type (str)
            suitable for MPlayer's stdin
    """

    name = None
    type = None
    convert = None
    adapt = staticmethod(repr)


class FlagType(MPlayerType):

    name = 'bool'
    type = bool

    @staticmethod
    def convert(res):
        return (res in ['yes', '1'])

    @staticmethod
    def adapt(obj):
        # MPlayer uses 1 for True and 0 for False
        return MPlayerType.adapt(int(obj))


class IntegerType(MPlayerType):

    name = 'int'
    type = int
    convert = staticmethod(int)


class FloatType(MPlayerType):

    name = 'float'
    type = (float, int)
    convert = staticmethod(float)


class StringType(MPlayerType):

    name = 'string'
    type = str

    @staticmethod
    def convert(res):
        # Response is already a string
        return res

    # FIXME:
    try:
        str
    except NameError:
        pass
    else:
        @staticmethod
        def adapt(obj):
            return obj


class StringListType(MPlayerType):

    name = 'dict'

    @staticmethod
    def convert(res):
        res = res.split(',')
        # For now, return list as a dict ('metadata' property)
        return dict(list(zip(res[::2], res[1::2])))


type_map = {
    'Flag': FlagType, 'Integer': IntegerType, 'Position': IntegerType,
    'Float': FloatType, 'Time': FloatType, 'String': StringType,
    'String list': StringListType
}
