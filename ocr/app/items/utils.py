import numpy as np


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
