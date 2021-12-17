# QuikClient

* в QUIK запускается server на lua (см src/lua) - обеспечивает связь с QuikClient по socket;
* в python class QuikClient передает запросы и получает результаты;


## Build packet
* выполнить команду: *python -m build*
* команда создаст директорию *dist* с архивами для установки

## Install packet
* в Anaconda перейти в папку dist (или скопировать ее удобное место);
* выполнить команду:  *pip install ....gz*

## Uninstall packet
* в Anaconda выполнить команду:  *pip uninstall <имя_пакета>>*