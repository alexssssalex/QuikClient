socket = require("socket") -- Указатель для работы с sockets
json = require( "dkjson" ) -- библиотека json
IPAddr = "127.0.0.1"       --IP Адрес
IPPort = 3587             --IP Port  
size_bufer = 1024         -- bufer for taransfer by socket
is_run = true


-- Функция вызывается перед вызовом main
function OnInit(path)
--    создает socket для подсоединения клиента
-- create a TCP socket and bind it to the local host, at port IPPort
  server = assert(socket.bind(IPAddr, IPPort))
  message(string.format("Server started. IP: %s; Port: %d\n", IPAddr, IPPort), 1);
end;

-- Функция вызывается перед остановкой скрипта
function OnStop(signal)
  message('I get stop')
  is_run = false
end;

--Этой функцией заменен парсер. Саму ее нужно применять с осторожностью, т.к. это может нарушить безопасность системы.
--Она позволяет выполнять любой луа-код, поступивший со стороны клиента
function _evalString (str)
  return assert(loadstring("return "..str))()
end



function _split_string_to_list( str )
--    функции из строки с разделителем запятая создает массив
  word = {}
  for w in string.gmatch(str,"%a+") do
    word[#word+1]=w
  end
  return word
end


function get_classes_list()
  -- получить список класов интсрумента (акции, биржи, и т.д). Возвращает список ["SPBFUT","RTSIDX","SPBOPT","CROSSRATE","CETS","SMAL","INDX","TQBR","TQQI","TQDE"]
  return _split_string_to_list(getClassesList())
end

function get_class_info(class)
--   -- получить описание класса 
-- {
--   "firmid":"MC0139600000",
--   "name":"МБ ФР: Т+ Акции и ДР",
--   "code":"TQBR",
--   "npars":64,
--   "nsecs":260
-- }
  return getClassInfo(class)
end

function get_class_codes(class)
  -- получить список кодов по классу
  -- "ABRD","AFKS","AFLT","AGRO","AKRN","ALBK","ALNU","ALRS","AMEZ","APTK","AQUA","ARSA","ASSB
  return _split_string_to_list(getClassSecurities(class))
end

function get_class_code_info(class, class_code)
--    информация по коду класса
--{'isin_code': 'RU0007661625', 'bsid': '', 'cusip_code': '', 'stock_code': '', 'couponvalue': 0,
    return getSecurityInfo(class, class_code)
end

function get_candle_data(class, class_code, interval)
--    INTERVAL_M1, INTERVAL_M2,...,INTERVAL_M6, INTERVAL_M10,INTERVAL_M15, INTERVAL_M20, INTERVAL_M30,
--    INTERVAL_H1, INTERVAL_H2, INTERVAL_H4, INTERVAL_D1, INTERVAL_W1, INTERVAL_MN1
    data = {}
    local number_iteration_max = 10
    local number_iteration = 0
    local time_wait = 50
    ds, err_msg = CreateDataSource(class, class_code, interval)
    while (number_iteration<number_iteration_max) and (ds:Size()<=0) and (ds ~= nil) do
        sleep(time_wait)
        number_iteration = number_iteration+1
    end
    if (ds ~= nil) and ds:Size()>0 then
        for i = 1, ds:Size() do
            data[i] = {}
            data[i]['D']=string.format("%04d-%02d-%02d %02d:%02d:%02d", ds:T(i).year, ds:T(i).month,
                                                ds:T(i).day, ds:T(i).hour, ds:T(i).min, ds:T(i).sec)
    --        data[i]['T_year'] = ds:T(i).year..ds:T(i).month..ds:T(i).day
    --        data[i]['T_month'] = ds:T(i).month
    --        data[i]['T_day'] = ds:T(i).day
    --        data[i]['T_hour'] = ds:T(i).hour
    --        data[i]['T_min'] = ds:T(i).min
    --        data[i]['T_sec'] = ds:T(i).sec
            data[i]['V'] = ds:V(i)
            data[i]['O'] = ds:O(i)
            data[i]['L'] = ds:L(i)
            data[i]['C'] = ds:C(i)
            data[i]['H'] = ds:H(i)
        end;
    end
    return data
end

function is_connected()
    return true
end

function _get_table_from_string(str)
    data = {}
    local i = 1
--    message(' I get str'..str)
--    message(string.format("%d",#str))
    while i<=#str do
        table.insert(data, string.sub(str,i,i+size_bufer-1))
        i =  i+size_bufer
    end
    return data
end

function _send_result(result)
    result = json.encode(result)
    result=_get_table_from_string(result)
    client:send(json.encode(#result))
    for  i=1,#result do
        client:send(result[i])
    end
end

function main()
    while is_run do
        message('I wait client conection')
    --принять подсоединение клиента и прочитать команду
        client = server:accept()
        local cmd, err = client:receive()
--        message('I receive client data:'..cmd)
    --получить результат и длину строки для передачи в json
        result = _evalString(cmd)
--        result = get_candle_data("TQBR",'GAZP', INTERVAL_M5)
--        result = json.encode(result, { indent = true })
--        result_length_string = json.encode(string.len(result))
    --передать длину строки (первое сообщение) и результат(второе сообщение)
        _send_result(result)
--        client:send(result_length_string)
--        client:send(result)
--        message(result)
--        message('I sended data')
        client:close()
    end
    message('I end main')
end