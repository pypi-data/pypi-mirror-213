__all__ = [
    'Recipient',
]


import logging

from typing import Optional, Union

from .enums import ErrorBehavior, MeetingRecipientType, PropertiesType, RecipientType
from .exceptions import StandardViolationError
from .prop import FixedLengthProp
from .properties import Properties
from .structures.entry_id import PermanentEntryID
from .utils import verifyPropertyId, verifyType


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Recipient:
    """
    Contains the data of one of the recipients in an msg file.
    """

    def __init__(self, _dir, msg):
        self.__msg = msg # Allows calls to original msg file.
        self.__dir = _dir
        if not self.exists('__properties_version1.0'):
            if msg.errorBehavior & ErrorBehavior.STANDARDS_VIOLATION:
                logger.error('Recipients MUST have a property stream.')
            else:
                raise StandardViolationError('Recipients MUST have a property stream.') from None
        self.__props = Properties(self._getStream('__properties_version1.0'), PropertiesType.RECIPIENT)
        self.__email = self._getStringStream('__substg1.0_39FE')
        if not self.__email:
            self.__email = self._getStringStream('__substg1.0_3003')
        self.__name = self._getStringStream('__substg1.0_3001')
        self.__typeFlags = self.__props.get('0C150003').value or 0
        from .calendar_base import CalendarBase
        if isinstance(msg, CalendarBase):
            self.__type = MeetingRecipientType(0xF & self.__typeFlags)
        else:
            self.__type = RecipientType(0xF & self.__typeFlags)
        self.__formatted = f'{self.__name} <{self.__email}>'

    def _ensureSet(self, variable, streamID, stringStream : bool = True, **kwargs):
        """
        Ensures that the variable exists, otherwise will set it using the
        specified stream. After that, return said variable.

        If the specified stream is not a string stream, make sure to set
        :param string stream: to False.

        :param overrideClass: Class/function to use to morph the data that was
            read. The data will be the first argument to the class's __init__
            function or the function itself, if that is what is provided. By
            default, this will be completely ignored if the value was not found.
        :param preserveNone: If true (default), causes the function to ignore
            :param overrideClass: when the value could not be found (is None).
            If this is changed to False, then the value will be used regardless.
        """
        try:
            return getattr(self, variable)
        except AttributeError:
            if stringStream:
                value = self._getStringStream(streamID)
            else:
                value = self._getStream(streamID)
            # Check if we should be overriding the data type for this instance.
            if kwargs:
                overrideClass = kwargs.get('overrideClass')
                if overrideClass is not None and (value is not None or not kwargs.get('preserveNone', True)):
                    value = overrideClass(value)
            setattr(self, variable, value)
            return value

    def _ensureSetProperty(self, variable : str, propertyName : str, **kwargs):
        """
        Ensures that the variable exists, otherwise will set it using the
        property. After that, return said variable.

        :param overrideClass: Class/function to use to morph the data that was
            read. The data will be the first argument to the class's __init__
            function or the function itself, if that is what is provided. By
            default, this will be completely ignored if the value was not found.
        :param preserveNone: If true (default), causes the function to ignore
            :param overrideClass: when the value could not be found (is None).
            If this is changed to False, then the value will be used regardless.
        """
        try:
            return getattr(self, variable)
        except AttributeError:
            try:
                value = self.props[propertyName].value
            except (KeyError, AttributeError):
                value = None
            # Check if we should be overriding the data type for this instance.
            if kwargs:
                overrideClass = kwargs.get('overrideClass')
                if overrideClass is not None and (value is not None or not kwargs.get('preserveNone', True)):
                    value = overrideClass(value)
            setattr(self, variable, value)
            return value

    def _ensureSetTyped(self, variable : str, _id, **kwargs):
        """
        Like the other ensure set functions, but designed for when something
        could be multiple types (where only one will be present). This way you
        have no need to set the type, it will be handled for you.

        :param overrideClass: Class/function to use to morph the data that was
            read. The data will be the first argument to the class's __init__
            function or the function itself, if that is what is provided. By
            default, this will be completely ignored if the value was not found.
        :param preserveNone: If true (default), causes the function to ignore
            :param overrideClass: when the value could not be found (is None).
            If this is changed to False, then the value will be used regardless.
        """
        try:
            return getattr(self, variable)
        except AttributeError:
            value = self._getTypedData(_id)
            # Check if we should be overriding the data type for this instance.
            if kwargs:
                overrideClass = kwargs.get('overrideClass')
                if overrideClass is not None and (value is not None or not kwargs.get('preserveNone', True)):
                    value = overrideClass(value)
            setattr(self, variable, value)
            return value

    def _getStream(self, filename) -> Optional[bytes]:
        """
        Gets a binary representation of the requested filename.

        This should ALWAYS return a bytes object if it was found, otherwise
        returns None.
        """
        return self.__msg._getStream([self.__dir, filename])

    def _getStringStream(self, filename) -> Optional[str]:
        """
        Gets a string representation of the requested filename. Checks for both
        Unicode and Non-Unicode representations and returns a value if possible.
        If there are both Unicode and Non-Unicode versions, then :param prefer:
        specifies which will be returned.
        """
        return self.__msg._getStringStream([self.__dir, filename])

    def _getTypedData(self, _id, _type = None):
        """
        Gets the data for the specified id as the type that it is supposed to
        be. :param id: MUST be a 4 digit hexadecimal string.

        If you know for sure what type the data is before hand, you can specify
        it as being one of the strings in the constant FIXED_LENGTH_PROPS_STRING
        or VARIABLE_LENGTH_PROPS_STRING.
        """
        verifyPropertyId(id)
        _id = _id.upper()
        found, result = self._getTypedStream('__substg1.0_' + _id, _type)
        if found:
            return result
        else:
            found, result = self._getTypedProperty(_id, _type)
            return result if found else None

    def _getTypedProperty(self, propertyID : str, _type = None):
        """
        Gets the property with the specified id as the type that it is supposed
        to be. :param id: MUST be a 4 digit hexadecimal string.

        If you know for sure what type the property is before hand, you can
        specify it as being one of the strings in the constant
        FIXED_LENGTH_PROPS_STRING or VARIABLE_LENGTH_PROPS_STRING.
        """
        verifyPropertyId(propertyID)
        verifyType(_type)
        propertyID = propertyID.upper()
        for x in (propertyID + _type,) if _type is not None else self.props:
            if x.startswith(propertyID):
                prop = self.props[x]
                return True, (prop.value if isinstance(prop, FixedLengthProp) else prop)
        return False, None

    def _getTypedStream(self, filename, _type = None):
        """
        Gets the contents of the specified stream as the type that it is
        supposed to be.

        Rather than the full filename, you should only feed this function the
        filename sans the type. So if the full name is "__substg1.0_001A001F",
        the filename this function should receive should be "__substg1.0_001A".

        If you know for sure what type the stream is before hand, you can
        specify it as being one of the strings in the constant
        FIXED_LENGTH_PROPS_STRING or VARIABLE_LENGTH_PROPS_STRING.

        If you have not specified the type, the type this function returns in
        many cases cannot be predicted. As such, when using this function it is
        best for you to check the type that it returns. If the function returns
        None, that means it could not find the stream specified.
        """
        self.__msg._getTypedStream(self, [self.__dir, filename], True, _type)

    def exists(self, filename) -> bool:
        """
        Checks if stream exists inside the recipient folder.
        """
        return self.__msg.exists([self.__dir, filename])

    def sExists(self, filename) -> bool:
        """
        Checks if the string stream exists inside the recipient folder.
        """
        return self.__msg.sExists([self.__dir, filename])

    def existsTypedProperty(self, id, _type = None) -> bool:
        """
        Determines if the stream with the provided id exists. The return of this
        function is 2 values, the first being a boolean for if anything was
        found, and the second being how many were found.
        """
        return self.__msg.existsTypedProperty(id, self.__dir, _type, True, self.__props)

    @property
    def account(self) -> Optional[str]:
        """
        Returns the account of this recipient.
        """
        return self._ensureSet('_account', '__substg1.0_3A00')

    @property
    def email(self) -> Optional[str]:
        """
        Returns the recipient's email.
        """
        return self.__email

    @property
    def entryID(self) -> Optional[PermanentEntryID]:
        """
        Returns the recipient's Entry ID.
        """
        return self._ensureSet('_entryID', '__substg1.0_0FFF0102', False, overrideClass = PermanentEntryID)

    @property
    def formatted(self) -> str:
        """
        Returns the formatted recipient string.
        """
        return self.__formatted

    @property
    def instanceKey(self) -> Optional[bytes]:
        """
        Returns the instance key of this recipient.
        """
        return self._ensureSet('_instanceKey', '__substg1.0_0FF60102', False)

    @property
    def name(self) -> Optional[str]:
        """
        Returns the recipient's name.
        """
        return self.__name

    @property
    def props(self) -> Properties:
        """
        Returns the Properties instance of the recipient.
        """
        return self.__props

    @property
    def recordKey(self) -> Optional[bytes]:
        """
        Returns the instance key of this recipient.
        """
        return self._ensureSet('_recordKey', '__substg1.0_0FF90102', False)

    @property
    def searchKey(self) -> Optional[bytes]:
        """
        Returns the search key of this recipient.
        """
        return self._ensureSet('_searchKey', '__substg1.0_300B0102', False)

    @property
    def smtpAddress(self) -> Optional[str]:
        """
        Returns the SMTP address of this recipient.
        """
        return self._ensureSet('_smtpAddress', '__substg1.0_39FE')

    @property
    def transmittableDisplayName(self) -> Optional[str]:
        """
        Returns the transmittable display name of this recipient.
        """
        return self._ensureSet('_transmittableDisplayName', '__substg1.0_3A20')

    @property
    def type(self) -> Union[RecipientType, MeetingRecipientType]:
        """
        Returns the recipient type. Type is:
            * Sender if `type & 0xf == 0`
            * To if `type & 0xf == 1`
            * Cc if `type & 0xf == 2`
            * Bcc if `type & 0xf == 3`
        """
        return self.__type

    @property
    def typeFlags(self) -> int:
        """
        The raw recipient type value and all the flags it includes.
        """
        return self.__typeFlags
