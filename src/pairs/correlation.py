def find_candidate_pairs(formation_returns, threshold):
    """
    Identify stock pairs with a correlation above the specified threshold.

    Parameters
    returns : pandas.DataFrame
        DataFrame containing the returns of multiple stocks, with each
        column representing a stock.
    threshold : float
        Minimum Pearson correlation coefficient required for a pair
        to be considered a candidate.

    Returns
    list of tuple
        List of candidate pairs in the form:
        (stock1, stock2, correlation)
    """
    

    corr_matrix =formation_returns.corr()

    candidate_pairs = []

    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):

            stock1 = corr_matrix.columns[i]
            stock2 = corr_matrix.columns[j]

            correlation = corr_matrix.iloc[i, j]

            if correlation >= threshold:
                candidate_pairs.append(
                    (stock1, stock2, correlation)
                )

    return candidate_pairs
