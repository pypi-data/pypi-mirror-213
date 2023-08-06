'''
by MRC

Modification history
----------------------------------
新增TEJ_Api_Data.py供以下狀況使用:
1. fetch_csv方法。
2. 取得benchmark報酬率。
3. 取得無風險利率。


Reference
----------------------------------
requests_csv.py
'''

from zipline.sources import requests_csv   
from zipline.utils.calendar_utils import get_calendar
from zipline.errors import (MultipleSymbolsFound,
                            SymbolNotFound,
                            ZiplineError,
                            IllegalValueException,
                            IllegalDTypeException,
                            EmptyOutputException
                            )                             
from TejToolAPI.TejToolAPI import *            # 2023-05-19 TQ-tool-api
import zipline.pipeline.domain as domain             

import pandas as pd
import numpy 
import tejapi
import datetime
from dateutil.relativedelta import relativedelta
import sys
import pytz

from zipline.utils.calendar_utils import get_calendar  # 來源為exchange_calendar

from logbook import Logger

tejapi.ApiConfig.page_limit=10000   


logger = Logger("Requests Source Logger")


# Map from calendar name to default country code for that calendar.
# (相關程式碼在algorithm.py)
_DEFAULT_FETCH_TEJ_API_COUNTRY_CODES = {
    d.calendar_name: d.country_code for d in domain.BUILT_IN_DOMAINS
} 
 
# 利用calendar取得國別碼(相關程式碼在algorithm.py)
def default_fetch_TEJ_API_country_code(calendar):
    """
    Get a default country_code to use for fetch_csv symbol lookups.

    This will be used to disambiguate symbol lookups for fetch_csv calls if
    our asset db contains entries with the same ticker spread across
    multiple
    """
    return _DEFAULT_FETCH_TEJ_API_COUNTRY_CODES.get(calendar.name)



class PandasRequestsTEJ_API(object):
    '''
    新增data_source到data_portal供run_algorithm()使用(相關程式碼在algorithm.py)
       
    20230402 (by MRC)
    '''
    
    def __init__(
        self,     
        symbol_column,
        date_column,       
        date_format,
        trading_day,
        asset_finder,      
        columns,
        symbols,        
        timezone,
        start,
        end, 
        import_data,        
        country_code,
        pre_func,
		post_func,
        data_frequency,
        **kwargs,
    ):

       
        self.timezone = timezone
        self.symbol_column = symbol_column or "symbol"
        self.date_column = date_column
        self.data_frequency = data_frequency
        self.country_code = country_code
        self.date_format = None
        
        #self.trading_calendar=trading_calendar
        self.finder = asset_finder
        self.trading_day = trading_day
        #self.trading_day=self.trading_calendar.day
        
        self.start = start
        self.end = end
        self.columns = columns
        self.symbols = symbols
        self.pre_func = pre_func
        self.post_func = post_func
        
        self.Parm = self.TEJ_Python_Api_Parm(start = self.start,
                                             end = self.end,    
                                             columns = self.columns,
                                             symbols = self.symbols)
        self.import_data=import_data        
        #self.df = self.load_df()       

    def TEJ_Python_Api_Parm(self,     
                            start,
                            end,    
                            columns,
                            symbols):
        
        Parm={}

        Parm['start'] = start
        Parm['end'] = end
        Parm['columns'] = columns
        Parm['symbols'] = symbols
        
        return Parm

    def get_TEJ_Python_Api_Data(self):    
        
        try:
            
            df = get_history_data(ticker = self.Parm['symbols'],
                                  columns = self.Parm['columns'],
                                  # columns = ['coid','mdate']+self.Parm['columns'],
                                  start = self.Parm['start'],
                                  end = self.Parm['end'],
                                  transfer_to_chinese = False)
        except:
            raise Exception('function fetch_tej_api() return an empty dataframe.')      
        
        return df
      
            
    #時區:要改?
    def roll_dts_to_midnight(self, dts, trading_day):
    
        if len(dts) == 0:
            return dts

        return (
            pd.DatetimeIndex(
                (dts.tz_convert("US/Eastern") - pd.Timedelta(hours=16)).date,
                tz="UTC",
            )
            + trading_day
        )

    
    def parse_date_str_series(
        self,format_str, tz, date_str_series, data_frequency, trading_day
    ):
        """
        Efficient parsing for a 1d Pandas/numpy object containing string
        representations of dates.

        Note: pd.to_datetime is significantly faster when no format string is
        passed, and in pandas 0.12.0 the %p strptime directive is not correctly
        handled if a format string is explicitly passed, but AM/PM is handled
        properly if format=None.

        Moreover, we were previously ignoring this parameter unintentionally
        because we were incorrectly passing it as a positional.  For all these
        reasons, we ignore the format_str parameter when parsing datetimes.
        """

        # Explicitly ignoring this parameter.  See note above.
        if format_str is not None:
            logger.warn(
                "The 'format_str' parameter to fetch_csv is deprecated. "
                "Ignoring and defaulting to pandas default date parsing."
            )
            format_str = None

        tz_str = str(tz)
        if tz_str == pytz.utc.zone:
            parsed = pd.to_datetime(
                date_str_series.values,
                format=format_str,
                utc=True,
                errors="coerce",
            )
        else:
            parsed = (
                pd.to_datetime(
                    date_str_series.values,
                    format=format_str,
                    errors="coerce",
                )
                .tz_localize(tz_str)
                .tz_convert("UTC")
            )

        if data_frequency == "daily":
            parsed = self.roll_dts_to_midnight(parsed, trading_day)
        return parsed
        
        
                
    def _lookup_unconflicted_symbol(self, symbol):
        """
        Attempt to find a unique asset whose symbol is the given string.

        If multiple assets have held the given symbol, return a 0.

        If no asset has held the given symbol, return a  NaN.
        """
        
        try:
            uppered = symbol.upper()
            
        except AttributeError:
            # The mapping fails because symbol was a non-string
            return numpy.nan

        try:
            return self.finder.lookup_symbol(
                uppered,
                as_of_date=None,
                country_code=self.country_code,
            )
        except MultipleSymbolsFound:
            # Fill conflicted entries with zeros to mark that they need to be
            # resolved by date.
            return 0
            
        except SymbolNotFound:
            # Fill not found entries with nans.
            
            
            return numpy.nan



    def load_df(self):
               
        if self.import_data is None:
            df = self.get_TEJ_Python_Api_Data() 
            df = df.sort_values(by=['coid','mdate'])
            
        elif self.import_data is not None:
            df = self.import_data
        else:
            pass
                     
        
        if self.pre_func:
            df.reset_index(drop=True,inplace=True)
            df = self.pre_func(df)
        
        #必要(不然df.iloc[row_idx, df.columns.get_loc("sid")] = asset這個語法會有問題，導致sid配錯)
        df.reset_index(drop=True,inplace=True)   
        
                                    
        
        # Batch-convert the user-specifed date column into timestamps.
        df["dt"] = self.parse_date_str_series(
            self.date_format,
            self.timezone,
            df[self.date_column],
            self.data_frequency,
            self.trading_day,
        ).values
        

        # ignore rows whose dates we couldn't parse
        df = df[df["dt"].notnull()]
        
        #if self.symbol is not None:
        #    df["sid"] = self.symbol
        
        if self.finder:

            df.sort_values(by=self.symbol_column, inplace=True)

            # Pop the 'sid' column off of the DataFrame, just in case the user
            # has assigned it, and throw a warning
            try:
                df.pop("sid")
                warnings.warn(
                    "Assignment of the 'sid' column of a DataFrame is "
                    "not supported by Fetcher. The 'sid' column has been "
                    "overwritten.",
                    category=UserWarning,
                    stacklevel=2,
                )
            except KeyError:
                # There was no 'sid' column, so no warning is necessary
                pass

                       
            # Fill entries for any symbols that don't require a date to
            # uniquely identify.  Entries for which multiple securities exist
            # are replaced with zeroes, while entries for which no asset
            # exists are replaced with NaNs.
            unique_symbols = df[self.symbol_column].unique()
            sid_series = pd.Series(
                data=map(self._lookup_unconflicted_symbol, unique_symbols),
                index=unique_symbols,
                name="sid",
            )
            df = df.join(sid_series, on=self.symbol_column)        

            # Fill any zero entries left in our sid column by doing a lookup
            # using both symbol and the row date.
            conflict_rows = df[df["sid"] == 0]
            for row_idx, row in conflict_rows.iterrows():
                try:
                    asset = (
                        self.finder.lookup_symbol(
                            row[self.symbol_column],
                            # Replacing tzinfo here is necessary because of the
                            # timezone metadata bug described below.
                            row["dt"].replace(tzinfo=pytz.utc),
                            country_code=self.country_code,
                            # It's possible that no asset comes back here if our
                            # lookup date is from before any asset held the
                            # requested symbol.  Mark such cases as NaN so that
                            # they get dropped in the next step.
                        )
                        or numpy.nan
                    )
                except SymbolNotFound:
                    asset = numpy.nan

                # Assign the resolved asset to the cell
                df.iloc[row_idx, df.columns.get_loc("sid")] = asset
            
            # Filter out rows containing symbols that we failed to find.
            length_before_drop = len(df)
            df = df[df["sid"].notnull()]
            no_sid_count = length_before_drop - len(df)
            if no_sid_count:
                logger.warn(
                    "Dropped {} rows from fetched csv.".format(no_sid_count),
                    no_sid_count,
                    extra={"syslog": True},
                )
        else:
            pass
        
                   
        # Dates are localized to UTC when they come out of
        # parse_date_str_series, but we need to re-localize them here because
        # of a bug that wasn't fixed until
        # https://github.com/pydata/pandas/pull/7092.
        # We should be able to remove the call to tz_localize once we're on
        # pandas 0.14.0

        # We don't set 'dt' as the index until here because the Symbol parsing
        # operations above depend on having a unique index for the dataframe,
        # and the 'dt' column can contain multiple dates for the same entry.
        df.drop_duplicates(["sid", "dt"])
        df.set_index(["dt"], inplace=True)
        df = df.tz_localize("UTC")
        df.sort_index(inplace=True)
        
 
        cols_to_drop = [self.date_column]
        
        cols_to_drop.append(self.symbol_column)
        df = df[df.columns.drop(cols_to_drop)]
        
        if self.post_func:
            df = self.post_func(df)
			
        return df

################################################################################
# 給使用者使用的函數

def get_Benchmark_Return(start,
                         end,    
                         symbol):
    '''
    為了計算benchmark_period_return,benchmark_volatility...
    
    return 
    ------------
    Series
    
    20230402 (by MRC)
    '''
   
    if not isinstance(symbol, list):
        raise IllegalDTypeException(parameter = '"symbol"',
                                    dtype = '"list"') 
    if len(symbol)>1:
       raise Exception('You can only choose one symbol')
    
    #TO DO:chk symbol是否為報酬指數
    
    TEJ_Api_data_source=PandasRequestsTEJ_API(
                            symbol_column = None,
                            date_column = None,                                       
                            date_format = None,
                            trading_day = None,
                            asset_finder= None,
                            columns = ['roi'], # ['coid','mdate','roi']
                            symbols = symbol,
                            timezone = None,
                            start = start,
                            end = end, 
                            import_data = None, 
                            country_code = None,
                            data_frequency = None,
                            pre_func = None,
                            post_func = None)
        
    df = TEJ_Api_data_source.get_TEJ_Python_Api_Data()        

    if len(df)==0:
        raise EmptyOutputException(function = '"get_Benchmark_Return()"',
                                   dtype = '"dataframe"')  
	
	#將利率單位轉成%
    df.iloc[:,2] = df.iloc[:,2] / 100                                # 20230505 (by MRC) TejToolAPI_20230427版本輸出的欄位名稱有改(改用iloc)
    ser = pd.Series(data = df.iloc[:,2].values, index = df['mdate']) # 20230505 (by MRC) TejToolAPI_20230427版本輸出的欄位名稱有改(改用iloc)
    
    #參考: zipline\data\benchmarks.py    
    if not ser.index.tz:
        ser = ser.tz_localize("utc")
       
    return ser.sort_index(ascending=True)
#----------------------------------------------------------------------------
def Bank_symbol_TW(name, return_type = 'DataFrame'):
    '''
    查台灣銀行股票代碼，取得無風險利率用。

    供以下方法使用
    ----------------------------------
    1. get_Bank_symbol()
    2. get_Treasury_Return()
      
    20230402 (by MRC)
    '''    
    
    if (return_type!='DataFrame') & (return_type!='symbol'):
        raise Exception('valid return_type parameter: DataFrame or symbol')
    
    df_Aind = tejapi.get('TWN/AIND',opts = {'columns':['coid','fnamec','tejind3_c','inamec','fnamee','inamee']}, paginate = True)
    df_Pind = tejapi.get('TWN/PIND',opts = {'columns':['coid','fnamec','tejind3_c','snamec','fnamee','snamee']}, paginate = True)

    df_Aind1 = df_Aind.query('tejind3_c.str.contains("M28A")', engine = 'python')
    df_Pind1 = df_Pind.query('tejind3_c.str.contains("M28A")', engine = 'python').rename(columns = {'snamec':'inamec',
                                                                                                    'snamee':'inamee'})
    df_bank = df_Pind1.append(df_Aind1).rename(columns = {'coid':'symbol'})

    search1 = (df_bank['fnamec'].str.contains(name))
    search2 = (df_bank['fnamee'].str.contains(name))
    search3 = (df_bank['inamec'].str.contains(name))
    search4 = (df_bank['inamee'].str.contains(name))
    search5 = (df_bank['symbol'].str.contains(name))
    
    if return_type=='DataFrame':
        return df_bank[search1 | search2 | search3 | search4 | search5 ].\
                   drop(columns = ['tejind3_c']).\
                   drop_duplicates(subset = ['symbol'],
                                   keep = 'first').\
                   reset_index(drop=True).\
                   set_index('symbol')
    
    elif return_type=='symbol':
        return df_bank[search1 | search2 | search3 | search4 | search5 ].\
                   drop(columns = ['tejind3_c']).\
                   drop_duplicates(subset = ['symbol'],
                                   keep = 'first').symbol.values  
    else:
        pass

def get_Bank_symbol(name,
                    return_type = 'DataFrame',
                    trading_calendar = get_calendar('TEJ_XTAI')):
    '''
    查銀行股票代碼，取得無風險利率用。

    供以下方法使用
    ----------------------------------
    1. get_Bank_symbol()
    2. get_Treasury_Return()
      
    20230402 (by MRC)
    ''' 
    
    country_code = default_fetch_TEJ_API_country_code(
        trading_calendar,
    )
        
    BANK_FUNC_NAMES = {
        'TW': Bank_symbol_TW
    }
    
    if country_code not in BANK_FUNC_NAMES.keys():
        raise IllegalValueException(parameter = '"country_code"',
                                    value = str(list(set(BANK_FUNC_NAMES.keys()))))    
   

   
    df = BANK_FUNC_NAMES[country_code](name = name,
                                       return_type = return_type)
                                             
    if len(df)==0:
        raise EmptyOutputException(function = '"get_Bank_symbol()"',
                                   dtype = '"dataframe"')          
    return df    
#----------------------------------------------------------------------------
def Treasury_Return_TW(start,
                       end,
                       rate_type,
                       term,
                       symbol = None):
    '''
    TW Treasury：為了計算excess return...
    
    return 
    ------------
    Series
    
    20230402 (by MRC)
    '''
    valid_rate_type = ['Time_Deposit_Rate','TAIBOR','Gov_Bond']
    
    Time_Deposit_Rate_terms = {'1m':'fld005',
                               '3m':'fld006',
                               '6m':'fld007',
                               '9m':'fld008',
                               '1y':'fld009'}

    Benchmark_Gov_Bond_terms = {#'0y':'TY00',
                                '2y':'TY02',
                                '5y':'TY05',
                                '10y':'TY10',
                                '12y':'TY12',
                                '20y':'TY20',
                                '30y':'TY30'}
   
    TAIBOR_terms = {'1w':'tw1',
                    '2w':'tw2',
                    '1m':'tm1',
                    '2m':'tm2',
                    '3m':'tm3',
                    '6m':'tm6',                    
                    '9m':'tm9',
                    '1y':'tm12'}

    if not isinstance(rate_type, str):
        raise IllegalDTypeException(parameter = '"rate_type"',
                                    dtype = '"str"')   
    if not isinstance(term, str):
        raise IllegalDTypeException(parameter = '"term"',
                                    dtype = '"str"')
    if not isinstance(symbol, str) and symbol is not None:
        raise IllegalDTypeException(parameter = '"symbol"',
                                    dtype = '"str"') 

        
    if rate_type not in valid_rate_type:
        raise IllegalValueException(parameter = '"rate_type"',
                                    value = valid_rate_type) 
                        
    elif rate_type=='Time_Deposit_Rate' and term not in Time_Deposit_Rate_terms.keys():
         raise IllegalValueException(parameter = '"terms"',
                                     value = str(list(set(Time_Deposit_Rate_terms.keys())))) 
                                    
    elif rate_type=='Gov_Bond' and term not in Benchmark_Gov_Bond_terms.keys():    
         raise IllegalValueException(parameter = '"terms"',
                                     value = str(list(set(Benchmark_Gov_Bond_terms.keys()))))
        
    elif rate_type=='TAIBOR' and term not in TAIBOR_terms.keys():            
         raise IllegalValueException(parameter = '"terms"',
                                     value = str(list(set(TAIBOR_terms.keys())))) 
        
    else:
        pass

    # 銀行定存利率    
    if rate_type=='Time_Deposit_Rate':
        
        df = tejapi.get('TWN/ARATE',
                        coid = symbol,
                        opts = {'columns':['coid','mdate',Time_Deposit_Rate_terms[term]]},
                        mdate = {'gte':start,'lte':end},
                        paginate = True)
    
    # TAIBOR
    elif rate_type=='TAIBOR':
        df = tejapi.get('GLOBAL/WIBOR1',
                       coid = 'Z9999',
                       opts = {'columns':['coid','mdate',TAIBOR_terms[term]]},
                       mdate = {'gte':start,'lte':end},
                       paginate = True)        
    
    # 指標公債殖利率
    elif rate_type=='Gov_Bond':
        df = tejapi.get('TWN/AGBD8A',
                        coid = Benchmark_Gov_Bond_terms[term],
                        opts = {'columns':['coid','mdate','yield']},
                        mdate = {'gte':start,'lte':end},
                        paginate = True)
    else:
        raise EmptyOutputException(function = '"get_Treasury_Return() & Treasury_Return_TW()"',
                                   dtype = '"dataframe"')               
    return df       
 
def get_Treasury_Return(start,
                        end,
                        rate_type,
                        term,
                        symbol = None,
                        trading_calendar = get_calendar('TEJ_XTAI')):

    '''
    為了計算excess return...
    
    return 
    ------------
    Series
    
    20230402 (by MRC)
    '''
    
    country_code = default_fetch_TEJ_API_country_code(
        trading_calendar,
    )
        
    ''' 
    # query country_code
    
    from iso3166 import countries_by_name
    name = "TAIWAN, PROVINCE OF CHINA"      # zipline.country.py
    print(countries_by_name[name].alpha2)
    '''

    TREASURY_FUNC_NAMES = {
        'TW': Treasury_Return_TW
    }
    
    if country_code not in TREASURY_FUNC_NAMES.keys():
        raise IllegalValueException(parameter = '"country_code"',
                                    value = str(list(set(TREASURY_FUNC_NAMES.keys()))))      
       
    df = TREASURY_FUNC_NAMES[country_code](start = start,
                                           end = end,
                                           rate_type = rate_type,
                                           term = term,
                                           symbol = symbol)
                                             
    if len(df)==0:
        raise EmptyOutputException(function = '"get_Treasury_Return()"',
                                   dtype = '"dataframe"')  
    
    #將利率單位轉成%，再將年利率轉為日利率
    df.iloc[:,2] = df.iloc[:,2].apply(lambda x: pow((1 + x / 100), (1 / 252)) - 1) 
    
    ser = pd.Series(data = df.iloc[:,2].values, index = df['mdate'])
    
    #參考: zipline\data\benchmarks.py    
    if not ser.index.tz:
        ser = ser.tz_localize("utc")
       
    return ser.sort_index(ascending=True)

        







