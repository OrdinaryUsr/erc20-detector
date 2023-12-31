Необходимо разработать детектор стандарта
[ERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/tree/master/contracts/token/ERC20)
от OpenZeppelin.

Сервис должен ходить в postgres, доставать из таблицы исходный
код контрактов, проводить анализ, выставлять флаги `is_erc20`, `status` в базе и, если он был обнаружен, указывать
первую подходящую версию стандарта со страницы релизов в github репозитории,

Таким образом таблица может содержать 4 поля: `contract_address`, `source_code`,
`is_erc20`, `erc20_version`, `status` (waits processing, processing, processed, failed)

Также следует предоставить возможности для добавления определения других
стандартов и горизонтального масштабирования.

Сервис не должен обращаться к каким либо внешним ресурсам при работе (кроме
postgres).

В решении можно использовать любые библиотеки\тулы с открытым исходным кодом.
Желательно писать на python не старше 3.10, использовать type hints и poetry.
Примеры контрактов с ERC20 можно посмотреть [тут](https://etherscan.io/tokens)

Подразумевается, что сервис (или несколько его инстансов) способен(ы) обработать
5млн контрактов в течение недели.
