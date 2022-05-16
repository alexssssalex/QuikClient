* установить QUIK;
* создать в QUIK папку lua и script;
* скопировать в папку **script** файл QuikServer.lua
* для Lua 5.3:
  * скачать библиотеку https://github.com/finsight/QUIKSharp.git (уже скачанный архив QUIKSharp-master.zip)
  * копировать из архива папку QUIKSharp-master.zip\QUIKSharp-master\src\QuikSharp\lua\clibs64\53_MT\scoket в QUIK\socket;
  * копировать из архива из папки QUIKSharp-master.zip\QUIKSharp-master\src\QuikSharp\lua файлы dkjson.lua и
  socket.lua  в папку QUIK/lua;
* для Lua 5.4: 
  * скачать библиотеку luasocket из списка https://quik2dde.ru/viewtopic.php?id=293 (уже скачанный архив luasocket.zip)
  * копировать из архива luasocket.zip\socket\core.dll в \QUIK\socket\
  * копировать из архива luasocket-3.0-5.4.3.zip\x64\socket.lua  в \QUIK\lua\
  * файл  dkjson.lua  необходимо положить в QUIK/lua как описано выше для версии Lua 5.3
* запустить QUIK;
* запустить script QuikServer.lua;
