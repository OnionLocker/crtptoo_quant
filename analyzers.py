# -*- coding: utf-8 -*-
# analyzers.py

def extract_trade_analysis(analyzers):
    stats = analyzers.getbyname("tradeanalyzer").get_analysis()

    total = stats.total.closed if 'total' in stats and 'closed' in stats.total else 0
    won = stats.won.total if 'won' in stats and 'total' in stats.won else 0
    lost = stats.lost.total if 'lost' in stats and 'total' in stats.lost else 0

    win_rate = (won / total) * 100 if total > 0 else 0

    pnl_won = stats.won.pnl.avg if 'won' in stats and 'pnl' in stats.won and stats.won.pnl.avg is not None else 0
    pnl_lost = stats.lost.pnl.avg if 'lost' in stats and 'pnl' in stats.lost and stats.lost.pnl.avg is not None else 0

    if pnl_lost != 0:
        profit_factor = abs(pnl_won / pnl_lost)
    else:
        profit_factor = None

    return {
        "total": total,
        "won": won,
        "lost": lost,
        "win_rate": win_rate,
        "profit_factor": profit_factor
    }

def analyze_results(results, analyzers, strategy_name):
    trade_stats = extract_trade_analysis(analyzers)
    results.update({
        'strategy_name': strategy_name,
        'total_trades': trade_stats['total'],
        'win_rate': round(trade_stats['win_rate'], 2),
        'profit_factor': round(trade_stats['profit_factor'], 4) if trade_stats['profit_factor'] else 'N/A'
    })
    return results
