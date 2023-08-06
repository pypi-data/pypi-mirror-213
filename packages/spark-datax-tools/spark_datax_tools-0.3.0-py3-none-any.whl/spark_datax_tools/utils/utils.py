def extract_only_parenthesis(format):
    import re
    _number = re.findall(r'\(.*?\)', format)
    if len(_number) > 0:
        res = str(_number[0])
        res = res.replace("(", "").replace(")", "").strip()
    else:
        res = ""
    return res


def extract_only_column_text(columns):
    import re
    new_col = str(columns).lower()

    _text = re.findall(r'([a-zA-Z ]+)', new_col)
    if len(_text) > 0:
        res = _text[0]
    else:
        res = ""
    return res


def get_reformat_dtype(columns, format, convert_string=False):
    from pyspark.sql import types

    _format = str(extract_only_column_text(format)).upper()
    if str(_format).upper() == "DATE":
        _mask = "yyyy-MM-dd"
        _format = format
        _locale = "es_PE"
        _schema_type = "['date', 'null']"
        _type = types.StructField(columns, types.DateType())
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC(10)"
            _locale = ""
            _schema_type = "['string', 'null']"
            _type = types.StructField(columns, types.StringType())
    elif str(_format).upper() == "TIMESTAMP":
        _mask = "yyyy-MM-dd HH:mm:ss.SSSSSS"
        _format = format
        _locale = "es_PE"
        _schema_type = "['timestamp', 'null']"
        _type = types.StructField(columns, types.TimestampType())
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC(26)"
            _locale = ""
            _schema_type = "['string', 'null']"
            _type = types.StructField(columns, types.StringType())
    elif str(_format).upper() == "TIME":
        _mask = ""
        _format = "ALPHANUMERIC(8)"
        _locale = "PE"
        _schema_type = "['string', 'null']"
        _type = types.StructField(columns, types.StringType())
    elif str(_format).upper() in ("NUMERIC SHORT", "INTEGER"):
        _mask = ""
        _format = format
        _locale = ""
        _schema_type = "['null', 'int32']"
        _type = types.StructField(columns, types.IntegerType())
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC"
            _locale = ""
            _schema_type = "['string', 'null']"
            _type = types.StructField(columns, types.StringType())
    elif str(_format).upper().startswith("DECIMAL"):
        _parentheses = extract_only_parenthesis(format)
        _parentheses_split = str(_parentheses).split(",")
        if len(_parentheses_split) <= 1:
            _decimal_left = int(_parentheses_split[0])
            _decimal_right = 0
        else:
            _decimal_left = int(_parentheses_split[0])
            _decimal_right = int(_parentheses_split[1])
        _mask = ""
        _format = format
        _locale = ""
        _schema_type = f"['null', '{format}']"
        _type = types.StructField(columns, types.DecimalType(precision=_decimal_left, scale=_decimal_right))
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC"
            _locale = ""
            _schema_type = "['string', 'null']"
            _type = types.StructField(columns, types.StringType())
    else:
        _mask = ""
        _format = format
        _locale = ""
        _schema_type = "['string', 'null']"
        _type = types.StructField(columns, types.StringType())

    return _format, _mask, _locale, _type, _schema_type
