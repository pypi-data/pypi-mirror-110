jyoyou
===========

![image](https://img.shields.io/pypi/v/joyo)
![image](https://img.shields.io/pypi/pyversions/joyo)
![image](https://gitlab.com/yassu/jyoyou.py/badges/master/pipeline.svg)
![image](https://img.shields.io/pypi/l/joyo)

jyoyouは常用漢字一覧を取得するプロジェクトです.

簡単な漢字の一覧を取得したい時などに使用できると思います.

## 使い方

`joyo.load`関数を使って常用漢字一覧を取得する. その際, 常用漢字一覧が取得されていなければ 取得する:

``` python
import joyo

kanjis = joyo.load()
print(kanjis)
```

出力:

```
亜哀挨愛曖悪握圧扱宛嵐安案暗以衣位囲医依委威為畏胃尉異移萎偉椅彙意違維慰遺緯域育一
壱逸茨芋引印因咽姻員院淫陰飲隠韻右宇羽雨唄鬱畝浦運雲永泳英映栄営詠影鋭衛易疫益液駅
悦越謁閲円延沿炎怨宴媛援園煙猿遠鉛塩演縁艶汚王凹央応往押旺欧殴桜翁奥横岡屋億憶臆虞
乙俺卸音恩温穏下化火加可仮何花佳価果河苛科架夏家荷華菓貨渦過嫁暇禍靴寡歌箇稼課蚊牙
瓦我画芽賀雅餓介回灰会快戒改怪拐悔海界皆械絵開階塊楷解潰壊懐諧貝外劾害崖涯街慨蓋該
概骸垣柿各角拡革格核殻郭覚較隔閣確獲嚇穫学岳楽額顎掛潟括活喝渇割葛滑褐轄且株釜鎌刈
干刊甘汗缶完肝官冠巻看陥乾勘患 ...
...
```

パスを指定する:

``` python
from pathlib import Path


joyo.load(Path('/tmp/abc'))
```

常用漢字一覧を更新する:

``` python
joyo.update()
```

パス名も指定できる:

``` python
joyo.update('/tmp/abc')
```


LICENSE
-------

[MIT](https://gitlab.com/yassu/jyoyou.py/-/blob/master/LICENSE)
