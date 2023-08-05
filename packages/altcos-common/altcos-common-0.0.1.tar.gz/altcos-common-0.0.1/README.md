# altcos-common

Библиотека для удобного взаимодейтсвия с `altcos`-репозиториями.

# Пример

Получение последнего коммита
```python
import altcos
import os

from altcos import ostree

# Путь до корня altcos-репозитория
SR = os.environ["STREAMS_ROOT"]

# Создание экземпляра потока на основе названия ветки
stream = ostree.Stream.from_ostree_ref(SR, "altcos/x86_64/sisyphus")
# Открытие ostree репозитория (по умолчанию в режиме bare)
repo = ostree.Repository(stream).open()
# Получение последнего коммита
print(repo.last_commit())
```
