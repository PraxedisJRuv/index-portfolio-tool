def amount_of_periods(period):
    #from inputs import start_date as start
    #from inputs import end_date as end
    from main_module import start 
    from main_module import end
    num_periods = (end - start) / period
    round_num_periods=(end - start)//period
    if num_periods!=round_num_periods:
        round_num_periods=round_num_periods+1
    return round_num_periods

def index_value(index, period, index_name):
    index_v=index[f"{index_name} Close"].resample(period).mean()
    return index_v

def index_returns(index,period,index_name):
    periods=amount_of_periods(period)
    index_v=index_value(index, period, index_name)
    index_r=[0]*periods
    for i in range(periods-1):
        index_r[i]=(index_v[i+1]/index_v[i])-1
    return index_r

def calc_dev_by_period(df,companies, period):
    deviations_by_period=[]
    for company in companies:
        deviation=(df[f"{company} High"] - df[f"{company} Low"]).resample(period).std()
        deviations_by_period.append(deviation)
    return deviations_by_period

def calc_vola(df, companies, period):
    deviations_by_period=calc_dev_by_period(df,companies, period)
    num_periods=amount_of_periods(period)
    volatility_weight=[]
    for i in range(num_periods):
        volatility_weight.append([])
        desv_sum=0
        for j in range(len(companies)):
            deviations_by_period[j][i]=1/deviations_by_period[j][i]
            desv_sum=desv_sum+deviations_by_period[j][i]
        for j in range(len(companies)):
            volatility_weight[i].append(deviations_by_period[j][i]/desv_sum)
    return volatility_weight

def calc_EW(companies, period):
    ew_weight=[]
    num_periods=amount_of_periods(period)
    weight=1/len(companies)
    for i in range(num_periods):
        ew_weight.append([])
        for j in range(len(companies)):
            ew_weight[i].append(weight)
    return ew_weight
