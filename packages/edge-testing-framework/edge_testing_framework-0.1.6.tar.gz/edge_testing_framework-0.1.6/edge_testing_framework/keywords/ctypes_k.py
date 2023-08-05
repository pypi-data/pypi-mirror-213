# coding:utf-8
import json

# @Auther:liyubin
# @Time: 2023/5/11 10:48

from edge_testing_framework.globals import g
from edge_testing_framework.log import logger
from edge_testing_framework.page_variables import e
from edge_testing_framework.utility import json2dict
from ctypes import *
import time
from edge_testing_framework.lib.injson_ok import check


"""
ctypes keywords
"""


def load_c(step):
    """加载c++文件 dll/so"""
    main('load_c', step)


def call_c(step):
    """调用c++中函数"""
    main('call_c', step)


def main(kw, step):
    """主入口关键字实际执行函数"""
    data = step['data']
    expected_ = step['expected']

    # 测试数据解析时，会默认添加一个 text 键，需要删除
    if 'text' in data and not data['text']:
        data.pop('text')

    # 全局变量替换, 在json2dict前还未执行函数
    page_var_key_str = step['page_variables']
    page_var_key_list = []
    if len(page_var_key_str) > 0:
        page_var_key_list = page_var_key_str.split(',,')  # 多个页面变量默认约定格式 var1,,var2

    for page_var_key in page_var_key_list:
        page_name = step.get('page', 'no page')
        if '{}-'.format(page_name) not in page_var_key:
            page_var_value = e.get('{}-{}'.format(page_name, page_var_key), ())[1]
        else:
            page_var_value = e.get('{}'.format(page_var_key), ())[1]
        if page_var_value:
            page_var_key = page_var_key.replace('{}-'.format(step.get('page', 'no page')), '')

            # 测试数据变量替换
            data_json_ = data.get('json', '{}')
            if data_json_ != '{}':
                data['json'] = data_json_.replace('<{}>'.format(page_var_key), page_var_value)

            # 预期值变量替换
            except_json_ = expected_.get('json', '{}')
            if except_json_ != '{}':
                expected_['json'] = except_json_.replace('<{}>'.format(page_var_key), page_var_value)

    _data = {}

    if kw in ('load_c', 'call_c'):
        try:
            _data['json'] = json2dict(data.get('json', '{}'))
        except Exception as ex:
            raise '请检查 测试数据、预期结果、输出数据的 值， error{}'.format(str(ex))

    for k in data:
        for s in ('{', '[', 'False', 'True'):
            if s in data[k]:
                try:
                    data[k] = eval(data[k])
                except:
                    logger.warning('Try eval data failure: %s' % data[k])
                break

    expected_['json'] = json2dict(expected_.get('json', '{}'))
    timeout = float(expected_.get('timeout', 0))
    expected_['time'] = float(expected_.get('time', 0))
    expected_['text'] = expected_.get('text', None)

    time.sleep(timeout)
    # 加载dll/so
    if kw == 'load_c':
        from edge_testing_framework.servers.ctypes_client import CtypesInit
        CtypesInit(_data['json']).setup_ctypes_client()

    # 调用dll/so中函数
    if kw == 'call_c':
        response, kwargs_ = execute_call_c(_data['json'])
        get_response_expect_var(expected_, step, response, kwargs_)


def execute_call_c(data):
    """
    执行 调用c++方法
    :param data:
    :return: 函数运行结果, 运行结果取值变量
    """
    c_func_name = data.get('c_func_name', '')
    assert '当前C++文件%s \n 请输入C++函数名：c_func_name 的值' if not c_func_name else True

    kwargs = {}  # 返回值取值时使用
    args = []  # 运行函数传值时使用
    for k, v in data.items():
        if k != 'c_func_name':
            # 测试数据中变量替换，如果提取的变量是对象、指针等时，直接在 g.var 中获取原始数据，而不是 '<var>' 方式写在用例中的话 对象就变str了
            if isinstance(v, str) and v.startswith('$'):
                v = g.var.get(v.replace('$', ''), None)
            if 'byref' in k:  # byref.：传给函数 前 加指针， .byref：传给函数 时 加指针
                args.append(byref(v))
            else:
                args.append(v)
            kr = k.replace('.byref', '').replace('byref.', '')
            kwargs.update(** {kr: byref(v)} if 'byref.' in k else {kr: v})  # byref.前置时 对象取值也加指针

    # 先组装 eval(func) = g.ctypes_client.动态函数名(),  而不是 g.ctypes_client.c_func_name()
    func = 'g.ctypes_client.{}'.format(c_func_name)
    logger.info('execute c++ func: {}, args: {}, kwargs: {}'.format(func, str(args), str(kwargs)))
    return pyramid_run(func, args), kwargs


def pyramid_run(func, kwargs):
    """
    待执行函数与原始数据组装运行
    :param func: 待运行函数
    :param kwargs: 原始参数
    :return: 原始返回值
    """
    length = len(kwargs)
    if length == 0:
        return eval(func)()
    elif length == 1:
        return eval(func)(kwargs[0])
    elif length == 2:
        return eval(func)(kwargs[0], kwargs[1])
    elif length == 3:
        return eval(func)(kwargs[0], kwargs[1], kwargs[2])
    elif length == 4:
        return eval(func)(kwargs[0], kwargs[1], kwargs[2], kwargs[3])
    elif length == 5:
        return eval(func)(kwargs[0], kwargs[1], kwargs[2], kwargs[3], kwargs[4])
    elif length == 6:
        return eval(func)(kwargs[0], kwargs[1], kwargs[2], kwargs[3], kwargs[4], kwargs[5])
    elif length == 7:
        return eval(func)(kwargs[0], kwargs[1], kwargs[2], kwargs[3], kwargs[4], kwargs[5], kwargs[6])
    elif length == 8:
        return eval(func)(kwargs[0], kwargs[1], kwargs[2], kwargs[3], kwargs[4], kwargs[5], kwargs[6], kwargs[7])
    elif length == 9:
        return eval(func)(kwargs[0], kwargs[1], kwargs[2], kwargs[3], kwargs[4], kwargs[5], kwargs[6], kwargs[7], kwargs[8])
    elif length == 10:
        return eval(func)(kwargs[0], kwargs[1], kwargs[2], kwargs[3], kwargs[4], kwargs[5], kwargs[6], kwargs[7], kwargs[8], kwargs[9])


def get_response_expect_var(expected_, step_, response_, kwargs_):
    """
    预期值处理
    变量处理
    需注意函数返回的数据类型和结构是不定的，在这里只提供通用断言相等、包含、大小、是否返回值 和 全局变量设置
    """

    response = json2dict(response_)  # 函数返回
    kwargs_ = json2dict(kwargs_)  # 对象取值
    full_kwargs_ = kwargs_
    real_kwargs_ = {}
    var = {}  # 存储所有输出变量

    logger.info(f'Expected: {step_["expected"]}')

    if expected_['text']:
        logger.info(f'Response: {response}')
        if expected_['text'].startswith('*'):
            if expected_['text'][1:] not in response:
                raise Exception(f'text | EXPECTED:{repr(expected_["text"])}, REAL:{repr(response)}')
        elif expected_['text'].startswith('!'):
            if eval(expected_['text'][1:]) == response:  # 校验不相等，相等抛异常
                raise Exception(f'text | EXPECTED:{repr(expected_["text"])}, REAL:{repr(response)}')
        else:
            if eval(expected_['text']) != response:  # 函数执行默认返回str、int、bytes，或其他类型通过自定义函数进一步验证
                raise Exception(f'text | EXPECTED:{repr(expected_["text"])}, REAL:{repr(response)}')

    if expected_['json']:
        real_kwargs_, real_expected_, full_kwargs_ = reset_except_response(expected_, response_, kwargs_)  # 重组预期值和实际值
        logger.info(f'Response: {real_kwargs_}')

        # 校验
        result = check(real_expected_, real_kwargs_)
        logger.info('json check result: %s' % result)
        if result['code'] != 0:
            raise Exception(f'json | EXPECTED:{repr(real_expected_)}\nREAL:{repr(real_kwargs_)}\nRESULT: {result}')
        elif result['var']:
            var = dict(var, **result['var'])
            g.var = dict(g.var, **result['var'])
            logger.info('Json var: %s' % (repr(result['var'])))

    output = step_['output']
    if output:
        logger.info('output: %s' % repr(output))

    for k, v in output.items():
        if k == 'text':
            v = v.replace('<', '').replace('>', '')
            g.var[v] = response
            logger.info('%s var: %s' % (v, repr(g.var[v])))
        if k == 'json':
            sub = json2dict(output.get('json', '{}'))
            result = check(sub, full_kwargs_)  # 对比后变量'<var>' 值变为key，value为full_kwargs_中key对应的value
            var = dict(var, **result['var'])  # 提取到的变量字典
            g.var = dict(g.var, **result['var'])  # 设置变量字典到全局变量字典中
            logger.info('Json var: %s' % (repr(result['var'])))

    if var:
        step_['_output'] += '\n||output=' + str(var)


def reset_except_response(expected_, response_, kwargs_, key_name='json'):
    """
    通过预期值结构提取函数运行后对象中的值，组成相同的结构断言
    :return:
    """
    try:
        real_kwargs_ = {}  # 对象按断言所需字段取值后的实际结果
        real_expected_ = {}

        # 按预期expected-> json={k.v: exc_value}中取值方式对kwargs_对象取值, 可能取多次、或设置全局变量，所以组成新的数据结构
        for e_k_, e_v in expected_[key_name].items():
            if type(e_v) in (str, int, float, bool):  # value支持的类型
                e_k_k_ = e_k_.split('.')[0]  # 用 e_k_ 作为key 因传递一个参会提取多个值，相同时会被覆盖
                # e_k_v = e_k_.split('.')[1] # e_k_v可能是一层也可能是多层，如：e_k_k_.e_k_v_1.e_k_v_2
                e_k_v = e_k_[len(e_k_k_) + 1:]

                if '[' in e_k_k_ and ']' in e_k_k_:  # 对象包含多个数据按index取值
                    e_k_k = e_k_k_.split('[')[0]
                    e_k_k_index = '[{}'.format(e_k_k_.split('[')[1])
                    if e_k_v:
                        e_k_v_v = eval('kwargs_.get(e_k_k){}.{}'.format(e_k_k_index, e_k_v))
                    else:
                        e_k_v_v = eval('kwargs_.get(e_k_k){}'.format(e_k_k_index))
                else:
                    e_k_k = e_k_k_
                    if e_k_v:
                        e_k_v_v = eval('kwargs_.get(e_k_k).{}'.format(e_k_v))
                    else:
                        e_k_v_v = eval('kwargs_.get(e_k_k)')
                if isinstance(e_k_v_v, bytes):
                    e_k_v = e_k_v.replace('.', '_')  # 多层级a.b.c时: . 替换 _
                    try:
                        # 默认bytes转str， check不对bytes类型支持
                        real_kwargs_['{}_{}'.format(e_k_k, e_k_v)] = e_k_v_v.decode('utf-8')
                    except Exception as exx:
                        real_kwargs_['{}_{}'.format(e_k_k, e_k_v)] = str(exx)  # 可能非完整bytes类型转str报错
                else:
                    e_k_v = e_k_v.replace('.', '_')  # 多层级a.b.c时: . 替换 _
                    real_kwargs_['{}_{}'.format(e_k_k, e_k_v)] = e_k_v_v

                real_expected_['{}_{}'.format(e_k_k, e_k_v)] = e_v

            # 批量断言
            elif isinstance(e_v, list):  # 批量对象取值断言，只支持一层list {list: [{}, {}]}
                real_kw_list = []
                real_ex_list = []
                for e_v_index, e_v_dict in enumerate(e_v):
                    real_expected_batch = {}
                    real_kwargs_batch = {}
                    for e_v_d_k, e_v_d_v in e_v_dict.items():
                        e_v_d_k_k_ = e_v_d_k.split('.')[0]
                        # e_v_d_k_v = e_v_d_k.split('.')[1] # e_k_v可能是一层也可能是多层，如：e_k_k_.e_k_v_1.e_k_v_2
                        e_v_d_k_v = e_v_d_k[len(e_v_d_k_k_) + 1:]

                        if '[' in e_v_d_k_k_ and ']' in e_v_d_k_k_:  # 对象包含多个数据按index取值
                            e_v_d_k_k = e_v_d_k_k_.split('[')[0]
                            e_k_k_index = '[{}'.format(e_v_d_k_k_.split('[')[1])
                            if e_v_d_k_v:
                                e_k_v_v = eval('kwargs_.get(e_v_d_k_k){}.{}'.format(e_k_k_index, e_v_d_k_v))
                            else:
                                e_k_v_v = eval('kwargs_.get(e_v_d_k_k){}'.format(e_k_k_index))
                        else:
                            e_v_d_k_k = e_v_d_k_k_
                            if e_v_d_k_v:
                                e_k_v_v = eval('kwargs_.get(e_v_d_k_k).{}'.format(e_v_d_k_v))
                            else:
                                e_k_v_v = eval('kwargs_.get(e_v_d_k_k)')

                        if isinstance(e_k_v_v, bytes):
                            e_v_d_k_v = e_v_d_k_v.replace('.', '_')  # 多层级a.b.c时: . 替换 _
                            try:
                                # 默认bytes转str， check不对bytes类型支持
                                real_kwargs_batch['{}_{}'.format(e_v_d_k_k, e_v_d_k_v)] = e_k_v_v.decode('utf-8')
                            except Exception as exx1:
                                # 可能非完整bytes类型转str报错
                                real_kwargs_batch['{}_{}'.format(e_v_d_k_k, e_v_d_k_v)] = str(exx1)
                        else:
                            e_v_d_k_v = e_v_d_k_v.replace('.', '_')  # 多层级a.b.c时: . 替换 _
                            real_kwargs_batch['{}_{}'.format(e_v_d_k_k, e_v_d_k_v)] = e_k_v_v

                        real_expected_batch['{}_{}'.format(e_v_d_k_k, e_v_d_k_v)] = e_v_d_v

                    real_kw_list.append(real_kwargs_batch)
                    real_ex_list.append(real_expected_batch)

                real_kwargs_[e_k_] = real_kw_list
                real_expected_[e_k_] = real_ex_list

        kwargs_.update(real_kwargs_)  # full_kwargs_ 包含了定义的所有参数，不参与断言，只提取变量：指针或结构体等
        return real_kwargs_, real_expected_, kwargs_
    except Exception as ex:
        raise '参数提取异常: {}'.format(str(ex))
