from abc import abstractmethod, ABCMeta
from codecs import iterencode, encode
from collections import deque, namedtuple
from contextlib import contextmanager
from itertools import islice
from logging import getLogger, INFO
from math import inf, isnan, copysign
from typing import Union, Any, Callable, Iterable, NoReturn, TypeVar, Sequence, cast, Tuple, List
from sys import float_info
import re
import types

EllipsisType = Any

class TemperComparable(metaclass=ABCMeta):
    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __le__(self, other: "C") -> bool:
        pass

    @abstractmethod
    def __lt__(self, other: "C") -> bool:
        pass

    @abstractmethod
    def __ge__(self, other: "C") -> bool:
        pass

    @abstractmethod
    def __gt__(self, other: "C") -> bool:
        pass

T = TypeVar("T")
C = TypeVar("C", bool, int, str, float, TemperComparable)

class NoResultException(Exception):
    def __init__(self, message="NO_RESULT"):
        Exception.__init__(self, message)


class TemperObject(object):
    "All user-defined classes include this marker class."


class TemperEnum(TemperObject):
    "Enum classes are user-defined classes additionally with this marker."


def get_static(reified_type, symbol=None) -> NoReturn:
    "There's no way to extract the class from a reified type at this time."
    raise NoResultException()


def temper_print(value: Any):
    "Temper semantics for printing."
    try:
        if isinstance(value, str):
            print(value)
        else:
            print(repr(value))
        return None
    except Exception:
        raise NoResultException()


class LoggingConsole(object):
    """One class per file to log data to the console."""

    def __init__(self, name: str):
        self.logger = getLogger(name)

    def log(self, message: str) -> None:
        self.logger.log(INFO, message)


def str_cat(*parts: str) -> str:
    "Concatenate parts into a single string."
    return "".join(map(str, parts))


def no_result() -> NoResultException:
    raise NoResultException()


def float_cmp(left: float, right: float):
    if left == 0 and right == 0:
        left_float = copysign(1.0, left)
        right_float = copysign(1.0, right)
        return (left_float > right_float) - (left_float < right_float)
    return (left > right) - (left < right)


def float_eq(left: float, right: float):
    return left == right and copysign(1.0, left) == copysign(1.0, right)


def float_not_eq(left: float, right: float):
    return left != right or copysign(1.0, left) != copysign(1.0, right)


def float_lt_eq(left: float, right: float) -> bool:
    return float_cmp(left, right) <= 0


def float_lt(left: float, right: float) -> bool:
    return float_cmp(left, right) < 0


def float_gt_eq(left: float, right: float) -> bool:
    return float_cmp(left, right) >= 0


def float_gt(left: float, right: float) -> bool:
    return float_cmp(left, right) > 0


def generic_cmp(left: C, right: C) -> int:
    if isinstance(left, float) and isinstance(right, float):
        return float_cmp(left, right)
    return (left > right) - (left < right)


def generic_eq(left: T, right: T) -> bool:
    if isinstance(left, float) and isinstance(right, float):
        return float_eq(left, right)
    return left == right


def generic_not_eq(left: T, right: T) -> bool:
    if isinstance(left, float) and isinstance(right, float):
        return float_not_eq(left, right)
    return left != right


def generic_lt_eq(left: C, right: C) -> bool:
    if isinstance(left, float) and isinstance(right, float):
        return float_lt_eq(left, right)
    return left <= right


def generic_lt(left: C, right: C) -> bool:
    if isinstance(left, float) and isinstance(right, float):
        return float_lt(left, right)
    return left < right


def generic_gt_eq(left: C, right: C) -> bool:
    if isinstance(left, float) and isinstance(right, float):
        return float_gt_eq(left, right)
    return left >= right


def generic_gt(left: C, right: C) -> bool:
    if isinstance(left, float) and isinstance(right, float):
        return float_gt(left, right)
    return left > right


def bool_not(value: bool) -> bool:
    return not value


def arith_int_div(dividend: int, divisor: int) -> int:
    try:
        return dividend // divisor
    except ArithmeticError:
        raise NoResultException()


def arith_dub_div(dividend: float, divisor: float) -> float:
    try:
        return dividend / divisor
    except ArithmeticError:
        raise NoResultException()



def arith_int_mod(dividend: int, divisor: int) -> int:
    try:
        return dividend % divisor
    except ArithmeticError:
        raise NoResultException()


def arith_dub_mod(dividend: float, divisor: float) -> float:
    try:
        return dividend % divisor
    except ArithmeticError:
        raise NoResultException()


def isinstance_int(val: Any) -> bool:
    "Python bool is a subclass of int, but Temper treats them as separate types."
    return isinstance(val, int) and not isinstance(val, bool)


def isinstance_char(val: Any) -> bool:
    "Temper char are represented as single character strings."
    return isinstance(val, str) and len(val) == 1


def cast_none(val: Any):
    if isinstance(val, type(None)):
        raise NoResultException()
    return val


def cast_by_type(val: Any, py_type: type):
    "Cast to a python type by an isinstance check."
    if not isinstance(val, py_type):
        raise NoResultException()
    return val


def cast_by_test(val, predicate: Callable[[Any], bool]) -> Any:
    "This cast validates that a temper function meets some predicate, e.g. callable."
    if not predicate(val):
        raise NoResultException()
    return val


class Nexter(object):
    "Construct a consumer function that calls next on an iterator; mimics the javascript generator interface."
    __slots__ = ("_iterator", "value", "done")

    def __init__(self, iterable):
        self._iterator = iter(iterable())
        self.value = None
        self.done = False

    def __call__(self):
        if not self.done:
            try:
                self.value = next(self._iterator)
            except NoResultException as e:
                self.done = True
                raise e
            except StopIteration:
                self.done = True
                raise NoResultException()
        return self


class Label(BaseException):
    "A label enables labled breaks with reasonably readable python"
    __slots__ = ()

    def __enter__(self) -> "Label":
        return self

    def continue_(self) -> "Label":
        raise self

    def break_(self) -> "Label":
        raise self

    def __exit__(self, _exc_type: type, exc: BaseException, _traceback: Any) -> bool:
        return exc is self


class LabelPair(BaseException):
    "Handles an edge case in the semantics of labeled breaks."
    __slots__ = ("continuing",)
    continuing: "InnerLabel"

    def __init__(self):
        self.continuing = InnerLabel()

    def __enter__(self) -> "LabelPair":
        return self

    def break_(self) -> "LabelPair":
        raise self

    def continue_(self) -> "InnerLabel":
        raise self.continuing

    def __exit__(self, _exc_type: type, exc: BaseException, _exc_tb: Any) -> bool:
        return exc is self


class InnerLabel(BaseException):
    __slots__ = ()

    def __enter__(self):
        return None

    def __exit__(self, exc_type: type, exc_val: BaseException, exc_tb: Any) -> bool:
        return exc_val is self


class Symbol(object):
    __slots__ = ("_text",)
    _text: str

    def __init__(self, text):
        self._text = text

    @property
    def text(self) -> str:
        return self._text

    def __eq__(self, other) -> bool:
        if isinstance(other, Symbol):
            raise NotImplementedError()
        return self._text == other._text

    def __hash__(self) -> int:
        return hash(self._text)

    def __repr__(self) -> str:
        return "symbol({!r})".format(self._text)

    def __str__(self) -> str:
        return self._text


class StringSlice(object):
    __slots__ = ()

    def __iter__(self):
        raise NotImplementedError()

    def advance(self, count):
        raise NotImplementedError()

    def _left_plus(self, count):
        raise NotImplementedError()

    def __bool__(self) -> bool:
        raise NotImplementedError()

    def __len__(self) -> int:
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()

    def has_at_least(self, count):
        return count <= 0 or self._left_plus(count) != -1

    def read(self):
        try:
            return next(iter(self))
        except StopIteration:
            raise NoResultException()

    @property
    def length(self) -> int:
        return len(self)

    def to_string(self) -> str:
        return str(self)

    @property
    def is_empty(self) -> bool:
        return not self


class Utf8StringSlice(StringSlice):
    __slots__ = ("_content", "_left")
    _left: int
    _content: str

    def __init__(self, left: int, content: str):
        if left >> 2 >= len(content):
            left = 0
            content = ""
        self._left = left
        self._content = content

    def __iter__(self) -> Iterable[int]:
        left, content = self._left, self._content
        utf8 = "utf-8"
        idx, sub = left >> 2, left & 3
        if sub:
            for byt in islice(encode(content[idx], utf8), sub, None):
                yield int(byt)
            idx += 1
        for buf in iterencode(_str_iter_at(content, idx), utf8):
            yield from map(int, buf)

    def __bool__(self) -> bool:
        return bool(self._content)

    def __len__(self) -> int:
        left, content = self._left, self._content
        return sum(_utf8_size(char) for char in _str_iter_at(content, left >> 2)) - (
            left & 3
        )

    def _left_plus(self, count: int) -> int:
        left, content = self._left, self._content
        len_content = len(content)
        idx, sub = left >> 2, left & 3

        while count > 0 and idx < len_content:
            rem = _utf8_size(content[idx]) - sub
            if rem > count:
                sub += count
                count = 0
            else:
                count -= rem
                sub = 0
                idx += 1

        return -1 if count else idx << 2 | sub

    def advance(self, count: int) -> "Utf8StringSlice":
        if count <= 0:
            result = self
        else:
            left, content = self._left_plus(count), self._content
            if left < 0:
                left, content = 0, ""
            result = Utf8StringSlice(left, content)
        return result

    def to_json(self):
        left, content = self._left, self._content
        right = len(content) << 2
        return {"left": left, "right": right, "content": content}

    def __str__(self) -> str:
        left, content = self._left, self._content
        idx, sub = left >> 2, left & 3
        if sub:
            pre = "\ufffd"
            idx += 1
        else:
            pre = ""
        return pre + content[idx:]


class Utf16StringSlice(StringSlice):
    __slots__ = ("_content", "_left")
    _left: int
    _content: str

    def __init__(self, left: int, content: str):
        if left >> 1 >= len(content):
            left = 0
            content = ""
        self._left = left
        self._content = content

    def __iter__(self) -> Iterable[int]:
        left, content = self._left, self._content
        utf16 = "utf-16-be"
        idx, sub = left >> 1, left & 1
        if sub:
            for hi, lo in islice(_iter_pairs(encode(content[idx], utf16)), sub, None):
                yield hi << 8 | lo
            idx += 1
        for buf in iterencode(_str_iter_at(content, idx), utf16):
            for hi, lo in _iter_pairs(buf):
                yield hi << 8 | lo

    def __bool__(self) -> bool:
        return bool(self._content)

    def __len__(self) -> int:
        left, content = self._left, self._content
        return sum(_utf16_size(char) for char in _str_iter_at(content, left >> 1)) - (
            left & 1
        )

    def _left_plus(self, count: int) -> int:
        left, content = self._left, self._content
        len_content = len(content)
        idx, sub = left >> 1, left & 1

        while count > 0 and idx < len_content:
            rem = _utf16_size(content[idx]) - sub
            if rem > count:
                sub += count
                count = 0
            else:
                count -= rem
                sub = 0
                idx += 1

        return -1 if count else idx << 1 | sub

    def advance(self, count: int) -> "Utf16StringSlice":
        if count <= 0:
            result = self
        else:
            left, content = self._left_plus(count), self._content
            if left < 0:
                left, content = 0, ""
            result = Utf16StringSlice(left, content)
        return result

    def to_json(self):
        left, content = self._left, self._content
        right = len(content) << 1
        return {"left": left, "right": right, "content": content}

    def __str__(self) -> str:
        left, content = self._left, self._content
        idx, sub = left >> 1, left & 1
        if sub:
            pre = "\ufffd"
            idx += 1
        else:
            pre = ""
        return pre + content[idx:]


class CodePointsStringSlice(StringSlice):
    __slots__ = ("_content", "_left")
    _left: int
    _content: str

    def __init__(self, left: int, content: str):
        if left >= len(content):
            content = ""
            left = 0
        self._left = left
        self._content = content

    def __iter__(self) -> Iterable[int]:
        left, content = self._left, self._content
        return (ord(c) for c in _str_iter_at(content, left))

    def __len__(self) -> int:
        return len(self._content) - self._left

    def __bool__(self) -> bool:
        return bool(self._content)

    def _left_plus(self, count: int) -> int:
        left = self._left + count
        return -1 if left > len(self._content) else left

    def advance(self, count: int) -> "CodePointsStringSlice":
        if count <= 0:
            result = self
        else:
            left, content = self._left_plus(count), self._content
            if left < 0:
                left, content = 0, ""
            result = CodePointsStringSlice(left, content)
        return result

    def __str__(self) -> str:
        return self._content[self._left :]

    def to_json(self):
        left, content = self._left, self._content
        return {"left": left, "right": len(content), "content": content}


class DenseBitVector(object):
    "An expandable bitvector backed by a bytearray."
    __slots__ = ("_bytearray",)
    _not0 = re.compile(rb"[^\0]")  # Any byte other than 0
    _tail0 = re.compile(rb"\0*$")  # Trailing 0 bytes

    def __init__(self, capacity: int):
        "Capacity is in bits."
        self._bytearray = bytearray((capacity + 7) >> 3)

    def __bool__(self) -> bool:
        "Test if any bit is set."
        return bool(self._not0.search(self._bytearray))

    def __bytes__(self) -> bytes:
        "Convert the bit vector into a read-only bytes value."
        return self._tail0.sub(b"", self._bytearray)

    def get(self, idx: int) -> bool:
        "Read a bit from the vector as a boolean; or false if out of bounds."
        if idx < 0:
            return False
        ba = self._bytearray
        byte_index = idx >> 3
        if byte_index >= len(ba):
            return False
        return bool(ba[byte_index] & (1 << (idx & 7)))

    def set(self, idx: int, bit: bool):
        "set a bit in the bit vector, expanding the vector as needed."
        if idx < 0:
            raise NoResultException()
        ba = self._bytearray
        byte_size = len(ba)
        byte_index = idx >> 3
        if byte_index >= byte_size:
            ba.extend(b"\0" * (byte_index + 1 - byte_size))
        mask = 1 << (idx & 7)
        if bit:
            ba[byte_index] |= mask
        else:
            ba[byte_index] &= ~mask


## Constructors


def string_utf8(string: str) -> Utf8StringSlice:
    "Implements connected method String::utf8"
    return Utf8StringSlice(0, string)


def string_utf16(string: str) -> Utf16StringSlice:
    "Implements connected method String::utf8"
    return Utf16StringSlice(0, string)


def string_code_points(string: str) -> CodePointsStringSlice:
    "Implements connected method String::utf8"
    return CodePointsStringSlice(0, string)


## Connected methods


def int_to_float64(value: int) -> float:
    "Implements connected method Int::toFloat64"
    try:
        return float(value)
    except OverflowError:
        raise NoResultException()

def int_to_float64_unsafe(value: int) -> float:
    "Implements connected method Int::toFloat64Unsafe"
    try:
        return float(value)
    except OverflowError:
        return -inf if value < 0 else inf


def int_to_string(num, radix: int=10) -> str:
    "Implements connected method Int::toString"
    if not 2 <= radix < 36:
        raise NoResultException()
    elif radix == 10:
        return str(num)
    elif radix == 16:
        return "%x" % (num,)
    elif radix == 8:
        return "%o" % (num,)
    else:

        def seq(rem):
            if rem == 0:
                yield "0"

            while rem:
                yield "0123456789abcdefghijklmnopqrstuvwxyz"[rem % radix]
                rem //= radix

            if num < 0:
                yield "-"

        return "".join(reversed(list(seq(abs(num)))))


def float64_to_int(value: float) -> int:
    "Implements connected method Float64::toInt"
    # Potentially much more expensive in Python than other backends.
    # TODO Should we tighten the limits for float to int?
    try:
        return int(value)
    except (OverflowError, ValueError):
        raise NoResultException()


def float64_to_int_unsafe(value: float) -> int:
    "Implements connected method Float64::toIntUnsafe"
    # Potentially much more expensive in Python than other backends.
    # TODO Should we tighten the limits for float to int?
    try:
        return int(value)
    except OverflowError:
        # There's not really a good option for infinity or whatnot, but using
        # the extreme float values, which work in my experience, are at least
        # no smaller than for other float values.
        return int(copysign(float_info.max, value))
    except ValueError:
        # Happens for NaN, but for any other such case, also use what we want.
        return 0


def float64_to_string(value: float) -> str:
    "Implements connected method Float64::toString"
    if value == inf:
        return "∞"
    elif value == -inf:
        return "-∞"
    elif isnan(value):
        return "NaN"
    else:
        return str(value)


def boolean_to_string(value: bool) -> str:
    return "true" if value else "false"


def string_split(string: str, separator: str) -> Tuple[str, ...]:
    "split a string, returning a list of elements."
    return tuple(string.split(separator)) if separator  else tuple(string)


def list_filter(lst: List[T], predicate: Callable[[T], bool]) -> Tuple[T, ...]:
    "Filter a list of elements, aborting on no-result."
    return tuple(i for i in lst if predicate(i))


def list_get(lst: Sequence[T], index: int) -> T:
    "Get an item from a list by index."
    if index < 0:  # Prohibit python index semantics
        raise NoResultException()
    try:
        return lst[index]
    except IndexError:
        raise NoResultException()


def list_get_or(lst: Sequence[T], index: int, default: T) -> T:
    "Get an item from a list by index with a default."
    if 0 <= index < len(lst):
        return lst[index]
    else:
        return default


def list_builder_add(lst: List[T], elem: T, at : Union[int, EllipsisType]=...) -> Any:
    "Append a single element to a list."
    lst_len: int = len(lst)
    if at is ... or at == lst_len:
        lst.append(elem)
    else:
        if at < 0 or at > lst_len:
            raise NoResultException()
        lst.insert(at, elem)


def list_builder_add_all(lst: List[T], elems: Sequence[T], at : Union[int, EllipsisType]=...) -> Any:
    "Append multiple elements to a list."
    lst_len: int = len(lst)
    if at is ... or at == lst_len:
        lst.extend(elems)
    else:
        if at < 0 or at > lst_len:
            raise NoResultException()
        lst[at:at] = elems


def list_join(lst: Sequence[T], separator: str, stringifier: Callable[[T], str]) -> str:
    "Join a list of items after converting them to strings."
    return separator.join(stringifier(i) for i in lst)


def list_map(lst: Sequence[T], func: Callable[[T], T]) -> Tuple[T, ...]:
    "Map a list of elements."
    return tuple(func(i) for i in lst)


def list_builder_remove_last(lst: List[T]) -> T:
    "Pops and returns the last item, if any, else raises."
    try:
        return lst.pop()
    except IndexError:
        raise NoResultException

def list_builder_reverse(lst: List[T]):
    "Reverses a list in place."
    lst.reverse()


def list_builder_splice(lst: List[T], index: Union[int, EllipsisType] = ..., remove_count: Union[int, EllipsisType] = ..., new_values: Union[Sequence[T], EllipsisType] = ...) -> Tuple[T, ...]:
    "Remove some items and insert others."
    # Work through defaults and bounds.
    if index is ... or index < 0:
        index = 0
    if remove_count is ...:
        remove_count = len(lst)
    elif remove_count < 0:
        remove_count = 0
    # Now take care of business.
    end_index = index + remove_count
    result = tuple(lst[index:end_index])
    lst[index:end_index] = () if new_values is ... else new_values
    return result


def list_builder_set(lst: List[T], idx: int, val: T):
    "set a list element, returning no result if out of bounds, or void on success."
    if idx < 0:
        raise NoResultException()
    try:
        lst[idx] = val
    except IndexError:
        raise NoResultException()
    return None


def list_map_dropping(lst: List[T], func: Callable[[T], Union[T, NoReturn]]) -> Tuple[T, ...]:
    "Map a list of elements, omitting any for which func produces no result."
    results = []
    for e in lst:
        try:
            results.append(func(e))
        except NoResultException:
            pass
    return tuple(results)


def list_slice(lst: Sequence[T], start_inclusive: int, end_exclusive: int) -> Tuple[T, ...]:
    "Almost exactly a Python slice, but indices are constrained to be >= 0."
    # TODO(tjp): Cheaper to always say tuple here, or separate out for ListBuilder use?
    return tuple(lst[max(start_inclusive, 0) : max(end_exclusive, 0)])


def deque_remove_first(deq):
    "Defer to deque.popleft, except returning no result when the deque is empty."
    if not deq:
        raise NoResultException()
    return deq.popleft()


def dense_bit_vector_set(instance: DenseBitVector, idx: int, bit: bool) -> None:
    "sets a bit within a dense bit vector."
    instance.set(idx, bit)


def map_constructor(entries):
    return types.MappingProxyType(dict(entries))


def map_builder_remove(builder, key):
    try:
        return builder.pop(key)
    except KeyError:
        raise NoResultException()

def map_builder_set(builder, key, value):
    builder[key] = value


def map_builder_to_map(builder):
    return map_constructor(builder)


# Generic named tuple is tricky, by the way, so just use simple mode. Example
# trick if we ever want to go there: https://stackoverflow.com/a/58621986
# For vscode, at least, I had to adjust that example to repeat the fields in
# the generic subclass, and I had to explicitly type the variable.
Pair = namedtuple("Pair", ["key", "value"])


_missing = object()


def mapped_get(map, key):
    result = map.get(key, _missing)
    if result is _missing:
        raise NoResultException()
    return result


def mapped_to_list(map):
    return tuple(Pair(*item) for item in map.items())


## Utility functions


def _count_iter(iterable: Iterable[int]) -> int:
    "Use a constrained deque to consume an enumeration of the iterable, giving us the count."
    last = deque(enumerate(iterable, 1), 1)
    return last.pop()[0] if last else 0


def _str_iter_at(string: Iterable[str], offset: int) -> Iterable[str]:
    "Return a string iterator skipped forward by 'offset' characters."
    iterator: Any = iter(string)
    if offset:
        iterator.__setstate__(offset)
    return iterator


def _utf8_size(char: str) -> int:
    num = ord(char)
    if 0 <= num < 0o200:
        return 1
    elif 0o200 <= num < 0o4000:
        return 2
    elif 0o4000 <= num < 0o100000:
        return 3
    else:
        return 4


def _utf16_size(char: str) -> int:
    return 1 + (ord(char) >= 0x10000)


def _iter_pairs(iterable: Sequence[T]):
    "Convert a stream like [1, 2, 3, 4] to [(1, 2), (3, 4)]."
    iterator = iter(iterable)
    # The semantics of zip are that it draws from iterators in a round-robin fashion. Passing the same iterator
    # twice thus converts a list into pairs.
    # We"re not using zip_longest, so we must ensure the list has an even length.
    return zip(iterator, iterator)

