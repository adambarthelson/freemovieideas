import os
import glob
import openpyxl
import pytesseract
from pandas import DataFrame

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


def extract_text_from_images(images):
    # print("Images to extract from:", images)
    date_column = []
    text_column = []
    for image in images:
        date_index = 2
        full_text = pytesseract.image_to_string(image).split('\n')
        full_text = list(filter(None, full_text))
        if "< S" in full_text: full_text.remove("< S")
        # print(full_text)
        date = full_text[date_index]
        if date == '':
            date_index += 1
            date = full_text[date_index]
        body = '\n'.join(full_text[date_index+1:-3 or None])
        date_column.append(date)
        text_column.append(body)
        # print("Date:", date)
        # print(body)
        # print("------------")
    write_to_xl(date_column, text_column)


def write_to_xl(date_column, text_column):
    df = DataFrame({'Date': date_column, 'Movie Idea': text_column})
    df.to_excel('freemovieidea-archive.xlsx', sheet_name='sheet1', index=False)
    # print(df)

main()