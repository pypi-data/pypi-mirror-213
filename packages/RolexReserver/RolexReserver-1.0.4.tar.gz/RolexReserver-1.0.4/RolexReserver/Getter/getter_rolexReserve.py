import datetime
import LibHanger.Library.uwLogger as Logger
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame
from enum import Enum
from LibHanger.Models.recset import recset
from Scrapinger.Library.browserContainer import browserContainer
from RolexReserver.Library.rolexReserverConfig import rolexReserverConfig
from RolexReserver.Library.rolexReserverGlobals import *
from RolexReserver.Library.rolexReserverException import getterError
from RolexReserver.Getter.Base.baseGetter import baseGetter
from RolexReserver.Models.log_reserve import log_reserve

class getter_rolexReserve(baseGetter):
    
    """
    予約サイト巡回
    """
    
    def __init__(self) -> None:
        
        """
        コンストラクタ
        """
        
        super().__init__()

        # レコードセット初期化
        self.init_recset()

        # スクレイピング準備
        self.wdc.settingScrape()
            
    def init_recset(self):
        
        """
        レコードセット初期化
        """

        # レコードセット初期化
        self.rslogReserve = recset[log_reserve](log_reserve)

    @Logger.loggerDecorator("getData")
    def getData(self, *args, **kwargs):
        
        """
        予約状況取得
        
        Parameters
        ----------
        None
        
        """
        
        try:
            kwargs['getter'] = self
            
            # 予約状況取得
            for times in range(int(gv.rolexReserverConfig.gettingCount)):
                Logger.logging.info('times = {}'.format(str(times + 1)))
                self.getRolexReserveDataToDataFrame(**kwargs)
            
        except Exception as e: # その他例外
            Logger.logging.error(str(e))
            raise getterError
        
    def cbCheckMem():
        pass
    
    @Logger.loggerDecorator("getStockDataToDataFrame")
    def getRolexReserveDataToDataFrame(self, *args, **kwargs):

        """
        予約状況取得
        
        Parameters
        ----------
        None
        
        """
        
        # 検索url(ルート)
        rootUrl = gv.rolexReserverConfig.rolexUrl

        # ウィンドウサイズを1200x1000にする
        self.wdc.browserCtl.changeBrowserSize('1200', '1000')
        
        # ページロード
        kwargs['loadPagetime'] = datetime.datetime.now()
        self.wdc.browserCtl.loadPage(rootUrl)
        
        # pandasデータを返却する
        return self.wdc.browserCtl.createSearchResultDataFrame(**kwargs)

    class chrome(browserContainer.chrome):
        
        """
        ブラウザコンテナ:chrome
        """

        class reserveStatusEnum(Enum):
            
            """
            予約状況
            """
            
            canNotBeReserved = 0
            """ 予約不可 """
            
            canBeReserved = 1
            """ 予約可 """
            
        def __init__(self, _config: rolexReserverConfig):
            
            """
            コンストラクタ
            
            Parameters
            ----------
                _config : rolexReserverConfig
                    共通設定
            """
            
            super().__init__(_config)

            self.config = _config
            self.cbCreateSearchResultDataFrameByWebDriver = self.createSearchResultDataFrameByWebDriver

        def createSearchResultDataFrameByWebDriver(self, element, *args, **kwargs) -> DataFrame:
            
            """
            予約状況をDataFrameで返す(By Selenium)
            """
            
            return self.getReserveData(element, *args, **kwargs)

        def getReserveData(self, element, *args, **kwargs):
            
            """
            予約状況をDataFrameで返す(By Selenium)
            
            Parameters
            ----------
            kwargs : getter_rolexReserve
                @getter
                    Getterクラス
            """
            
            # getterインスタンス取得
            bc:getter_rolexReserve = kwargs.get('getter')

            # loadPage時の時刻を取得
            loadPagetime = kwargs.get('loadPagetime')
            
            # 次週ボタンをクリックする
            
            # html解析
            html = element.parent.page_source
            bsSrc = BeautifulSoup(html, 'lxml')
            
            # スクレイピング結果から改行ｺｰﾄﾞを除去
            [tag.extract() for tag in bsSrc(string='\n')]
            
            # 予約状況テーブル取得
            reservedTables = bsSrc.contents[0].contents[1].find_all(class_="ly-mainMsg")[0]
            
            # ログデータmodel用意
            rslogReserve = recset[log_reserve](log_reserve) 
            rslogReserve.newRow()
            rslogReserve.fields(log_reserve.logtime.key).value = loadPagetime
            
            # 予約状況
            reserveStatus:self.reserveStatusEnum
            
            if reservedTables:
                
                # 選択可能なメニューがあるかどうか判別
                if reservedTables.contents[0].text:
                    
                    # 選択可能な予約メニューの存在チェック
                    # '選択可能な予約メニューがありません。'が含まれるかどうか
                    menuExistsMsg = reservedTables.contents[0].text
                    if self.config.menuExistsMsgString in menuExistsMsg:
                        Logger.logging.info(self.config.menuExistsCheckLogFormat.format(self.config.menuExistsCheckLogNoData))
                        reserveStatus = self.reserveStatusEnum.canNotBeReserved.value
                        getHtml = ''
                    else:
                        Logger.logging.info(self.config.menuExistsCheckLogFormat.format(self.config.menuExistsCheckLogExistsData))
                        reserveStatus = self.reserveStatusEnum.canBeReserved.value
                        getHtml = html
                
            else:
                Logger.logging.info(self.config.menuExistsCheckLogFormat.format('Data Not Exists.'))

            rslogReserve.fields(log_reserve.status.key).value = reserveStatus
            rslogReserve.fields(log_reserve.html.key).value = getHtml
            rslogReserve.fields(log_reserve.updinfo.key).value = bc.getUpdInfo()
            
            # レコードセットマージ
            bc.rslogReserve.merge(rslogReserve, False)
            
            return None

    class beautifulSoup(browserContainer.beautifulSoup):
        
        """
        ブラウザコンテナ:beautifulSoup
        """

        def __init__(self, _config: rolexReserverConfig):
            
            """
            コンストラクタ
            
            Parameters
            ----------
                _config : rolexReserverConfig
                    共通設定
            """

            super().__init__(_config)
            
            self.config = _config
            self.cbCreateSearchResultDataFrameByBeutifulSoup = self.createSearchResultDataFrameByBeutifulSoup
            