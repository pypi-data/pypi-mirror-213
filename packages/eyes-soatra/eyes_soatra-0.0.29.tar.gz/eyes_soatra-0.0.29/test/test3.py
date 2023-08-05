#!python3
from eyes_soatra import eyes
import json

res = eyes.view_page(
    url = 'https://www.city.chitose.lg.jp/docs/4467.html',
)
js = json.dumps(
    res,
    ensure_ascii=False,
    indent=4
)

print(js)