"""
> 此文件共包含四个模块：
Module 1: 基准数据和投资组合数据预处理函数(补全行业分类和个股收益率)
Module 2: 计算基准和投资组合的权重和收益矩阵
Module 3: Brinson多期模型核心算法，计算投资组合相对基准的择时收益、选股收益和交互收益
Module 4: 主函数模块

> 总体输入：DF数据格式
input 1：基准数据（日期+代码+日终权重）index不指定
input 2：日终个股收益率和行业分类
input 3：持仓数据  持仓日期、股票代码、日终权重或者市值等可以计算出权重的数据(需要补全收益率和行业分类)  index不指定
input 1和input3，结构一致用持仓（日期+代码+日终权重）作为输入。模块结合input2日终个股收益率，行业分类数据，
去帮用户计算基准和组合的行业权重及收益率
提供1、2、3、4、5五期基准和持仓数据以及2、3、4、5、6五期的行业和个股收益率，计算五期的Brinson归因

> 总体输出：
output 1：基于交易日的  归因结果  DF
"""

import os
import time

# 0. 导入pandas库
import pandas as pd

# 1. 基准数据和投资组合数据预处理函数(补全行业分类和个股收益率)
'''
· 函数功能：基准数据和投资组合数据预处理函数（日期+代码+权重）
· 输入变量：benchmark_data, positions_data, industry_data, stock_return_data
· 输出变量：基准数据和投资组合数据补全数据（日期+代码+当日日终权重+行业+下一个交易日日终个股收益率），格式为DataFrame的list
· 数据格式：
    1. industry_data：index为日期，columns为代码
    2. stock_return_data：index为日期，columns为代码
'''


def preProcess(benchmark_data, positions_data, industry_data, stock_return_data):
    # 1. 数据去重
    print('1. 数据去重')
    benchmark_data.drop_duplicates()
    positions_data.drop_duplicates()
    # 2. 处理 个股收益率 和 行业分类 数据缺失
    print('2. 处理 个股收益率 和 行业分类 数据缺失')
    # 速度太慢，放在输入之前
    # industry_data.fillna(0.0, inplace=True)
    # stock_return_data.fillna('其他', inplace=True)
    # 3. 补全 个股收益率 和 行业分类 列 并补全
    print('3. 补全 个股收益率 和 行业分类 列 并补全')
    benchmark_data['个股收益率'] = 0.0
    benchmark_data['行业'] = ''
    positions_data['个股收益率'] = 0.0
    positions_data['行业'] = ''
    # 先获取某列再获取某行 根据columns和index获取
    industry_dates = set(industry_data.index)
    stock_return_dates = set(stock_return_data.index)
    dates = list(industry_dates.intersection(stock_return_dates))
    dates.sort()
    n_dates = len(dates)
    for i in benchmark_data.index:
        cur_date = benchmark_data['日期'][i]  # 获取数据：日期
        real_index = dates.index(cur_date) + 1
        assert real_index < n_dates, cur_date + '下一日的个股收益率或行业数据缺失'
        real_date = dates[dates.index(cur_date) + 1]  # 填入数据：日期+1的数据
        cur_stock = benchmark_data['代码'][i]  # 获取数据：代码
        assert cur_stock in stock_return_data.columns and real_date in stock_return_data.index, cur_stock + '+' + real_date + 'stock数据缺失'
        assert cur_stock in industry_data.columns and real_date in industry_data.index, cur_stock + '+' + real_date + 'industry数据缺失'
        benchmark_data.loc[i, '个股收益率'] = stock_return_data[cur_stock][real_date]  # 根据日期和代码获取个股收益率
        benchmark_data.loc[i, '行业'] = industry_data[cur_stock][real_date]  # 根据日期和代码获取行业

    for i in positions_data.index:
        cur_date = positions_data['日期'][i]
        real_index = dates.index(cur_date) + 1
        assert real_index < n_dates, cur_date + '下一日的个股收益率或行业数据缺失'
        real_date = dates[dates.index(cur_date) + 1]  # 填入数据：日期+1的数据
        cur_stock = positions_data['代码'][i]
        assert cur_stock in stock_return_data.columns and real_date in stock_return_data.index, cur_stock + '+' + real_date + 'stock数据缺失'
        assert cur_stock in industry_data.columns and real_date in industry_data.index, cur_stock + '+' + real_date + 'industry数据缺失'
        positions_data.loc[i, '个股收益率'] = stock_return_data[cur_stock][real_date]
        positions_data.loc[i, '行业'] = industry_data[cur_stock][real_date]

    positions_data = positions_data[['日期', '代码', '行业', '个股收益率', '权重']]  # 选定需要使用的列
    benchmark_data = benchmark_data[['日期', '代码', '行业', '个股收益率', '权重']]  # 选定需要使用的列

    # positions_data['日期'] = positions_data['日期'].astype('datetime64')  # 转化日期格式
    return [benchmark_data, positions_data]


# 2. 计算基准和投资组合的权重和收益矩阵
'''
· 函数功能：计算基准和投资组合的权重和收益矩阵
· 输入变量：
    1） benchmark：补全的基准数据
    2)  positions: 补全的投资组合数据
· 输出变量：基准和投资组合的权重矩阵、收益矩阵，格式为DataFrame的list
· 注意：由于从基准中提取的行业名称可能不全，需要综合基准和投资组合的行业名称
'''


def w_r_calculation(benchmark, positions, sectors, td_dates):
    # Part 1: 初始化一些存储用的中间变量
    b_w = pd.DataFrame(0, columns=sectors, index=td_dates).astype('float')  # 存储基准权重
    b_r = pd.DataFrame(0, columns=sectors, index=td_dates).astype('float')  # 存储基准收益率
    p_w = pd.DataFrame(0, columns=sectors, index=td_dates).astype('float')  # 存储投资组合权重
    p_r = pd.DataFrame(0, columns=sectors, index=td_dates).astype('float')  # 存储投资组合收益率

    # Part 2: 计算过程
    for d in td_dates[:-1]:
        # t-1日权重为t日初始权重
        real_d = td_dates[td_dates.index(d) + 1]
        # 当前交易日筛选
        b_date_sub = benchmark[(benchmark['日期'] == d)]
        p_date_sub = positions[(positions['日期'] == d)]
        # 每个交易日的权重和应该为1
        b_date_total = b_date_sub['权重'].sum()
        p_date_total = p_date_sub['权重'].sum()
        assert round(b_date_total, 5) == 1, d + '权重和不为1，为：' + str(b_date_total)
        assert round(p_date_total, 5) == 1, d + '权重和不为1，为：' + str(p_date_total)
        for s in sectors:
            # 当前交易日某行业筛选
            b_date_s_sub = benchmark[(benchmark['行业'] == s) & (benchmark['日期'] == d)]
            p_date_s_sub = positions[(positions['行业'] == s) & (positions['日期'] == d)]
            # 当前交易日某行业总日终权重，即下个交易日初始权重
            b_date_s_total = b_date_s_sub['权重'].sum()
            p_date_s_total = p_date_s_sub['权重'].sum()
            b_w[s][real_d] = b_date_s_total
            p_w[s][real_d] = p_date_s_total
            if b_date_s_total == 0:
                b_r[s][real_d] = 0
            if p_date_s_total == 0:
                p_r[s][real_d] = 0
            # 计算下个交易日某行业收益率
            b_total_r = 0
            p_total_r = 0
            for i in b_date_s_sub.index:
                b_total_r += b_date_s_sub['权重'][i] / b_date_s_total * b_date_s_sub['个股收益率'][i]
            for i in p_date_s_sub.index:
                p_total_r += p_date_s_sub['权重'][i] / p_date_s_total * p_date_s_sub['个股收益率'][i]
            b_r[s][real_d] = b_total_r
            p_r[s][real_d] = p_total_r
    return [b_w, b_r, p_w, p_r]


# 3. Brinson多期模型核心算法，计算投资组合相对基准的择时收益、选股收益和交互收益
'''
· 函数功能：Brinson多期模型核心算法，计算投资组合相对基准的择时收益、选股收益和交互收益
· 输入变量：
    1）p_w_r: 组合加总收益
    2) b_w: 基准权重
    3）b_r: 基准收益
· 输出变量：总超额收益、择时收益、择股收益和交互作用收益率，格式为DataFrame，第一天为R0
'''


def Brinson_Multiple(b_w, b_r, p_w, p_r, sectors, td_dates):
    ticker = ['R_pp', 'R_pb', 'R_bp', 'R_bb']
    # 存储多期收益贡献
    cum_R = pd.DataFrame(0, columns=ticker, index=td_dates).astype('float')
    # 存储单期收益贡献(绝对)
    single_R = pd.DataFrame(0, columns=ticker, index=td_dates).astype('float')

    # 必须按照顺序迭代计算
    for d in td_dates[1:]:
        for s in sectors:
            single_R['R_bb'][d] += b_w[s][d] * b_r[s][d]
            single_R['R_bp'][d] += b_w[s][d] * p_r[s][d]
            single_R['R_pb'][d] += p_w[s][d] * b_r[s][d]
            single_R['R_pp'][d] += p_w[s][d] * p_r[s][d]

        for t in ticker:
            pre_R = cum_R[t][td_dates[td_dates.index(d) - 1]]
            cum_R[t][d] = pre_R + (pre_R + 1) * single_R[t][d]

    # 去除blank行
    # cum_R.drop(index=['blank', ], inplace=True)

    Total_Excess_Return = cum_R['R_pp'] - cum_R['R_bb']
    Time_Selection = cum_R['R_pb'] - cum_R['R_bb']
    Stock_Selection = cum_R['R_bp'] - cum_R['R_bb']
    Interactive_Effect = Total_Excess_Return - Time_Selection - Stock_Selection

    Outcome = pd.DataFrame(list(zip(Total_Excess_Return, Time_Selection, Stock_Selection, Interactive_Effect)),
                           columns=['Total_Excess_Return', 'Time_Selection', 'Stock_Selection', 'Interactive_Effect'],
                           index=td_dates)
    return Outcome


def brinson(benchmark_data, positions_data, industry_data, stock_return_data, output_path=None):
    # 1. 使用行业分类和个股收益率补全基准和投资组合数据
    print('1. 使用行业分类和日终个股收益率补全基准和投资组合数据')
    starttime = time.time()
    benchmark, positions = preProcess(benchmark_data, positions_data, industry_data, stock_return_data)
    print('preProcess_cost: ', time.time() - starttime)
    # 2. 提取行业名称 和 交易日信息
    # sectors: 提取行业名称  并集 |
    b_sectors = set(benchmark['行业'])
    p_sectors = set(positions['行业'])
    sectors = list(b_sectors.union(p_sectors))
    # trading_dates 从基准提取交易日信息  交集 &
    b_td_dates = set(benchmark['日期'])
    p_td_dates = set(positions['日期'])
    td_dates = list(b_td_dates.intersection(p_td_dates))
    td_dates.sort()
    td_dates += [str(len(td_dates)), ]
    # 3. 计算基准和投资组合的权重和收益矩阵
    print('3. 计算基准和投资组合的权重和收益矩阵')
    starttime = time.time()
    # 没有第一个交易日的权重和收益率
    b_w, b_r, p_w, p_r = w_r_calculation(benchmark, positions, sectors, td_dates)
    print('w_r_calculation_cost: ', time.time() - starttime)

    # 4. Brinson多期模型核心算法，计算投资组合相对基准的择时收益、选股收益和交互收益
    print('4. Brinson多期模型核心算法，计算投资组合相对基准的择时收益、选股收益和交互收益')
    starttime = time.time()
    outcome = Brinson_Multiple(b_w, b_r, p_w, p_r, sectors, td_dates)
    print('Brinson_Multiple_cost: ', time.time() - starttime)

    # 5. 打印结果，并将结果导出为excel形式
    # print(outcome.head())
    if output_path:
        outcome.to_excel(output_path, index=True, header=True)
    return outcome


def main():
    benchmark_path = '你的基准数据存放地址'  # 请修改
    positions_path = '你的持仓数据存放地址'  # 请修改
    industry_path = './data/INDUSTRY_UPDATE.H5'  # 请修改
    stock_return_path = './data/STOCK_RETURN_UPDATE.H5'  # 请修改

    # 1. 读取数据
    industry_data = pd.read_hdf(industry_path)
    stock_return_data = pd.read_hdf(stock_return_path)
    # industry_data = pd.DataFrame()
    # stock_return_data = pd.DataFrame()

    benchmark = [
        ['20210104', '000001.SZ', 0.1],
        ['20210104', '000002.SZ', 0.1],
        ['20210104', '000004.SZ', 0.1],
        ['20210104', '000005.SZ', 0.1],
        ['20210104', '000006.SZ', 0.1],
        ['20210104', '000007.SZ', 0.1],
        ['20210104', '000008.SZ', 0.1],
        ['20210104', '000009.SZ', 0.1],
        ['20210104', '000010.SZ', 0.1],
        ['20210104', '000011.SZ', 0.1],

        ['20210105', '000002.SZ', 0.1],
        ['20210105', '000004.SZ', 0.1],
        ['20210105', '000005.SZ', 0.1],
        ['20210105', '000006.SZ', 0.1],
        ['20210105', '000007.SZ', 0.1],
        ['20210105', '000008.SZ', 0.1],
        ['20210105', '000009.SZ', 0.1],
        ['20210105', '000010.SZ', 0.1],
        ['20210105', '000011.SZ', 0.1],
        ['20210105', '000012.SZ', 0.1],

        ['20210106', '000004.SZ', 0.1],
        ['20210106', '000005.SZ', 0.1],
        ['20210106', '000006.SZ', 0.1],
        ['20210106', '000007.SZ', 0.1],
        ['20210106', '000008.SZ', 0.1],
        ['20210106', '000009.SZ', 0.1],
        ['20210106', '000010.SZ', 0.1],
        ['20210106', '000011.SZ', 0.1],
        ['20210106', '000012.SZ', 0.1],
        ['20210106', '000013.SZ', 0.1],
    ]
    positions = [
        ['20210104', '000023.SZ', 0.15],
        ['20210104', '000016.SZ', 0.05],
        ['20210104', '000004.SZ', 0.1],
        ['20210104', '000005.SZ', 0.1],
        ['20210104', '000006.SZ', 0.1],
        ['20210104', '000007.SZ', 0.1],
        ['20210104', '000008.SZ', 0.1],
        ['20210104', '000014.SZ', 0.1],
        ['20210104', '000010.SZ', 0.1],
        ['20210104', '000011.SZ', 0.1],

        ['20210105', '000021.SZ', 0.1],
        ['20210105', '000002.SZ', 0.1],
        ['20210105', '000004.SZ', 0.1],
        ['20210105', '000005.SZ', 0.1],
        ['20210105', '000006.SZ', 0.15],
        ['20210105', '000017.SZ', 0.05],
        ['20210105', '000008.SZ', 0.1],
        ['20210105', '000019.SZ', 0.1],
        ['20210105', '000010.SZ', 0.1],
        ['20210105', '000011.SZ', 0.1],

        ['20210106', '000020.SZ', 0.1],
        ['20210106', '000012.SZ', 0.1],
        ['20210106', '000004.SZ', 0.1],
        ['20210106', '000005.SZ', 0.1],
        ['20210106', '000006.SZ', 0.1],
        ['20210106', '000007.SZ', 0.1],
        ['20210106', '000013.SZ', 0.1],
        ['20210106', '000009.SZ', 0.15],
        ['20210106', '000010.SZ', 0.05],
        ['20210106', '000011.SZ', 0.1]
    ]
    benchmark_data = pd.DataFrame(benchmark, columns=['日期', '代码', '权重'])
    positions_data = pd.DataFrame(positions, columns=['日期', '代码', '权重'])

    output_path = ''
    # 2. 调用接口
    outcome = brinson(benchmark_data, positions_data, industry_data, stock_return_data, output_path)

    print(outcome.values)


if __name__ == '__main__':
    main()
    data = [[0., 0., 0., 0.],
            [0.00259725, 0.0025685, 0.0016157, -0.00158695],
            [0.01447521, 0.00998372, 0.01697335, -0.01248186],
            [0.01625212, 0.01493057, 0.01975691, -0.01843536]]
    # for row in data:
    #     print(row[0], sum(row[1:]), round(row[0], 5) == round(sum(row[1:]), 5))
