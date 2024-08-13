# GA 實驗
## 1. 環境
windows、python3.10、pipenv
## 2. 前置工作
    pipenv install
生成虛擬環境並自動下載套件模組
## 3. 執行 scripts/00_prepare.bat檔案
    ./scripts/00_prepare.bat
----------
### 3.1 執行檔案內容(第一行)

    python .\data_generate.py exp1 30 3

#### 參數 :
* exp1 : 實驗編號
* 30   : 訂單數量
* 3   : 插單數量
### 3.2 執行檔案內容(第二行)

    python .\generate_scripts.py 1 10

#### 參數 :
* 1 : 實驗編號
* 10   : 執行次數
---------
## 5. 實驗

    ./scripts/01_exp.bat

透過剛剛生成的腳本直接執行即可開始實驗，腳本位置皆放在 scripts 中
