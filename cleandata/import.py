def db_import(file):
    with open(file) as f:
        data = [line.strip().split(',') for line in f]
    return data