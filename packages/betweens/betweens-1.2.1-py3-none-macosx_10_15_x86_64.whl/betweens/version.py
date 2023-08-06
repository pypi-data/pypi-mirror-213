ver = '0.2.0'
def version():
    print(ver)

def check_ver():
    import pip
    pip.main(['install','betweens','-U'])

