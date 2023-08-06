def dict_to_string(data: dict, multi=False) -> str:
    return "".join(f"{key}: {value}\n" for key, value in data.items()) if multi else \
        "".join(f"{key}: {value}" for key, value in data.items())
