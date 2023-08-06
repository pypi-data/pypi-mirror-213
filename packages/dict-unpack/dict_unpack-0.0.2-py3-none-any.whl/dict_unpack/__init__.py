from functools import reduce


def unpack(dictionary: dict, index: list, delimiter: str = None):
    """
    :param dictionary: A dictionary.
    :param index: A list specifying which keys you want to extract from the
    dictionary.The list items must follow the order of the path.
    :param delimiter: If it is empty, override the same-named key-value pairs in the parent. If it is not empty,
    use the provided string as the delimiter to connect with the parent key.
    :return: A list.
    """
    def flatten_dict(dictlist: list, listkey: str):
        result = []

        for dictitem in dictlist:
            listvalue = dictitem.get(listkey)
            dictitem.pop(listkey)

            if listvalue:
                if isinstance(listvalue[0], dict):
                    if delimiter:
                        result.extend([
                            {**dictitem, **{f"{listkey}{delimiter}{key}": value for key, value in item.items()}}
                            for item in listvalue
                        ])
                    else:
                        result.extend([
                            {**dictitem, **item}
                            for item in listvalue
                        ])
                else:
                    result.extend([
                        {**dictitem, **{listkey: item}}
                        for item in listvalue
                    ])
            else:
                raise Exception(f"A empty field '{listkey}' does not need to be unpacked.")

        return result

    if delimiter:
        index = list(
            reduce(lambda acc, item: acc + [f"{acc[-1]}{delimiter}{item}" if acc[-1] != '' else item], index, [""])[1:]
        )

    return reduce(lambda acc, x: flatten_dict(acc, x), index, [dictionary])