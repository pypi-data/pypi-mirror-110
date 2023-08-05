from logger_tt import setup_logging


setup_logging(analyze_raise_statement=True)

a = 'haha'
b = 'hihi'

raise RuntimeError(f'Too much laughing with a={a} and b={b}')
