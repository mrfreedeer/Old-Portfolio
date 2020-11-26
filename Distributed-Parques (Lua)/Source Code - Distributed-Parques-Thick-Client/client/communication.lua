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

function communication.sendMessage(message)
    client:send(message)
end

function communication.sendinfo(player, jailing)
    local info = {}
    pawnpositions = '{'
    for i, pawn in ipairs(player) do
        if table.indexOf(pawnsOut, i) == nil then
            if i ~= 4 then
                pawnpositions  =  pawnpositions .. '"pawn'.. i ..'":'.. pawn.pos .. ', '
            else 
                pawnpositions  =  pawnpositions .. '"pawn'.. i ..'":'.. pawn.pos .. ', '
            end
        end
    end
    if player.out then 
        pawnpositions = pawnpositions .. '"out": true'
    else 
        pawnpositions = pawnpositions .. '"out": false'
    end
    if jailing ~= '' then 
        pawnpositions = pawnpositions .. ", "..jailing 
    end
    pawnpositions = pawnpositions .. '}'
    client:send(pawnpositions)
end

function communication.receiveInfo()
    
    local data, err = client:receive('*l')
    if data and not err then 
        print(data)
        return data, true
    end
    return nil, false
end

return communication
