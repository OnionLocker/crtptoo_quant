# -*- coding: utf-8 -*-
# analyzers.py

def extract_trade_analysis(analyzers):
    stats = analyzers.getbyname("tradeanalyzer").get_analysis()
    
    total_trades = stats.get('total', {}).get('total', 0)
    won_trades = stats.get('won', {}).get('total', 0)
    lost_trades = stats.get('lost', {}).get('total', 0)
    pnl_won = stats.get('won', {}).get('pnl', {}).get('avg') or 0
    pnl_lost = stats.get('lost', {}).get('pnl', {}).get('avg') or 0

    win_rate = (won_trades / total_trades) * 100 if total_trades > 0 else 0

    if pnl_lost == 0:
        if pnl_won > 0:
            profit_factor = float('inf')
        else:
            profit_factor = None
    else:
        profit_factor = abs(pnl_won / pnl_lost)

    return {
        '总交易次数': total_trades,
        '盈利交易数': won_trades,
        '亏损交易数': lost_trades,
        '平均盈利': pnl_won,
        '平均亏损': pnl_lost,
        '胜率': win_rate,
        '盈亏比（Profit Factor）': profit_factor
    }

def analyze_results(results, analyzers, strategy_name):
    trade_stats = extract_trade_analysis(analyzers)
    profit_factor = trade_stats.get('盈亏比（Profit Factor）')
    if profit_factor is None:
        profit_factor_str = 'N/A'
    elif profit_factor == float('inf'):
        profit_factor_str = '∞'
    else:
        profit_factor_str = round(profit_factor, 4)

    results.update({
        '策略名称': strategy_name,
        '总交易次数': trade_stats.get('总交易次数', 0),
        '胜率': round(trade_stats.get('胜率', 0), 2),
        '盈亏比': profit_factor_str
    })
    return results