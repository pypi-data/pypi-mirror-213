def check_format_validity(path):
    from importing import read_machine_data_h5
    try:
        read_machine_data_h5(path)
    except Exception:
        return False
    return True
