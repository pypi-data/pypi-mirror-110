# ko_lm_dataformat

- 한국어 언어모델 학습 데이터를 저장하기 위한 유틸리티
- 코드는 EleutherAI에서 사용하는 [lm_dataformat](https://github.com/leogao2/lm_dataformat)를 참고하여 제작.

  - 일부 버그 수정
  - 한국어에 맞게 기능 추가 및 수정 (sentence splitter, text cleaner)

- [`zstandard`](https://github.com/facebook/zstd), [`ultrajson`](https://github.com/ultrajson/ultrajson) 을 사용하여 데이터 압축 속도 개선

## Install

```bash
pip install ko_lm_dataformat
```

## What have been changed

### 기능 추가

- Sentence splitter
  - `kss v1.3.1`

### 로직 변경

- 기존과 달리 `json`의 `"text"` 는 무조건 하나의 document만 받음.
  - `str` 이 아닌 `List[str]` 로 들어오게 되면 기존에는 각 str이 document였으나, 여기서는 sentence로 취급.
  - 기존에는 여러 document를 `\n\n`으로 join 하였지만, `ko_lm_dataformat` 에서는 해당 로직을 없앰.

## Usage

To write:

```python
import ko_lm_dataformat as kldf

ar = kldf.Archive('output_dir')

for x in something():
  # do other stuff
  ar.add_data(somedocument, meta={
    'example': stuff,
    'someothermetadata': [othermetadata, otherrandomstuff],
    'otherotherstuff': True
  })

# remember to commit at the end!
ar.commit()
```

To read:

```python
import ko_lm_dataformat as kldf

rdr = kldf.Reader('input_dir_or_file')

for doc in rdr.stream_data(get_meta=False):
  # do something with the document
```
