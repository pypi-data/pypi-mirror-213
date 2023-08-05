"""

测试注释1

"""


# 单行注释1

from dknovautils import *

# from dknovautils.commons import *
# from dknovautils.dkfiles import DkPyFiles
# from dknovautils.dkat import AT

# from dknovautils.dkipy import DkIpyUtils

# from commons import *
# from dkfiles import DkPyFiles
# from dkat import AT

print("test01 start")

'''

测试注释2

'''

"""

测试注释3

"""


def ftest01():
    '''

    测试注释4

    What is a Circular Import?

    '''

    assert 1 == 1, 'err5162'

    assert str(None) == 'None', str(None)

    assert AT.VERSION >= '0.0.39', f'err5484 {AT.VERSION}'

    AT.log_basicConfig()

    AT.logger().info('hello dkn logger')

    time.sleep(1.0)

    # assert False, 'ok'

    iprint(f'now:{AT.fepochSecs()}')

    print(AT.sdf_isocompact_format_datetime())

    iprint_warn('hello22')
    iprint_info('hello22')
    iprint_error('hello22')

    print('='*5)

    # r=DkIpyUtils.mfr('dir')
    # iprint(r)

    # assert False,'ok'

    # return

    # AT.log_basicConfig()

    iprint(AT.VERSION)

    fp = r'F:\DIKI\DIKIETC\ADEV\learn\LearnPython\PythonBook\dknovautils\test_a.py'

    jsonstr = Path(fp).read_text(encoding='utf8')

    # 这是单行注释2
    # fp2 = DkPyFiles.f_remove_comments_v1(jsonstr)
    # # print(fp2)

    # iprint_info(fp2)

    cstr = AT.sdf_logger_format_datetime()
    print(cstr)

    def f_abc(a): return a

    # TypeError: cannot set 'f_abc' attribute of immutable type 'str'
    # str.f_abc = f_abc
    # assert "abc".f_abc(123)==123,'err9592'

    # 可以直接修改函数
    DkPyFiles.f_remove_comments_v1 = lambda x: x

    assert DkPyFiles.f_remove_comments_v1(123) == 123, 'err2556'

    # now=datetime.now()
    # datetime.faa = 1

    # DkIpyUtils.magic_fc(123)

    assert DkIpyUtils.hello(1) == 1

    print(AT.VERSION)


if __name__ == '__main__':
    ftest01()


'''

https://packaging.python.org/en/latest/tutorials/packaging-projects/


'''