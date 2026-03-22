import markowitz_cpp
def markowitz(Sigma, wb, alpha, lamb):
    w = markowitz_cpp.optimize_portfolio(Sigma, wb, alpha, lamb)
    return w
def markowitz_of_periods(Sigma,wb,alpha,lamb,num_periods):
    wt=[]
    for i in range(num_periods):
        wt.append(markowitz(Sigma,wb[i],alpha,lamb))
    return wt