import os
import glob
import openpyxl
import pytesseract
from pandas import DataFrame
from dateutil.parser import parse

def main():
    images = collect_images('*.jpg')
    images.append(collect_images('*.png'))
    images.append(collect_images('*.jpeg'))
    images = [item for sublist in images for item in sublist]
    extract_text_from_images(images)

def collect_images(pattern):
    files = []
    start_dir = os.getcwd()
    for dir,_,_ in os.walk(start_dir):
        files.extend(glob.glob(os.path.join(dir,pattern)))
    return files

def fix_utf8(str):
  return str.encode('utf-8','ignore').decode("utf-8")

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def first(iterable, condition = lambda x: True):
    """
    Returns the first item in the `iterable` that
    satisfies the `condition`.

    If the condition is not given, returns the first item of
    the iterable.

    Raises `StopIteration` if no item satysfing the condition is found.

    >>> first( (1,2,3), condition=lambda x: x % 2 == 0)
    2
    >>> first(range(3, 100))
    3
    >>> first( () )
    Traceback (most recent call last):
    ...
    StopIteration
    """

    return next(x for x in iterable if condition(x))


def extract_text_from_images(images):
    # print("Images to extract from:", images)
    date_column = []
    text_column = []
    for image in images:
        try:
            full_text = pytesseract.image_to_string(image).split('\n')
            full_text = list(filter(None, full_text))
            full_text = list(map(fix_utf8, full_text))
            if "< S" in full_text: full_text.remove("< S")
            if "< ¢-)" in full_text: full_text.remove("< ¢-)")
            if "< Notes ¢:) Done" in full_text: full_text.remove("< Notes ¢:) Done")
            date_index = full_text.index(first(full_text, is_date))
            # print(full_text)
            date = full_text[date_index]
            if date == '' or date == ' ':
                date_index += 1
                date = full_text[date_index]
            body = '\n'.join(full_text[date_index+1:-3 or None])
            date_column.append(date)
            text_column.append(body)
            # print("Date:", date)
            # print(body)
            # print("------------")
        except Exception:
            pass
    write_to_xl(date_column, text_column)


def write_to_xl(date_column, text_column):
    df = DataFrame({'Date': date_column, 'Movie Idea': text_column})
    df.to_excel('freemovieidea-archive.xlsx', sheet_name='sheet1', index=False)
    # print(df)

main()