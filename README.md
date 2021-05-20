# Bitmex Trading Bot

### Introduce

Bitmex API를 사용하여 정해진 로직에 따라 트레이딩하는 프로그램

Bitmex 에서 제공하는 오픈소스에 따라 해당 데이터를 DB에 기록함.
[Bitmex API Connector - Python-Swaggerpy](https://github.com/BitMEX/api-connectors/tree/master/official-http/python-swaggerpy)
- 현재 가격(Current Price)
- 한달간의 OHLC -> Moving Average

핵심 로직은 main.py를 수정하여 구현하면 된다.

+ 현재 다시 구현하려면 리팩토링이 필요한 상태.
-> 비트코인 광풍이므로 다시 해보고 싶음, 여유 생기면 다시 해보기
