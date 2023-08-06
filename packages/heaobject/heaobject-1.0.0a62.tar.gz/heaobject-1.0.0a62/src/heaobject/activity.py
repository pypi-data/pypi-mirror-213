"""
Classes for recording user activity.

The HEA Activity Microservice subscribes to the types in this module and
manages them for you. Any subclasses of Activity that do not appear in this
module are ignored by the Activity microservice.
"""
from abc import ABC, abstractmethod
from datetime import date, datetime
from humanize import naturaldelta
from enum import Enum
from typing import Optional, Union
from .data import DataObject, SameMimeType
import uuid


class Status(Enum):
    """
    The lifecycle of an action. Allowed sequences of statuses are:
    NOT_STARTED, IN_PROGRESS, and COMPLETED; and NOT_STARTED, IN_PROGRESS, and
    FAILED. Their values are ordered according to these sequences, for example,
    Status.NOT_STARTED.value < Status.IN_PROGRESS.value < Status.FAILED.value.
    However, comparing statuses directly, for example,
    Status.NOT_STARTED < Status.IN_PROGRESS does not work. Instantaneous
    actions skip directly from NOT_STARTED to either COMPLETED or FAILED.
    """
    NOT_STARTED = 10
    IN_PROGRESS = 20
    COMPLETED = 30
    FAILED = 40


class DesktopObjectAction(DataObject, SameMimeType, ABC):
    """
    Abstract base class for recording user activity. Activity records have a
    beginning and an end. Examples include logins and actions on desktop
    objects. Concrete implementations must at minimum provide implementations
    of the began and ended properties.

    Activity objects, like other desktop objects, have an id property that is
    generated when the object is stored. Activity objects also have an
    application-generated id for situations where it is desirable to record
    changes in an action's state prior to the object being stored (such as when
    sending the object over an asynchronous message queue).
    """

    @abstractmethod
    def __init__(self):
        """
        Constructor for Activity objects. It generates a version 4 UUID and
        assigns it to the application_id property. The initial status is
        NOT_STARTED.
        """
        super().__init__()
        self.__user_id: Optional[str] = None
        # The python docs (https://docs.python.org/3.10/library/uuid.html)
        # recommend using uuid1 or 4, but 1 may leak IP addresses of server-
        # side processes, so I went with 4.
        self.__application_id = str(uuid.uuid4())


    @classmethod
    def get_mime_type(cls) -> str:
        return 'application/x.activity'

    @property
    def application_id(self) -> str:
        """A computed uuid for identifying updates on the same activity. If
        activity objects are generated and sent over a message queue, the id
        field may not be set until the receiver stores the object. The activity
        might have concluded before an id is generated. The unique_id property
        serves as a stand-in for the id for the sender to identify updates on
        an activity independently of the receiver. See the docstring for
        DesktopObject.id for the distinction between application ids and
        database ids (the latter is stored in the DesktopObject.id property)"""
        return self.__application_id

    @property
    def mime_type(self) -> str:
        return type(self).get_mime_type()

    @property
    def user_id(self) -> Optional[str]:
        """The identifier of the user who began the activity. It may be
        different from the owner of the activity object so as to control the
        object's visibility."""
        return self.__user_id

    @user_id.setter
    def user_id(self, __user_id: Optional[str]) -> None:
        self.__user_id = str(__user_id) if __user_id is not None else None

    @property
    @abstractmethod
    def began(self) -> date | None:
        """When the activity began."""
        pass

    @property
    @abstractmethod
    def ended(self) -> date | None:
        """When the activity ended."""
        pass

    @property
    def duration(self) -> int | None:
        """How long the activity took to complete or fail in seconds."""
        if self.began is not None and self.ended is not None:
            return (self.ended - self.began).seconds
        else:
            return None

    @property
    def human_readable_duration(self) -> str | None:
        """How long the activity took to complete or fail in human readable form."""
        if self.began is not None and self.ended is not None:
            return naturaldelta(self.ended - self.began)
        else:
            return None


class Action(DesktopObjectAction, ABC):
    """
    Actions are user activities with a lifecycle indicated by the action's
    status property.
    """
    @abstractmethod
    def __init__(self):
        super().__init__()
        self.__began: date | None = None
        self.__ended: date | None = None
        self.__status: Optional[Union[Status, str]] = Status.NOT_STARTED

    @property
    def began(self) -> date | None:
        return self.__began

    @property
    def ended(self) -> date | None:
        return self.__ended

    @property
    def status(self) -> Optional[Status]:
        """The action's lifecycle status as a Status enum value. If setting
        the property to a string value, the property will attempt to parse the
        string into a Status enum value. The default value is
        Status.NOT_STARTED."""
        return self.__status

    @status.setter
    def status(self, __status: Optional[Status]) -> None:
        old_status = self.__status
        if isinstance(__status, Status):
            ___status = __status
        elif isinstance(__status, str):
            try:
                ___status = Status[__status]
            except KeyError as e:
                raise ValueError(str(e))
        else:
            raise ValueError(
            "Status can only be a Status enum value or string that can be converted to Status enum value.")
        if ___status.value < old_status.value:
            raise ValueError(f'Invalid status changed {old_status} to {___status}')
        self.__status = ___status
        now = datetime.now()
        if old_status == Status.NOT_STARTED and self.__status.value > Status.NOT_STARTED.value:
            self.__began = now
        if old_status.value < Status.COMPLETED.value and self.__status == Status.COMPLETED:
            self.__ended = now
        if old_status.value < Status.FAILED.value and self.__status == Status.FAILED:
            self.__ended = now


class DesktopObjectAction(Action):
    """A user action on a desktop object.

    The name property is used to store a code for the action. HEA defines a
    set of standard codes prefixed with hea-, and HEA reserves that prefix for
    its own use. Third parties may define their own prefix and action codes.

    The description property is expected to be populated with a brief
    description of the action."""
    def __init__(self):
        super().__init__()
        self.__old_object_uri: str | None = None
        self.__new_object_uri: str | None = None

    @property
    def old_object_uri(self) -> str | None:
        """The URI of the object prior to the action being performed, if any. It should be set while the activity has
        a NOT_STARTED status."""
        return self.__old_object_uri

    @old_object_uri.setter
    def old_object_uri(self, old_object_uri: str | None):
        self.__old_object_uri = str(old_object_uri) if old_object_uri is not None else None

    @property
    def new_object_uri(self) -> str | None:
        return self.__new_object_uri

    @new_object_uri.setter
    def new_object_uri(self, new_object_uri: str | None):
        """The URI of the object after the action has completed, if any. It is only set if the activity has a COMPLETED
        status."""
        self.__new_object_uri = str(new_object_uri) if new_object_uri is not None else None
