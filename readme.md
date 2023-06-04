# 通用的網站爬蟲框架

## 步驟
1. 使用selenium打開網站
2. 捕捉事先設定好的商品頁面的class名稱
3. 對該物件的所有一級子物件進行截圖
4. 依照csv中描述的商品屬性來進行儲存
5. 使用ocr對每一張圖片進行解析
6. 將商品的商品屬性、價格、性別等等輸入sqlite的資料庫

| Field | Description |
| -----| ---- |
|oriprice|Original price of the item|
|price	|Current price of the item|
|imgcode|Filename of the item's image|
|facturer|Manufacturer of the item|
|color	|Number of Available Colors|
|name	|Name or title of the item|
|star	|Rating or number of stars for the item|
|path	|Location and feature of the item|
|sex	|The gender of the item|

## ocr

由於同一個網站對於所有商品會有相同的佈局

因此，使用ocr前事先將每一個對應的位置標記好有助於區分不同的資料屬性

`Labeler.html` 是一個靜態網頁，用來對圖片進行標記並將標記結果儲存為json

## 待完成程式碼
- [ ]輸入一個網頁物件(WebElement)後能對他做截圖的函式

- [ ]讀取一個檔案以決定如何進行下一頁或是show more切換的功能

- [x]讀取一張圖片並在圖片上標示方匡後將參數紀錄的靜態網頁

* [x]輸入一張圖片與四個數字(x,y,w,h)後能對子圖進行ocr辨識並返回一個字串的函式

## 額外要求

需安裝tesseract
> https://digi.bib.uni-mannheim.de/tesseract/

安裝完成後需要修改路徑名稱