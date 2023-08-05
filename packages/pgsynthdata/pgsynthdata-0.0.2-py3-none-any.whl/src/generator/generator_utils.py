from bisect import bisect_left
from typing import List, Optional, Sequence, Union
import string
import random
from typing import Any
import radar


def fulfill_histogram_properties(histogram, rows_to_gen, data_type=float):
    if histogram is None:
        return False
        
    max_nr_of_rows_from_bounds = data_type(
        histogram[len(histogram)-1])-data_type(histogram[0]) + 1

    if max_nr_of_rows_from_bounds < rows_to_gen:
        return True

    return False


def take_closest(myList: List[any], myNumber: int):
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before


def random_word(average_length: int, value: str = None) -> str:
    average_length = round(average_length-1)
    if value:
        if str(value).isdigit():
            word = gen_random_word(average_length, numeric=True)
        elif str(value).isupper():
            word = gen_random_word(average_length).upper()
        elif str(value) and str(value)[0].isupper():
            word = gen_random_word(average_length).capitalize()
        else:
            word = gen_random_word(average_length)
    else:
        word = gen_random_word(average_length)

    return word


def gen_random_word(length: int, numeric: bool = False) -> str:
    if length == 0:
        length += 1
    letters = string.ascii_lowercase
    numbers = string.digits

    if numeric:
        return ''.join(random.choice(numbers) for i in range(length))
    else:
        return ''.join(random.choice(letters) for i in range(length))


def gen_random_number(start: Any, end: Any, uniform: bool = False) -> Union[int, float]:

    start = int(start)
    end = int(end)

    if uniform:
        return random.uniform(start, end)
    else:
        return random.randint(start, end)


def random_number(numeric_precision: int = None, numeric_precision_radix: int = None, numeric_scale: int = None,
                  min_value: Any = None, max_value: Any = None) -> Union[int, float]:

    if numeric_precision:
        if numeric_scale and numeric_scale != 0:
            number = round(gen_random_number(
                min_value or 0,
                max_value or ((numeric_precision_radix **
                              (numeric_precision - numeric_scale - 1)) / 1.5),
                uniform=True),
                numeric_scale)
        else:
            number = gen_random_number(min_value or 0,
                                       max_value or ((numeric_precision_radix ** (numeric_precision - 1)) / 1.5))
    else:
        number = gen_random_number(0, 50000)

    return number


def random_date(start_date, end_date, time=False):
    if time:
        return radar.random_datetime(start=start_date, stop=end_date)
    else:
        return radar.random_date(start=start_date, stop=end_date)


def random_boolean(postgres: bool = True) -> Union[str, bool]:

    random_boolean = random.choice([True, False])
    if not postgres:
        return random_boolean
    else:
        if random_boolean:
            return 'true'
        else:
            return 'false'


def random_choices(list: List[Any], weights: Optional[Sequence[float]], k: int = 1) -> Any:
    if k == 1:
        return random.choices(list, weights=weights, k=k)[0]
    else:
        return random.choices(list, weights=weights, k=k)
