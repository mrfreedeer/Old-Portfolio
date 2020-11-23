socket = require( "socket")
local json = require( "json")
client = ""



local communication = {}

function communication.connect(serverAddress)
    client = socket.connect(serverAddress,8000)
    client:settimeout(0)
    client:setoption("keepalive",true)
    if not client then 
        print("Error, could not connect to server")
        return false 
    else 
        return true
    end 
end

function wait()
    print("----------------------------------------")
end

function communication.sendMessage(message)
    client:send(message)
end

function communication.sendinfo(player, endturn)
    local info = {}
    pawnpositions = '{'
    for i, pawn in ipairs(player) do
        if table.indexOf(pawnsOut, i) == nil then
            pawnpositions  =  pawnpositions .. '"pawn'.. i ..'":'
            pawnpositions = pawnpositions .. '{"position":'.. pawn.pos
            pawnpositions = pawnpositions .. ',"colour":"' .. pawn.colour .. '"'
            if pawn.lap then 
                pawnpositions = pawnpositions .. ', "lap": true}, '
            else 
                pawnpositions = pawnpositions .. ', "lap": false}, '
            end
        end
    end
    if player.out then 
        pawnpositions = pawnpositions .. '"out": true'
    else 
        pawnpositions = pawnpositions .. '"out": false'
    end

    if endturn then 
        pawnpositions = pawnpositions .. ', "endturn": true'
    else 
        pawnpositions = pawnpositions .. ', "updateposition": true'
    end
    pawnpositions = pawnpositions .. '}'
    client:send(pawnpositions)
end

function communication.receiveInfo()
    
    local data, err = client:receive('*l')
    if data and not err then 
        print("INCOMING:\t",data)
        return data, true
    end
    return nil, false
end

function communication.sendTime()
    timestr ='{"hours":'
    timestr = timestr .. time.hour .. ', '
    timestr = timestr .. '"minutes":' .. time.min .. ', '
    timestr = timestr .. '"seconds":' .. time.sec ..'}'
    client:send(timestr)
end
return communication
