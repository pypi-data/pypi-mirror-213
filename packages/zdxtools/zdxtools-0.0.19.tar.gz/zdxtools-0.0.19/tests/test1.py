from pypi_update.src.zdxtools.dx_tools import sign_tools
def test():
    data = {
        'a':1,
        '222':'2',
        'getsig':'213123',
    }

    print(sign_tools.get_sign(data,neadlist=['a','222'],deletelist=['getsig']))
if __name__ == '__main__':
    test()