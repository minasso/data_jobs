def import_csv(file):
    '''
    Import file and remove/reformat columns
    '''
    import pandas as pd
    f = pd.read_csv(file,)
    if 'Unnamed: 0' in f.columns:
        f = f.drop('Unnamed: 0', axis=1)
    if 'index' in f.columns:
        f = f.drop('index', axis=1)
    f.columns = map(str.lower, f.columns)
    f.columns = f.columns.str.replace(' ', '_')
    return f

def fix_salary(f):
    '''
    Fix the salary information
    '''
    f['salary_estimate'] = f['salary_estimate'].str.replace('\(Glassdoor est.\)', '')

    f['salary_estimate'] = f['salary_estimate'].str.replace('$', '').str.replace('K', '000')

    f['low_salary'] = f['salary_estimate'].str.split('-').str.get(0)
    f['high_salary'] = f['salary_estimate'].str.split('-').str.get(1)

    f.drop('salary_estimate', axis=1, inplace=True)

    try:
        f['low_salary'] = pd.to_numeric(f['low_salary'])

        f['high_salary'] = pd.to_numeric(f['high_salary'])

        f['mid_salary'] = (f['low_salary'] + f['low_salary']) / 2
    except:
        print('could not convert to numeric')


    return f

def fix_rest(f):
    '''
    Fix the location into city/state, clean company name
    '''
    f['city'] = f['location'].str.split(', ').str.get(0)
    f['state'] = f['location'].str.split(', ').str.get(-1)
    f = f.drop('location', axis=1)
    f['company_name'] = f['company_name'].str.split('\n').str.get(0)
    return f