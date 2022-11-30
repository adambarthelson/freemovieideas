import os
import gc
import glob
import openpyxl
import pytesseract
from pandas import DataFrame
import pandas as pd
from dateutil.parser import parse

def main():
    images = []
    images += collect_images('./images_to_extract/*.jpg')
    images += collect_images('./images_to_extract/*.png')
    images += collect_images('./images_to_extract/*.jpeg')
    

    print("Images to OCR:", len(images))
    print("Running...")

    df = DataFrame({'Date': [], 'Movie Idea': []})
    df.to_excel('freemovieidea-archive.xlsx', sheet_name='sheet1', index=False)
    del df

    for image in images:
        try:
            extract_text_from_image(image)
        except Exception:
            pass

    print("Done!")

def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])

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

    return next((x for x in iterable if condition(x)), False)


def extract_text_from_image(image):
    full_text = pytesseract.image_to_string(image, lang='eng', config='--psm 6').split('\n')
    full_text = list(filter(None, full_text))
    full_text = list(map(fix_utf8, full_text))
    if "< S" in full_text: full_text.remove("< S")
    if "< ¢-)" in full_text: full_text.remove("< ¢-)")
    if "< Notes ¢:) Done" in full_text: full_text.remove("< Notes ¢:) Done")
    first_date = first(full_text, is_date) # ;)
    if first_date != False:
        date_index = full_text.index(first_date)
        # print(full_text)
        date = full_text[date_index]
        if date == '' or date == ' ':
            date_index += 1
            date = full_text[date_index]
        body = '\n'.join(full_text[date_index+1:-3 or None])
        if body == "":
            body = '\n'.join(full_text[date_index+1:0 or None])
        print("Date:", date)
        date = date.encode('utf-8','ignore').decode("utf-8")
        write_to_xl(date, body)
        del full_text
        del body
        del date_index
        del date
        gc.collect()
        # print("Date:", date)
        # print(body)
        # print("------------")



def write_to_xl(date_column, text_column):
    df=pd.read_excel("freemovieidea-archive.xlsx", engine='openpyxl')

    #df.append({'Date': date_column, 'Movie Idea': text_column}, ignore_index = True)
    df2 = DataFrame({'Date': [date_column], 'Movie Idea': [text_column]})

    df3 = pd.concat([df, df2], ignore_index = True)
    df3.reset_index()

    df3.to_excel('freemovieidea-archive.xlsx', sheet_name='sheet1', index=False)

    del df
    del df2
    del df3
    gc.collect()


main()