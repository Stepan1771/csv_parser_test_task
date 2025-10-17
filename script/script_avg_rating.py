import csv

import argparse

from tabulate import tabulate

from script.db_helper import db_helper


def average_rating():
    delimiter = ","
    encoding = "utf-8"

    parser = argparse.ArgumentParser(
        description="Average rating",
    )
    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
    )
    parser.add_argument(
        '--report',
        choices=['average-rating'],
        required=True,
    )
    args = parser.parse_args()

    if not args.files:
        return False

    try:
        db_helper.create_table()
        for csv_file in args.files:
            with open(
                    csv_file,
                    encoding=encoding,
            ) as file:
                csv_reader = csv.reader(
                    file,
                    delimiter=delimiter,
                )
                headers = tuple(next(csv_reader))

                for row in csv_reader:
                    db_helper.insert_data(
                        headers=headers,
                        row=row,
                    )

        data = db_helper.average_rating()

        if not data:
            return False

        headers = ["brand", "rating"]
        result = tabulate(
            data,
            headers=headers,
            tablefmt='grid',
            floatfmt=".2f",
            )

        print(result)

        return result

    except Exception as e:
        print(f"Ошибка: {e}")
        return False

    finally:
       db_helper.drop_db()