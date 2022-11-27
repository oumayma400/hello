import configparser

def get_variables(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    variables = {}
    for section in config.sections():
        for key, value in config.items(section):
            var = "%s" % (key)
            if ',' in value:variables[var] = value.split(',')
            else:variables[var] = value
    return variables