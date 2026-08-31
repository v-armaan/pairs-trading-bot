from src.pairs import cointegration,spread

def select_pairs(formation_prices,candidate_pairs):
    coint_pairs=cointegration.find_cointegrated_pairs(formation_prices,candidate_pairs)
    selected_pairs=[]
    for pair in coint_pairs:
        alpha,beta=cointegration.fit_hedge_ratio(formation_prices,pair)
        spread_for_adf=spread.calculate_spread(formation_prices,pair,alpha,beta)
        adf_p=cointegration.adf_test(spread_for_adf)
        
        if adf_p<0.05:
            selected_pairs.append(
                (pair[0],pair[1],pair[2],adf_p,alpha,beta)
            )
    
    return selected_pairs
    