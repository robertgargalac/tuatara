import numpy as np

month_decode_dict = {'english': {'01': 'Janauary',
                                 '02': 'February',
                                 '03': 'March',
                                 '04': 'April',
                                 '05': 'May',
                                 '06': 'June',
                                 '07': 'July',
                                 '08': 'August',
                                 '09': 'September',
                                 '10': 'October',
                                 '11': 'November',
                                 '12': 'December'},
                     'romanian': {'01': 'Ianuarie',
                                  '02': 'Februarie',
                                  '03': 'Martie',
                                  '04': 'Aprilie',
                                  '05': 'Mai',
                                  '06': 'Iunie',
                                  '07': 'Iulie',
                                  '08': 'August',
                                  '09': 'Septembrie',
                                  '10': 'Octombrie',
                                  '11': 'Noiembrie',
                                  '12': 'Decembrie'}
                     }


def get_item(data, key_name):
    items = []
    item_values = data[key_name]

    for item in np.unique(item_values):
        paragraph = {}
        mask = np.where(item_values == item)

        for key in data:
            parameter_values = np.array(data[key])
            paragraph[key] = parameter_values[mask]

        items.append(paragraph)
    return items
