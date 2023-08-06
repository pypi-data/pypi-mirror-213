from __future__ import annotations
import oexp.jbridge as jbridge
import sys
import weakref
from multiprocessing import current_process
from threading import current_thread
import abc
from typing import List, Optional, Dict, TypeVar, Generic
from enum import Enum, auto
import json

_SAFE_PROCESS = current_process().pid
_SAFE_THREAD = current_thread().ident


def _ensure_synchronized():
    global _SAFE_PROCESS, _SAFE_THREAD
    if current_process().pid != _SAFE_PROCESS or current_thread().ident != _SAFE_THREAD:
        raise Exception(
            f"Python-Kotlin communication is currently not safe to use across multiple threads or processes. If you need this feature, please let me know."
        )


JAR_URL = f"https://matt-central.s3.us-east-2.amazonaws.com//0/versioned/front/529/oexp-front-0-all.jar"


class OexpExitSocketHeaders(Enum):
    EXIT = b"\x00"


EXIT = b"\x00"
SET_EXIT_PORT = b"\x01"
CALL_GLOBAL_FUN = b"\x02"
CREATE_OBJECT = b"\x03"
INIT_OBJECT = b"\x04"
CHECK_EQUALITY = b"\x05"
STR = b"\x06"
CALL_FUN = b"\x07"
GET_JSON = b"\x08"
GET_VAL = b"\x09"
SET_VAR = b"\x0A"
GC = b"\x0B"


def _sendall(b):
    jbridge._java_conn.sendall(b)


def _send_short(arg):
    _sendall(arg.to_bytes(2, "big"))


def _send_int(arg):
    _sendall(arg.to_bytes(4, "big"))


def _send_long(arg):
    _sendall(arg.to_bytes(8, "big"))


def _send_string(arg):
    the_int = len(arg)
    _send_int(the_int)
    _sendall(arg.encode())


def _recv(n):
    return jbridge._java_conn.recv(n)


def _recv_is_present():
    isPresent = _recv_byte()
    if isPresent == b"\x00":
        return False
    else:
        if isPresent != b"\x01":
            raise Exception(f"isPresent should be b'\x01' but is {isPresent}")
        return True


def _recv_byte(nullable=False):
    if nullable and not _recv_is_present():
        return None
    return _recv(1)


def _recv_short(nullable=False):
    if nullable and not _recv_is_present():
        return None
    return int.from_bytes(_recv(2), "big", signed=True)


def _recv_int(nullable=False):
    if nullable and not _recv_is_present():
        return None
    return int.from_bytes(_recv(4), "big", signed=True)


def _recv_long(nullable=False):
    if nullable and not _recv_is_present():
        return None
    return int.from_bytes(_recv(8), "big", signed=True)


def _recv_string(nullable=False):
    if nullable and not _recv_is_present():
        return None
    length = _recv_int()
    return _recv(length).decode("utf-8")


def _recv_exception_check():
    no_exception = _recv_byte()
    if no_exception == b"\x00":
        return None
    else:
        if no_exception != b"\x01":
            raise Exception(f"no_exception should be b'\x01' but is {no_exception}")
        report = _recv_string()
        import oexp.jbridge

        oexp.jbridge.kill_java()
        raise Exception(Exception(report))


def _recv_confirmation():
    confirmation = _recv_byte()
    if confirmation != b"\x00":
        raise Exception(f"confirmation should be b'\x00' but is {confirmation}")


def _recv_bool(nullable=False):
    if nullable and not _recv_is_present():
        return None
    isTrue = _recv_byte()
    if isTrue == b"\x01":
        return True
    else:
        if isTrue != b"\x00":
            raise Exception(f"isTrue should be b'\x00' but is {isTrue}")
        return False


def _recv_object(cls, nullable=False):
    if nullable and not _recv_is_present():
        return None
    r_id = _recv_long()
    if isinstance(cls, KBObject):
        if r_id != cls._id._id:
            cls._init()
            raise Exception(f"buggy singleton id")
        return cls
    else:
        return cls(_id=r_id)


def _recv_enum(cls, nullable=False):
    if nullable and not _recv_is_present():
        return None
    ordinal = _recv_short()
    members = cls.__members__.values()
    for mem in members:
        if mem.value == ordinal:
            return mem
    raise Exception(f"could not find enum constant of {cls} with {ordinal=}")


def _recv_list(elementReceiveFun, nullable=False):
    if nullable and not _recv_is_present():
        return None
    r_len = _recv_int()
    r = []
    for i in range(r_len):
        r.append(elementReceiveFun())
    return r


def _recv_map(keyReceiveFun, valueReceiveFun, nullable=False):
    if nullable and not _recv_is_present():
        return None
    r_len = _recv_int()
    r = {}
    for i in range(r_len):
        k = keyReceiveFun()
        r[k] = valueReceiveFun()
    return r


class DEFAULT_VALUE:
    pass


DEFAULT_VALUE = DEFAULT_VALUE()


class NO_DEFAULT:
    pass


NO_DEFAULT = NO_DEFAULT()


class _ObjectID:
    _object_ids = {}

    def __init__(self, _id):
        self._id = _id

    def __str__(self):
        return f"_ObjectID[{self._id}]"

    def __repr__(self):
        return str(self)


def _object_id(_id):
    ref = _ObjectID._object_ids.get(_id)
    if ref is not None:
        return ref()
    else:
        obj = _ObjectID(_id)
        wref = weakref.ref(obj, lambda ref: _gc_callback(_id))
        _ObjectID._object_ids[_id] = wref
        return obj


_PROBABLY_DISCONNECTED = False


def _gc_callback(the_id):
    global _PROBABLY_DISCONNECTED
    if not _PROBABLY_DISCONNECTED:
        try:
            _sendall(GC)
            _send_long(the_id)
            del _ObjectID._object_ids[the_id]
        except OSError:
            _PROBABLY_DISCONNECTED = True


def _exit_server():
    _sendall(EXIT)


def _check_required_parameters(**kwargs):
    for k, v in kwargs.items():
        if v == NO_DEFAULT:
            raise Exception(f"there is no default value for {k}, so it must be defined")


# [[matt.oexp.front.api.ApiKt#login]]
def login(username=NO_DEFAULT, password=NO_DEFAULT) -> OnlineExperiments:
    _ensure_synchronized()
    _check_required_parameters(**dict(username=username, password=password))
    jbridge._init_java()
    _sendall(CALL_GLOBAL_FUN)
    _send_string(f"matt.oexp.front.api.ApiKt")
    _send_string(f"login")
    _send_string(username)
    _send_string(password)
    _recv_exception_check()
    return _recv_object(OnlineExperiments, nullable=False)


class KBClass(abc.ABC):
    def __str__(self):
        return f"{type(self)} with id {self._id}"


class KBVClass(KBClass, abc.ABC):
    pass


class KBDClass(KBClass, abc.ABC):
    pass


class KBObject(KBClass, abc.ABC):
    pass


# [[matt.oexp.front.api.API]]
class API(KBObject):
    _id = None

    @staticmethod
    def _init():
        _ensure_synchronized()
        if API._id is None:
            jbridge._init_java()
            _sendall(INIT_OBJECT)
            _send_string("matt.oexp.front.api.API")
            API._id = _object_id(_recv_long())

    # [[matt.oexp.front.api.API#enableLocalMode]]
    def enable_local_mode(self, port=NO_DEFAULT):
        _ensure_synchronized()
        _check_required_parameters(**dict(port=port))
        API._init()
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(0)
        _send_int(port)
        _recv_exception_check()
        return _recv_confirmation()

    # [[matt.oexp.front.api.API#enableStageMode]]
    def enable_stage_mode(self, token=NO_DEFAULT):
        _ensure_synchronized()
        _check_required_parameters(**dict(token=token))
        API._init()
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(1)
        _send_string(token)
        _recv_exception_check()
        return _recv_confirmation()

    # [[matt.oexp.front.api.API]]
    def __eq__(self, other):
        _ensure_synchronized()
        return type(other) == type(self)


API = API()


def experiment(user=NO_DEFAULT, uid=NO_DEFAULT):
    _check_required_parameters(**dict(user=user, uid=uid))
    return Experiment(user, uid)


# [[matt.oexp.front.api.Experiment]]
class Experiment(KBDClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.front.api.Experiment")
            _send_long(args[0]._id._id)
            _send_long(args[1])
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.front.api.Experiment#css]]
    @property
    def css(self) -> Optional[str]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_string(nullable=True)
        return temp

    @css.setter
    def css(self, value) -> Optional[str]:
        _ensure_synchronized()
        _sendall(SET_VAR)
        _send_long(self._id._id)
        _send_int(0)
        if value is None:
            _sendall(b"\x00")
        else:
            _sendall(b"\x01")
        if value is not None:
            _send_string(value)
        _recv_confirmation()

    # [[matt.oexp.front.api.Experiment#manifests]]
    @property
    def manifests(self) -> Optional[List[TrialManifest]]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(1)
        temp = _recv_list(
            elementReceiveFun=lambda: _recv_object(TrialManifest, nullable=False),
            nullable=True,
        )
        return temp

    @manifests.setter
    def manifests(self, value) -> Optional[List[TrialManifest]]:
        _ensure_synchronized()
        _sendall(SET_VAR)
        _send_long(self._id._id)
        _send_int(1)
        if value is None:
            _sendall(b"\x00")
        else:
            _sendall(b"\x01")
        if value is not None:
            _send_int(len(value))
            for e in value:
                _send_long(e._id._id)
        _recv_confirmation()

    # [[matt.oexp.front.api.Experiment#name]]
    @property
    def name(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(2)
        temp = _recv_string(nullable=False)
        return temp

    @name.setter
    def name(self, value) -> str:
        _ensure_synchronized()
        _sendall(SET_VAR)
        _send_long(self._id._id)
        _send_int(2)
        _send_string(value)
        _recv_confirmation()

    # [[matt.oexp.front.api.Experiment#uid]]
    @property
    def uid(self) -> int:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(3)
        temp = _recv_long(nullable=False)
        return temp

    # [[matt.oexp.front.api.Experiment#user]]
    @property
    def user(self) -> OnlineExperiments:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(4)
        temp = _recv_object(OnlineExperiments, nullable=False)
        return temp

    # [[matt.oexp.front.api.Experiment#delete]]
    def delete(self):
        _ensure_synchronized()
        _check_required_parameters(**dict())
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(0)
        _recv_exception_check()
        return _recv_confirmation()

    # [[matt.oexp.front.api.Experiment#deleteAllImages]]
    def delete_all_images(self):
        _ensure_synchronized()
        _check_required_parameters(**dict())
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(1)
        _recv_exception_check()
        return _recv_confirmation()

    # [[matt.oexp.front.api.Experiment#generateImageUrl]]
    def generate_image_url(self, path=NO_DEFAULT) -> str:
        _ensure_synchronized()
        _check_required_parameters(**dict(path=path))
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(2)
        _send_string(path)
        _recv_exception_check()
        return _recv_string(nullable=False)

    # [[matt.oexp.front.api.Experiment#linkProlific]]
    def link_prolific(self, prolific_study_id=NO_DEFAULT) -> ProlificStudyData:
        _ensure_synchronized()
        _check_required_parameters(**dict(prolific_study_id=prolific_study_id))
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(3)
        _send_string(prolific_study_id)
        _recv_exception_check()
        return _recv_object(ProlificStudyData, nullable=False)

    # [[matt.oexp.front.api.Experiment#listImages]]
    def list_images(self) -> List[str]:
        _ensure_synchronized()
        _check_required_parameters(**dict())
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(4)
        _recv_exception_check()
        return _recv_list(
            elementReceiveFun=lambda: _recv_string(nullable=False), nullable=False
        )

    # [[matt.oexp.front.api.Experiment#open]]
    def open(self):
        _ensure_synchronized()
        _check_required_parameters(**dict())
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(5)
        _recv_exception_check()
        return _recv_confirmation()

    # [[matt.oexp.front.api.Experiment#sessionUrl]]
    def session_url(
        self, disable_auto_fullscreen=DEFAULT_VALUE, allow_fullscreen_exit=DEFAULT_VALUE
    ) -> str:
        _ensure_synchronized()
        _check_required_parameters(**dict())
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(6)
        if disable_auto_fullscreen == DEFAULT_VALUE:
            _sendall(b"\x00")
        else:
            _sendall(b"\x01")
            if disable_auto_fullscreen is None:
                _sendall(b"\x00")
            else:
                _sendall(b"\x01")
            if disable_auto_fullscreen is not None:
                if disable_auto_fullscreen:
                    _sendall(b"\x01")
                else:
                    _sendall(b"\x00")
        if allow_fullscreen_exit == DEFAULT_VALUE:
            _sendall(b"\x00")
        else:
            _sendall(b"\x01")
            if allow_fullscreen_exit is None:
                _sendall(b"\x00")
            else:
                _sendall(b"\x01")
            if allow_fullscreen_exit is not None:
                if allow_fullscreen_exit:
                    _sendall(b"\x01")
                else:
                    _sendall(b"\x00")
        _recv_exception_check()
        return _recv_string(nullable=False)

    # [[matt.oexp.front.api.Experiment#subjectData]]
    def subject_data(self) -> SubjectData:
        _ensure_synchronized()
        _check_required_parameters(**dict())
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(7)
        _recv_exception_check()
        return _recv_object(SubjectData, nullable=False)

    # [[matt.oexp.front.api.Experiment#uploadImages]]
    def upload_images(self, root_dir=NO_DEFAULT) -> List[str]:
        _ensure_synchronized()
        _check_required_parameters(**dict(root_dir=root_dir))
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(8)
        _send_string(root_dir)
        _recv_exception_check()
        return _recv_list(
            elementReceiveFun=lambda: _recv_string(nullable=False), nullable=False
        )

    # [[matt.oexp.front.api.Experiment#viewImage]]
    def view_image(self, path=NO_DEFAULT):
        _ensure_synchronized()
        _check_required_parameters(**dict(path=path))
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(9)
        _send_string(path)
        _recv_exception_check()
        return _recv_confirmation()

    # [[matt.oexp.front.api.Experiment]]
    def __eq__(self, other):
        _ensure_synchronized()
        if isinstance(other, KBClass):
            _sendall(CHECK_EQUALITY)
            _send_long(self._id._id)
            _send_long(other._id._id)
            return _recv_bool()
        else:
            return False


def online_experiments(username=NO_DEFAULT, password=NO_DEFAULT):
    _check_required_parameters(**dict(username=username, password=password))
    return OnlineExperiments(username, password)


# [[matt.oexp.front.api.OnlineExperiments]]
class OnlineExperiments(KBDClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.front.api.OnlineExperiments")
            _send_string(args[0])
            _send_string(args[1])
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.front.api.OnlineExperiments#password]]
    @property
    def password(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_string(nullable=False)
        return temp

    # [[matt.oexp.front.api.OnlineExperiments#prolificKey]]
    @property
    def prolific_key(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(1)
        temp = _recv_string(nullable=False)
        return temp

    @prolific_key.setter
    def prolific_key(self, value) -> str:
        _ensure_synchronized()
        _sendall(SET_VAR)
        _send_long(self._id._id)
        _send_int(1)
        _send_string(value)
        _recv_confirmation()

    # [[matt.oexp.front.api.OnlineExperiments#username]]
    @property
    def username(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(2)
        temp = _recv_string(nullable=False)
        return temp

    # [[matt.oexp.front.api.OnlineExperiments#changePassword]]
    def change_password(self, new_password=NO_DEFAULT):
        _ensure_synchronized()
        _check_required_parameters(**dict(new_password=new_password))
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(0)
        _send_string(new_password)
        _recv_exception_check()
        return _recv_confirmation()

    # [[matt.oexp.front.api.OnlineExperiments#experiment]]
    def experiment(self, name=NO_DEFAULT) -> Experiment:
        _ensure_synchronized()
        _check_required_parameters(**dict(name=name))
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(1)
        _send_string(name)
        _recv_exception_check()
        return _recv_object(Experiment, nullable=False)

    # [[matt.oexp.front.api.OnlineExperiments#experimentWithUid]]
    def experiment_with_uid(self, uid=NO_DEFAULT) -> Experiment:
        _ensure_synchronized()
        _check_required_parameters(**dict(uid=uid))
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(2)
        _send_long(uid._id._id)
        _recv_exception_check()
        return _recv_object(Experiment, nullable=False)

    # [[matt.oexp.front.api.OnlineExperiments#listExperimentData]]
    def list_experiment_data(self) -> List[ExperimentConfig]:
        _ensure_synchronized()
        _check_required_parameters(**dict())
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(3)
        _recv_exception_check()
        return _recv_list(
            elementReceiveFun=lambda: _recv_object(ExperimentConfig, nullable=False),
            nullable=False,
        )

    # [[matt.oexp.front.api.OnlineExperiments#listExperiments]]
    def list_experiments(self) -> List[Experiment]:
        _ensure_synchronized()
        _check_required_parameters(**dict())
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(4)
        _recv_exception_check()
        return _recv_list(
            elementReceiveFun=lambda: _recv_object(Experiment, nullable=False),
            nullable=False,
        )

    # [[matt.oexp.front.api.OnlineExperiments]]
    def __eq__(self, other):
        _ensure_synchronized()
        if isinstance(other, KBClass):
            _sendall(CHECK_EQUALITY)
            _send_long(self._id._id)
            _send_long(other._id._id)
            return _recv_bool()
        else:
            return False


def experiment_config(
    uid=NO_DEFAULT,
    name=NO_DEFAULT,
    manifests=DEFAULT_VALUE,
    prolific_study_id=DEFAULT_VALUE,
    css=DEFAULT_VALUE,
):
    _check_required_parameters(**dict(uid=uid, name=name))
    return ExperimentConfig(uid, name, manifests, prolific_study_id, css)


# [[matt.oexp.olang.lab.model.ExperimentConfig]]
class ExperimentConfig(KBDClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.lab.model.ExperimentConfig")
            _send_long(args[0]._id._id)
            _send_string(args[1])
            if args[2] == DEFAULT_VALUE:
                _sendall(b"\x00")
            else:
                _sendall(b"\x01")
                if args[2] is None:
                    _sendall(b"\x00")
                else:
                    _sendall(b"\x01")
                if args[2] is not None:
                    _send_int(len(args[2]))
                    for e in args[2]:
                        _send_long(e._id._id)
            if args[3] == DEFAULT_VALUE:
                _sendall(b"\x00")
            else:
                _sendall(b"\x01")
                if args[3] is None:
                    _sendall(b"\x00")
                else:
                    _sendall(b"\x01")
                if args[3] is not None:
                    _send_long(args[3]._id._id)
            if args[4] == DEFAULT_VALUE:
                _sendall(b"\x00")
            else:
                _sendall(b"\x01")
                if args[4] is None:
                    _sendall(b"\x00")
                else:
                    _sendall(b"\x01")
                if args[4] is not None:
                    _send_string(args[4])
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.lab.model.ExperimentConfig#css]]
    @property
    def css(self) -> Optional[str]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_string(nullable=True)
        return temp

    # [[matt.oexp.olang.lab.model.ExperimentConfig#manifestCount]]
    @property
    def manifest_count(self) -> Optional[int]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(1)
        temp = _recv_int(nullable=True)
        return temp

    # [[matt.oexp.olang.lab.model.ExperimentConfig#manifests]]
    @property
    def manifests(self) -> Optional[List[TrialManifest]]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(2)
        temp = _recv_list(
            elementReceiveFun=lambda: _recv_object(TrialManifest, nullable=False),
            nullable=True,
        )
        return temp

    # [[matt.oexp.olang.lab.model.ExperimentConfig#name]]
    @property
    def name(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(3)
        temp = _recv_string(nullable=False)
        return temp

    # [[matt.oexp.olang.lab.model.ExperimentConfig#prolificStudyID]]
    @property
    def prolific_study_id(self) -> Optional[ProlificStudyId]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(4)
        temp = _recv_object(ProlificStudyId, nullable=True)
        return temp

    # [[matt.oexp.olang.lab.model.ExperimentConfig#uid]]
    @property
    def uid(self) -> ExperimentUid:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(5)
        temp = _recv_object(ExperimentUid, nullable=False)
        return temp

    # [[matt.oexp.olang.lab.model.ExperimentConfig#willProvideAManifest]]
    @property
    def will_provide_a_manifest(self) -> bool:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(6)
        temp = _recv_bool(nullable=False)
        return temp

    # [[matt.oexp.olang.lab.model.ExperimentConfig]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.lab.model.ExperimentConfig]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.lab.model.ExperimentConfig]]
    def __eq__(self, other):
        _ensure_synchronized()
        if isinstance(other, KBClass):
            _sendall(CHECK_EQUALITY)
            _send_long(self._id._id)
            _send_long(other._id._id)
            return _recv_bool()
        else:
            return False


def subject(id=NO_DEFAULT, demographic=DEFAULT_VALUE, events=DEFAULT_VALUE):
    _check_required_parameters(**dict(id=id))
    return Subject(id, demographic, events)


# [[matt.oexp.olang.lab.model.Subject]]
class Subject(KBClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.lab.model.Subject")
            _send_long(args[0]._id._id)
            if args[1] == DEFAULT_VALUE:
                _sendall(b"\x00")
            else:
                _sendall(b"\x01")
                _send_int(len(args[1]))
                for e in args[1]:
                    _send_long(e._id._id)
            if args[2] == DEFAULT_VALUE:
                _sendall(b"\x00")
            else:
                _sendall(b"\x01")
                _send_int(len(args[2]))
                for e in args[2]:
                    _send_long(e._id._id)
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.lab.model.Subject#demographic]]
    @property
    def demographic(self) -> List[SubjectDemographicData]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_list(
            elementReceiveFun=lambda: _recv_object(
                SubjectDemographicData, nullable=False
            ),
            nullable=False,
        )
        return temp

    @demographic.setter
    def demographic(self, value) -> List[SubjectDemographicData]:
        _ensure_synchronized()
        _sendall(SET_VAR)
        _send_long(self._id._id)
        _send_int(0)
        _send_int(len(value))
        for e in value:
            _send_long(e._id._id)
        _recv_confirmation()

    # [[matt.oexp.olang.lab.model.Subject#events]]
    @property
    def events(self) -> List[ExperimentEvent]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(1)
        temp = _recv_list(
            elementReceiveFun=lambda: _recv_object(ExperimentEvent, nullable=False),
            nullable=False,
        )
        return temp

    # [[matt.oexp.olang.lab.model.Subject#id]]
    @property
    def id(self) -> ProlificParticipantUid:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(2)
        temp = _recv_object(ProlificParticipantUid, nullable=False)
        return temp

    # [[matt.oexp.olang.lab.model.Subject]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.lab.model.Subject]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.lab.model.Subject]]
    def __eq__(self, other):
        _ensure_synchronized()
        if isinstance(other, KBClass):
            _sendall(CHECK_EQUALITY)
            _send_long(self._id._id)
            _send_long(other._id._id)
            return _recv_bool()
        else:
            return False


def subject_data(data_version=DEFAULT_VALUE, subjects=DEFAULT_VALUE):
    _check_required_parameters(**dict())
    return SubjectData(data_version, subjects)


# [[matt.oexp.olang.lab.model.SubjectData]]
class SubjectData(KBClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.lab.model.SubjectData")
            if args[0] == DEFAULT_VALUE:
                _sendall(b"\x00")
            else:
                _sendall(b"\x01")
                _send_int(args[0])
            if args[1] == DEFAULT_VALUE:
                _sendall(b"\x00")
            else:
                _sendall(b"\x01")
                _send_int(len(args[1]))
                for e in args[1]:
                    _send_long(e._id._id)
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.lab.model.SubjectData#dataVersion]]
    @property
    def data_version(self) -> int:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_int(nullable=False)
        return temp

    # [[matt.oexp.olang.lab.model.SubjectData#subjects]]
    @property
    def subjects(self) -> List[Subject]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(1)
        temp = _recv_list(
            elementReceiveFun=lambda: _recv_object(Subject, nullable=False),
            nullable=False,
        )
        return temp

    # [[matt.oexp.olang.lab.model.SubjectData]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.lab.model.SubjectData]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.lab.model.SubjectData]]
    def __eq__(self, other):
        _ensure_synchronized()
        if isinstance(other, KBClass):
            _sendall(CHECK_EQUALITY)
            _send_long(self._id._id)
            _send_long(other._id._id)
            return _recv_bool()
        else:
            return False


def subject_demographic_data(
    prolific_pid=NO_DEFAULT,
    session_id=DEFAULT_VALUE,
    birth_year=NO_DEFAULT,
    birth_month=NO_DEFAULT,
    gender=NO_DEFAULT,
    ethnicity=NO_DEFAULT,
):
    _check_required_parameters(
        **dict(
            prolific_pid=prolific_pid,
            birth_year=birth_year,
            birth_month=birth_month,
            gender=gender,
            ethnicity=ethnicity,
        )
    )
    return SubjectDemographicData(
        prolific_pid, session_id, birth_year, birth_month, gender, ethnicity
    )


# [[matt.oexp.olang.lab.model.SubjectDemographicData]]
class SubjectDemographicData(KBClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.lab.model.SubjectDemographicData")
            _send_long(args[0]._id._id)
            if args[1] == DEFAULT_VALUE:
                _sendall(b"\x00")
            else:
                _sendall(b"\x01")
                if args[1] is None:
                    _sendall(b"\x00")
                else:
                    _sendall(b"\x01")
                if args[1] is not None:
                    _send_long(args[1]._id._id)
            _send_string(args[2])
            _send_string(args[3])
            _send_string(args[4])
            _send_int(len(args[5]))
            for e in args[5]:
                _send_string(e)
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.lab.model.SubjectDemographicData#birthMonth]]
    @property
    def birth_month(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_string(nullable=False)
        return temp

    # [[matt.oexp.olang.lab.model.SubjectDemographicData#birthYear]]
    @property
    def birth_year(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(1)
        temp = _recv_string(nullable=False)
        return temp

    # [[matt.oexp.olang.lab.model.SubjectDemographicData#ethnicity]]
    @property
    def ethnicity(self) -> List[str]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(2)
        temp = _recv_list(
            elementReceiveFun=lambda: _recv_string(nullable=False), nullable=False
        )
        return temp

    # [[matt.oexp.olang.lab.model.SubjectDemographicData#gender]]
    @property
    def gender(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(3)
        temp = _recv_string(nullable=False)
        return temp

    # [[matt.oexp.olang.lab.model.SubjectDemographicData#prolificPID]]
    @property
    def prolific_pid(self) -> ProlificParticipantUid:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(4)
        temp = _recv_object(ProlificParticipantUid, nullable=False)
        return temp

    # [[matt.oexp.olang.lab.model.SubjectDemographicData#sessionID]]
    @property
    def session_id(self) -> Optional[ProlificSessionId]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(5)
        temp = _recv_object(ProlificSessionId, nullable=True)
        return temp

    # [[matt.oexp.olang.lab.model.SubjectDemographicData]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.lab.model.SubjectDemographicData]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.lab.model.SubjectDemographicData]]
    def __eq__(self, other):
        _ensure_synchronized()
        if isinstance(other, KBClass):
            _sendall(CHECK_EQUALITY)
            _send_long(self._id._id)
            _send_long(other._id._id)
            return _recv_bool()
        else:
            return False


def trial(query=NO_DEFAULT, distractors=NO_DEFAULT):
    _check_required_parameters(**dict(query=query, distractors=distractors))
    return Trial(query, distractors)


# [[matt.oexp.olang.lab.model.Trial]]
class Trial(KBDClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.lab.model.Trial")
            _send_string(args[0])
            _send_int(len(args[1]))
            for e in args[1]:
                _send_string(e)
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.lab.model.Trial#distractors]]
    @property
    def distractors(self) -> List[str]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_list(
            elementReceiveFun=lambda: _recv_string(nullable=False), nullable=False
        )
        return temp

    # [[matt.oexp.olang.lab.model.Trial#query]]
    @property
    def query(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(1)
        temp = _recv_string(nullable=False)
        return temp

    # [[matt.oexp.olang.lab.model.Trial]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.lab.model.Trial]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.lab.model.Trial]]
    def __eq__(self, other):
        _ensure_synchronized()
        if isinstance(other, KBClass):
            _sendall(CHECK_EQUALITY)
            _send_long(self._id._id)
            _send_long(other._id._id)
            return _recv_bool()
        else:
            return False


def trial_manifest(trials=NO_DEFAULT, skip=DEFAULT_VALUE):
    _check_required_parameters(**dict(trials=trials))
    return TrialManifest(trials, skip)


# [[matt.oexp.olang.lab.model.TrialManifest]]
class TrialManifest(KBDClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.lab.model.TrialManifest")
            _send_int(len(args[0]))
            for e in args[0]:
                _send_long(e._id._id)
            if args[1] == DEFAULT_VALUE:
                _sendall(b"\x00")
            else:
                _sendall(b"\x01")
                if args[1]:
                    _sendall(b"\x01")
                else:
                    _sendall(b"\x00")
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.lab.model.TrialManifest#skip]]
    @property
    def skip(self) -> bool:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_bool(nullable=False)
        return temp

    # [[matt.oexp.olang.lab.model.TrialManifest#trials]]
    @property
    def trials(self) -> List[Trial]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(1)
        temp = _recv_list(
            elementReceiveFun=lambda: _recv_object(Trial, nullable=False),
            nullable=False,
        )
        return temp

    # [[matt.oexp.olang.lab.model.TrialManifest]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.lab.model.TrialManifest]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.lab.model.TrialManifest]]
    def __eq__(self, other):
        _ensure_synchronized()
        if isinstance(other, KBClass):
            _sendall(CHECK_EQUALITY)
            _send_long(self._id._id)
            _send_long(other._id._id)
            return _recv_bool()
        else:
            return False


def encrypted_stimulus_path(cipher_path=NO_DEFAULT):
    _check_required_parameters(**dict(cipher_path=cipher_path))
    return EncryptedStimulusPath(cipher_path)


# [[matt.oexp.olang.model.EncryptedStimulusPath]]
class EncryptedStimulusPath(KBVClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.model.EncryptedStimulusPath")
            _send_string(args[0])
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.model.EncryptedStimulusPath#cipherPath]]
    @property
    def cipher_path(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_string(nullable=False)
        return temp

    # [[matt.oexp.olang.model.EncryptedStimulusPath]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.EncryptedStimulusPath]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.model.EncryptedStimulusPath]]
    def __eq__(self, other):
        _ensure_synchronized()
        return type(other) == type(self) and other.cipher_path == self.cipher_path


# [[matt.oexp.olang.model.ExperimentEvent]]
class ExperimentEvent(KBClass, abc.ABC):
    # [[matt.oexp.olang.model.ExperimentEvent#expUID]]
    @property
    @abc.abstractmethod
    def exp_uid(self) -> ExperimentUid:
        pass

    # [[matt.oexp.olang.model.ExperimentEvent#pid]]
    @property
    @abc.abstractmethod
    def pid(self) -> ProlificParticipantUid:
        pass

    # [[matt.oexp.olang.model.ExperimentEvent#sessionID]]
    @property
    @abc.abstractmethod
    def session_id(self) -> ProlificSessionId:
        pass

    # [[matt.oexp.olang.model.ExperimentEvent#sessionNumber]]
    @property
    @abc.abstractmethod
    def session_number(self) -> SessionNumber:
        pass

    # [[matt.oexp.olang.model.ExperimentEvent]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.ExperimentEvent]]
    def to_dict(self):
        return json.loads(self.to_json())


def experiment_start(
    pid=NO_DEFAULT,
    session_id=NO_DEFAULT,
    unix_time_millis=NO_DEFAULT,
    session_number=NO_DEFAULT,
    exp_uid=NO_DEFAULT,
    query_params=DEFAULT_VALUE,
):
    _check_required_parameters(
        **dict(
            pid=pid,
            session_id=session_id,
            unix_time_millis=unix_time_millis,
            session_number=session_number,
            exp_uid=exp_uid,
        )
    )
    return ExperimentStart(
        pid, session_id, unix_time_millis, session_number, exp_uid, query_params
    )


# [[matt.oexp.olang.model.ExperimentStart]]
class ExperimentStart(ExperimentEvent, KBClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.model.ExperimentStart")
            _send_long(args[0]._id._id)
            _send_long(args[1]._id._id)
            _send_long(args[2])
            _send_long(args[3]._id._id)
            _send_long(args[4]._id._id)
            if args[5] == DEFAULT_VALUE:
                _sendall(b"\x00")
            else:
                _sendall(b"\x01")
                if args[5] is None:
                    _sendall(b"\x00")
                else:
                    _sendall(b"\x01")
                if args[5] is not None:
                    _send_int(len(args[5]))
                    for k, v in args[5].items():
                        _send_string(k)
                        _send_string(v)
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.model.ExperimentStart#expUID]]
    @property
    def exp_uid(self) -> ExperimentUid:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_object(ExperimentUid, nullable=False)
        return temp

    # [[matt.oexp.olang.model.ExperimentStart#pid]]
    @property
    def pid(self) -> ProlificParticipantUid:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(1)
        temp = _recv_object(ProlificParticipantUid, nullable=False)
        return temp

    # [[matt.oexp.olang.model.ExperimentStart#queryParams]]
    @property
    def query_params(self) -> Optional[Dict[str, str]]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(2)
        temp = _recv_map(
            keyReceiveFun=lambda: _recv_string(nullable=False),
            valueReceiveFun=lambda: _recv_string(nullable=False),
            nullable=True,
        )
        return temp

    # [[matt.oexp.olang.model.ExperimentStart#sessionID]]
    @property
    def session_id(self) -> ProlificSessionId:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(3)
        temp = _recv_object(ProlificSessionId, nullable=False)
        return temp

    # [[matt.oexp.olang.model.ExperimentStart#sessionNumber]]
    @property
    def session_number(self) -> SessionNumber:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(4)
        temp = _recv_object(SessionNumber, nullable=False)
        return temp

    # [[matt.oexp.olang.model.ExperimentStart#unixTimeMillis]]
    @property
    def unix_time_millis(self) -> int:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(5)
        temp = _recv_long(nullable=False)
        return temp

    # [[matt.oexp.olang.model.ExperimentStart]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.ExperimentStart]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.model.ExperimentStart]]
    def __eq__(self, other):
        _ensure_synchronized()
        if isinstance(other, KBClass):
            _sendall(CHECK_EQUALITY)
            _send_long(self._id._id)
            _send_long(other._id._id)
            return _recv_bool()
        else:
            return False


def experiment_uid(uid=NO_DEFAULT):
    _check_required_parameters(**dict(uid=uid))
    return ExperimentUid(uid)


# [[matt.oexp.olang.model.ExperimentUID]]
class ExperimentUid(KBVClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.model.ExperimentUID")
            _send_long(args[0])
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.model.ExperimentUID#uid]]
    @property
    def uid(self) -> int:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_long(nullable=False)
        return temp

    # [[matt.oexp.olang.model.ExperimentUID]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.ExperimentUID]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.model.ExperimentUID]]
    def __eq__(self, other):
        _ensure_synchronized()
        return type(other) == type(self) and other.uid == self.uid


def manifest_number(num=NO_DEFAULT):
    _check_required_parameters(**dict(num=num))
    return ManifestNumber(num)


# [[matt.oexp.olang.model.ManifestNumber]]
class ManifestNumber(KBVClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.model.ManifestNumber")
            _send_int(args[0])
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.model.ManifestNumber#num]]
    @property
    def num(self) -> int:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_int(nullable=False)
        return temp

    # [[matt.oexp.olang.model.ManifestNumber]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.ManifestNumber]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.model.ManifestNumber]]
    def __eq__(self, other):
        _ensure_synchronized()
        return type(other) == type(self) and other.num == self.num


def prolific_participant_uid(pid=NO_DEFAULT):
    _check_required_parameters(**dict(pid=pid))
    return ProlificParticipantUid(pid)


# [[matt.oexp.olang.model.ProlificParticipantUid]]
class ProlificParticipantUid(KBVClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.model.ProlificParticipantUid")
            _send_string(args[0])
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.model.ProlificParticipantUid#pid]]
    @property
    def pid(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_string(nullable=False)
        return temp

    # [[matt.oexp.olang.model.ProlificParticipantUid#isPilot]]
    def is_pilot(self) -> bool:
        _ensure_synchronized()
        _check_required_parameters(**dict())
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(0)
        _recv_exception_check()
        return _recv_bool(nullable=False)

    # [[matt.oexp.olang.model.ProlificParticipantUid#isTest]]
    def is_test(self) -> bool:
        _ensure_synchronized()
        _check_required_parameters(**dict())
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(1)
        _recv_exception_check()
        return _recv_bool(nullable=False)

    # [[matt.oexp.olang.model.ProlificParticipantUid]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.ProlificParticipantUid]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.model.ProlificParticipantUid]]
    def __eq__(self, other):
        _ensure_synchronized()
        return type(other) == type(self) and other.pid == self.pid


def prolific_session_id(id=NO_DEFAULT):
    _check_required_parameters(**dict(id=id))
    return ProlificSessionId(id)


# [[matt.oexp.olang.model.ProlificSessionId]]
class ProlificSessionId(KBVClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.model.ProlificSessionId")
            _send_string(args[0])
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.model.ProlificSessionId#id]]
    @property
    def id(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_string(nullable=False)
        return temp

    # [[matt.oexp.olang.model.ProlificSessionId#isPilot]]
    def is_pilot(self) -> bool:
        _ensure_synchronized()
        _check_required_parameters(**dict())
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(0)
        _recv_exception_check()
        return _recv_bool(nullable=False)

    # [[matt.oexp.olang.model.ProlificSessionId#isTest]]
    def is_test(self) -> bool:
        _ensure_synchronized()
        _check_required_parameters(**dict())
        _sendall(CALL_FUN)
        _send_long(self._id._id)
        _send_int(1)
        _recv_exception_check()
        return _recv_bool(nullable=False)

    # [[matt.oexp.olang.model.ProlificSessionId]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.ProlificSessionId]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.model.ProlificSessionId]]
    def __eq__(self, other):
        _ensure_synchronized()
        return type(other) == type(self) and other.id == self.id


def prolific_study_id(id=NO_DEFAULT):
    _check_required_parameters(**dict(id=id))
    return ProlificStudyId(id)


# [[matt.oexp.olang.model.ProlificStudyID]]
class ProlificStudyId(KBVClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.model.ProlificStudyID")
            _send_string(args[0])
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.model.ProlificStudyID#id]]
    @property
    def id(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_string(nullable=False)
        return temp

    # [[matt.oexp.olang.model.ProlificStudyID]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.ProlificStudyID]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.model.ProlificStudyID]]
    def __eq__(self, other):
        _ensure_synchronized()
        return type(other) == type(self) and other.id == self.id


def session_number(num=NO_DEFAULT):
    _check_required_parameters(**dict(num=num))
    return SessionNumber(num)


# [[matt.oexp.olang.model.SessionNumber]]
class SessionNumber(KBVClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.model.SessionNumber")
            _send_long(args[0])
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.model.SessionNumber#num]]
    @property
    def num(self) -> int:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_long(nullable=False)
        return temp

    # [[matt.oexp.olang.model.SessionNumber]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.SessionNumber]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.model.SessionNumber]]
    def __eq__(self, other):
        _ensure_synchronized()
        return type(other) == type(self) and other.num == self.num


# [[matt.oexp.olang.model.SubjectTrialEvent]]
class SubjectTrialEvent(KBClass, abc.ABC):
    # [[matt.oexp.olang.model.SubjectTrialEvent#timeMillis]]
    @property
    @abc.abstractmethod
    def time_millis(self) -> int:
        pass

    # [[matt.oexp.olang.model.SubjectTrialEvent]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.SubjectTrialEvent]]
    def to_dict(self):
        return json.loads(self.to_json())


def temporary_encrypted_stimulus(path=NO_DEFAULT, temp_url=NO_DEFAULT):
    _check_required_parameters(**dict(path=path, temp_url=temp_url))
    return TemporaryEncryptedStimulus(path, temp_url)


# [[matt.oexp.olang.model.TemporaryEncryptedStimulus]]
class TemporaryEncryptedStimulus(KBClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.model.TemporaryEncryptedStimulus")
            _send_long(args[0]._id._id)
            _send_string(args[1])
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.model.TemporaryEncryptedStimulus#path]]
    @property
    def path(self) -> EncryptedStimulusPath:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_object(EncryptedStimulusPath, nullable=False)
        return temp

    # [[matt.oexp.olang.model.TemporaryEncryptedStimulus#tempURL]]
    @property
    def temp_url(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(1)
        temp = _recv_string(nullable=False)
        return temp

    # [[matt.oexp.olang.model.TemporaryEncryptedStimulus#url]]
    @property
    def url(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(2)
        temp = _recv_string(nullable=False)
        return temp

    # [[matt.oexp.olang.model.TemporaryEncryptedStimulus]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.TemporaryEncryptedStimulus]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.model.TemporaryEncryptedStimulus]]
    def __eq__(self, other):
        _ensure_synchronized()
        if isinstance(other, KBClass):
            _sendall(CHECK_EQUALITY)
            _send_long(self._id._id)
            _send_long(other._id._id)
            return _recv_bool()
        else:
            return False


# [[matt.oexp.olang.model.TrialData]]
class TrialData(ExperimentEvent, KBClass, abc.ABC):
    # [[matt.oexp.olang.model.TrialData#distractors]]
    @property
    @abc.abstractmethod
    def distractors(self) -> List[S]:
        pass

    # [[matt.oexp.olang.model.TrialData#log]]
    @property
    @abc.abstractmethod
    def log(self) -> List[SubjectTrialEvent]:
        pass

    # [[matt.oexp.olang.model.TrialData#pid]]
    @property
    @abc.abstractmethod
    def pid(self) -> ProlificParticipantUid:
        pass

    # [[matt.oexp.olang.model.TrialData#selectionIndices]]
    @property
    @abc.abstractmethod
    def selection_indices(self) -> List[int]:
        pass

    # [[matt.oexp.olang.model.TrialData#sessionID]]
    @property
    @abc.abstractmethod
    def session_id(self) -> ProlificSessionId:
        pass

    # [[matt.oexp.olang.model.TrialData#sessionNumber]]
    @property
    @abc.abstractmethod
    def session_number(self) -> SessionNumber:
        pass

    # [[matt.oexp.olang.model.TrialData#startTimeUnixMillis]]
    @property
    @abc.abstractmethod
    def start_time_unix_millis(self) -> int:
        pass

    # [[matt.oexp.olang.model.TrialData#target]]
    @property
    @abc.abstractmethod
    def target(self) -> S:
        pass

    @target.setter
    @abc.abstractmethod
    def target(self, value) -> S:
        pass

    # [[matt.oexp.olang.model.TrialData#trialIndex]]
    @property
    @abc.abstractmethod
    def trial_index(self) -> int:
        pass

    # [[matt.oexp.olang.model.TrialData#expUID]]
    @property
    @abc.abstractmethod
    def exp_uid(self) -> ExperimentUid:
        pass


def completion_code(code=NO_DEFAULT, code_type=NO_DEFAULT, actions=NO_DEFAULT):
    _check_required_parameters(**dict(code=code, code_type=code_type, actions=actions))
    return CompletionCode(code, code_type, actions)


# [[matt.oexp.olang.model.prolific.CompletionCode]]
class CompletionCode(KBDClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.model.prolific.CompletionCode")
            _send_string(args[0])
            _send_string(args[1])
            _send_int(len(args[2]))
            for e in args[2]:
                _send_int(len(e))
                for k, v in e.items():
                    _send_string(k)
                    _send_string(v)
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.model.prolific.CompletionCode#actions]]
    @property
    def actions(self) -> List[Dict[str, str]]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_list(
            elementReceiveFun=lambda: _recv_map(
                keyReceiveFun=lambda: _recv_string(nullable=False),
                valueReceiveFun=lambda: _recv_string(nullable=False),
                nullable=False,
            ),
            nullable=False,
        )
        return temp

    # [[matt.oexp.olang.model.prolific.CompletionCode#code]]
    @property
    def code(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(1)
        temp = _recv_string(nullable=False)
        return temp

    # [[matt.oexp.olang.model.prolific.CompletionCode#code_type]]
    @property
    def code_type(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(2)
        temp = _recv_string(nullable=False)
        return temp

    # [[matt.oexp.olang.model.prolific.CompletionCode]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.prolific.CompletionCode]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.model.prolific.CompletionCode]]
    def __eq__(self, other):
        _ensure_synchronized()
        if isinstance(other, KBClass):
            _sendall(CHECK_EQUALITY)
            _send_long(self._id._id)
            _send_long(other._id._id)
            return _recv_bool()
        else:
            return False


# [[matt.oexp.olang.model.prolific.CompletionOption]]
class CompletionOption(Enum):
    url = 0
    code = 1
    # [[matt.oexp.olang.model.prolific.CompletionOption]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.prolific.CompletionOption]]
    def to_dict(self):
        return json.loads(self.to_json())


def prolific_study_data(
    external_study_url=NO_DEFAULT,
    completion_option=NO_DEFAULT,
    completion_codes=NO_DEFAULT,
):
    _check_required_parameters(
        **dict(
            external_study_url=external_study_url,
            completion_option=completion_option,
            completion_codes=completion_codes,
        )
    )
    return ProlificStudyData(external_study_url, completion_option, completion_codes)


# [[matt.oexp.olang.model.prolific.ProlificStudyData]]
class ProlificStudyData(KBDClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.model.prolific.ProlificStudyData")
            _send_string(args[0])
            _send_short(args[1].value)
            _send_int(len(args[2]))
            for e in args[2]:
                _send_long(e._id._id)
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.model.prolific.ProlificStudyData#completion_codes]]
    @property
    def completion_codes(self) -> List[CompletionCode]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_list(
            elementReceiveFun=lambda: _recv_object(CompletionCode, nullable=False),
            nullable=False,
        )
        return temp

    # [[matt.oexp.olang.model.prolific.ProlificStudyData#completion_option]]
    @property
    def completion_option(self) -> CompletionOption:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(1)
        temp = _recv_enum(CompletionOption, nullable=False)
        return temp

    # [[matt.oexp.olang.model.prolific.ProlificStudyData#external_study_url]]
    @property
    def external_study_url(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(2)
        temp = _recv_string(nullable=False)
        return temp

    # [[matt.oexp.olang.model.prolific.ProlificStudyData]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.prolific.ProlificStudyData]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.model.prolific.ProlificStudyData]]
    def __eq__(self, other):
        _ensure_synchronized()
        if isinstance(other, KBClass):
            _sendall(CHECK_EQUALITY)
            _send_long(self._id._id)
            _send_long(other._id._id)
            return _recv_bool()
        else:
            return False


def button_event(time_millis=NO_DEFAULT, button=NO_DEFAULT):
    _check_required_parameters(**dict(time_millis=time_millis, button=button))
    return ButtonEvent(time_millis, button)


# [[matt.oexp.olang.model.ButtonEvent]]
class ButtonEvent(SubjectTrialEvent, KBClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.model.ButtonEvent")
            _send_int(args[0])
            _send_string(args[1])
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.model.ButtonEvent#button]]
    @property
    def button(self) -> str:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_string(nullable=False)
        return temp

    # [[matt.oexp.olang.model.ButtonEvent#timeMillis]]
    @property
    def time_millis(self) -> int:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(1)
        temp = _recv_int(nullable=False)
        return temp

    # [[matt.oexp.olang.model.ButtonEvent]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.ButtonEvent]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.model.ButtonEvent]]
    def __eq__(self, other):
        _ensure_synchronized()
        if isinstance(other, KBClass):
            _sendall(CHECK_EQUALITY)
            _send_long(self._id._id)
            _send_long(other._id._id)
            return _recv_bool()
        else:
            return False


def encrypted_subject_trial_data(
    pid=NO_DEFAULT,
    session_number=NO_DEFAULT,
    session_id=NO_DEFAULT,
    trial_index=NO_DEFAULT,
    target=NO_DEFAULT,
    distractors=NO_DEFAULT,
    selection_indices=DEFAULT_VALUE,
    start_time_unix_millis=NO_DEFAULT,
    log=DEFAULT_VALUE,
    exp_uid=NO_DEFAULT,
):
    _check_required_parameters(
        **dict(
            pid=pid,
            session_number=session_number,
            session_id=session_id,
            trial_index=trial_index,
            target=target,
            distractors=distractors,
            start_time_unix_millis=start_time_unix_millis,
            exp_uid=exp_uid,
        )
    )
    return EncryptedSubjectTrialData(
        pid,
        session_number,
        session_id,
        trial_index,
        target,
        distractors,
        selection_indices,
        start_time_unix_millis,
        log,
        exp_uid,
    )


# [[matt.oexp.olang.model.EncryptedSubjectTrialData]]
class EncryptedSubjectTrialData(TrialData, ExperimentEvent, KBDClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.model.EncryptedSubjectTrialData")
            _send_long(args[0]._id._id)
            _send_long(args[1]._id._id)
            _send_long(args[2]._id._id)
            _send_int(args[3])
            _send_long(args[4]._id._id)
            _send_int(len(args[5]))
            for e in args[5]:
                _send_long(e._id._id)
            if args[6] == DEFAULT_VALUE:
                _sendall(b"\x00")
            else:
                _sendall(b"\x01")
                _send_int(len(args[6]))
                for e in args[6]:
                    _send_int(e)
            _send_long(args[7])
            if args[8] == DEFAULT_VALUE:
                _sendall(b"\x00")
            else:
                _sendall(b"\x01")
                _send_int(len(args[8]))
                for e in args[8]:
                    _send_long(e._id._id)
            _send_long(args[9]._id._id)
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.model.EncryptedSubjectTrialData#distractors]]
    @property
    def distractors(self) -> List[TemporaryEncryptedStimulus]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_list(
            elementReceiveFun=lambda: _recv_object(
                TemporaryEncryptedStimulus, nullable=False
            ),
            nullable=False,
        )
        return temp

    # [[matt.oexp.olang.model.EncryptedSubjectTrialData#expUID]]
    @property
    def exp_uid(self) -> ExperimentUid:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(1)
        temp = _recv_object(ExperimentUid, nullable=False)
        return temp

    # [[matt.oexp.olang.model.EncryptedSubjectTrialData#log]]
    @property
    def log(self) -> List[SubjectTrialEvent]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(2)
        temp = _recv_list(
            elementReceiveFun=lambda: _recv_object(SubjectTrialEvent, nullable=False),
            nullable=False,
        )
        return temp

    # [[matt.oexp.olang.model.EncryptedSubjectTrialData#pid]]
    @property
    def pid(self) -> ProlificParticipantUid:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(3)
        temp = _recv_object(ProlificParticipantUid, nullable=False)
        return temp

    # [[matt.oexp.olang.model.EncryptedSubjectTrialData#selectionIndices]]
    @property
    def selection_indices(self) -> List[int]:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(4)
        temp = _recv_list(
            elementReceiveFun=lambda: _recv_int(nullable=False), nullable=False
        )
        return temp

    # [[matt.oexp.olang.model.EncryptedSubjectTrialData#sessionID]]
    @property
    def session_id(self) -> ProlificSessionId:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(5)
        temp = _recv_object(ProlificSessionId, nullable=False)
        return temp

    # [[matt.oexp.olang.model.EncryptedSubjectTrialData#sessionNumber]]
    @property
    def session_number(self) -> SessionNumber:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(6)
        temp = _recv_object(SessionNumber, nullable=False)
        return temp

    # [[matt.oexp.olang.model.EncryptedSubjectTrialData#startTimeUnixMillis]]
    @property
    def start_time_unix_millis(self) -> int:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(7)
        temp = _recv_long(nullable=False)
        return temp

    # [[matt.oexp.olang.model.EncryptedSubjectTrialData#target]]
    @property
    def target(self) -> TemporaryEncryptedStimulus:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(8)
        temp = _recv_object(TemporaryEncryptedStimulus, nullable=False)
        return temp

    @target.setter
    def target(self, value) -> TemporaryEncryptedStimulus:
        _ensure_synchronized()
        _sendall(SET_VAR)
        _send_long(self._id._id)
        _send_int(8)
        _send_long(value._id._id)
        _recv_confirmation()

    # [[matt.oexp.olang.model.EncryptedSubjectTrialData#trialIndex]]
    @property
    def trial_index(self) -> int:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(9)
        temp = _recv_int(nullable=False)
        return temp

    # [[matt.oexp.olang.model.EncryptedSubjectTrialData]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.EncryptedSubjectTrialData]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.model.EncryptedSubjectTrialData]]
    def __eq__(self, other):
        _ensure_synchronized()
        if isinstance(other, KBClass):
            _sendall(CHECK_EQUALITY)
            _send_long(self._id._id)
            _send_long(other._id._id)
            return _recv_bool()
        else:
            return False


def exit_full_screen_event(
    pid=NO_DEFAULT,
    session_id=NO_DEFAULT,
    unix_time_millis=NO_DEFAULT,
    session_number=NO_DEFAULT,
    exp_uid=NO_DEFAULT,
):
    _check_required_parameters(
        **dict(
            pid=pid,
            session_id=session_id,
            unix_time_millis=unix_time_millis,
            session_number=session_number,
            exp_uid=exp_uid,
        )
    )
    return ExitFullScreenEvent(
        pid, session_id, unix_time_millis, session_number, exp_uid
    )


# [[matt.oexp.olang.model.ExitFullScreenEvent]]
class ExitFullScreenEvent(ExperimentEvent, KBClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.model.ExitFullScreenEvent")
            _send_long(args[0]._id._id)
            _send_long(args[1]._id._id)
            _send_long(args[2])
            _send_long(args[3]._id._id)
            _send_long(args[4]._id._id)
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.model.ExitFullScreenEvent#expUID]]
    @property
    def exp_uid(self) -> ExperimentUid:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_object(ExperimentUid, nullable=False)
        return temp

    # [[matt.oexp.olang.model.ExitFullScreenEvent#pid]]
    @property
    def pid(self) -> ProlificParticipantUid:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(1)
        temp = _recv_object(ProlificParticipantUid, nullable=False)
        return temp

    # [[matt.oexp.olang.model.ExitFullScreenEvent#sessionID]]
    @property
    def session_id(self) -> ProlificSessionId:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(2)
        temp = _recv_object(ProlificSessionId, nullable=False)
        return temp

    # [[matt.oexp.olang.model.ExitFullScreenEvent#sessionNumber]]
    @property
    def session_number(self) -> SessionNumber:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(3)
        temp = _recv_object(SessionNumber, nullable=False)
        return temp

    # [[matt.oexp.olang.model.ExitFullScreenEvent#unixTimeMillis]]
    @property
    def unix_time_millis(self) -> int:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(4)
        temp = _recv_long(nullable=False)
        return temp

    # [[matt.oexp.olang.model.ExitFullScreenEvent]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.ExitFullScreenEvent]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.model.ExitFullScreenEvent]]
    def __eq__(self, other):
        _ensure_synchronized()
        if isinstance(other, KBClass):
            _sendall(CHECK_EQUALITY)
            _send_long(self._id._id)
            _send_long(other._id._id)
            return _recv_bool()
        else:
            return False


def selection_event(
    time_millis=NO_DEFAULT, selection_index=NO_DEFAULT, distractor_index=NO_DEFAULT
):
    _check_required_parameters(
        **dict(
            time_millis=time_millis,
            selection_index=selection_index,
            distractor_index=distractor_index,
        )
    )
    return SelectionEvent(time_millis, selection_index, distractor_index)


# [[matt.oexp.olang.model.SelectionEvent]]
class SelectionEvent(SubjectTrialEvent, KBClass):
    def __init__(self, *args, _id=None):
        _ensure_synchronized()
        if _id is None:
            jbridge._init_java()
            _sendall(CREATE_OBJECT)
            _send_string("matt.oexp.olang.model.SelectionEvent")
            _send_int(args[0])
            _send_int(args[1])
            _send_int(args[2])
            self._id = _object_id(_recv_long())
        else:
            self._id = _object_id(_id)

    # [[matt.oexp.olang.model.SelectionEvent#distractorIndex]]
    @property
    def distractor_index(self) -> int:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(0)
        temp = _recv_int(nullable=False)
        return temp

    # [[matt.oexp.olang.model.SelectionEvent#selectionIndex]]
    @property
    def selection_index(self) -> int:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(1)
        temp = _recv_int(nullable=False)
        return temp

    # [[matt.oexp.olang.model.SelectionEvent#timeMillis]]
    @property
    def time_millis(self) -> int:
        _ensure_synchronized()
        _sendall(GET_VAL)
        _send_long(self._id._id)
        _send_int(2)
        temp = _recv_int(nullable=False)
        return temp

    # [[matt.oexp.olang.model.SelectionEvent]]
    def to_json(self):
        _ensure_synchronized()
        _sendall(GET_JSON)
        _send_long(self._id._id)
        return _recv_string(nullable=False)

    # [[matt.oexp.olang.model.SelectionEvent]]
    def to_dict(self):
        return json.loads(self.to_json())

    # [[matt.oexp.olang.model.SelectionEvent]]
    def __eq__(self, other):
        _ensure_synchronized()
        if isinstance(other, KBClass):
            _sendall(CHECK_EQUALITY)
            _send_long(self._id._id)
            _send_long(other._id._id)
            return _recv_bool()
        else:
            return False
