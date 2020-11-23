-----------------------------------------------------------------------------------------
--
-- game.lua
--
-----------------------------------------------------------------------------------------

local composer = require("composer")
local scene = composer.newScene()

local everything
local boardlib = require "board"
local widget = require "widget"
local filename = "dice"
local extension = ".png"
local halfH = display.contentHeight * 0.5
local halfW = display.contentWidth * 0.5
local diea = nil
local rolleda = {}
local rolledb = {}
local dieb = nil
local center = {halfW, halfH}
local globalboard
local blackies
local player = {}
local blackies = {}
local tappedpawn = nil
local pawnToTake = nil
local blockMessage = false
dicePictures = {}
turnText = {}
throwdiceText = {}
hasturnText = {}
local otherPlayers = {}
local equaldice = false
testing = true
-----   Test Area ----------
----------------------------
local otherplayersinfo = testing
local start = testing
local turn = testing 
----------------------------
local takePawn = false

player.out = false
player.colour = chosencolour
player.rolled = false
player.hasExitedBefore = false
player.playerid = playerid
player.nametext = {}
timesRolled = 0


local function drawName( playername, colour, homecolour) 
    if colour == 'red' then
        nametext = display.newText(playername, homecolour[1] -20, homecolour[2] - 50, native.systemFont, 15 )
    elseif colour == 'green' then
        nametext = display.newText(playername, homecolour[1]-20, homecolour[2] - 50, native.systemFont, 15 )
    elseif colour == 'yellow' then
        nametext = display.newText(playername, homecolour[1] -20, homecolour[2] + 50, native.systemFont, 15 )
    elseif colour == 'blue' then
        nametext = display.newText(playername, homecolour[1] -20 , homecolour[2] + 50, native.systemFont, 15 )
    end
end

local function resetTextColour(text)
    text:setTextColor(unpack(white))
end

local function resetNameHighlight(otherPlayers)
    for _, otherPlayer in ipairs(otherPlayers) do
        resetTextColour(otherPlayer.nametext)
    end
end

local function highlightName(player)
    if player.colour == 'red' then
        player.nametext:setTextColor(unpack(red))
    elseif player.colour == 'green' then
        player.nametext:setTextColor(unpack(green))
    elseif player.colour == 'yellow' then
        player.nametext:setTextColor(unpack(yellow))
    elseif player.colour == 'blue' then
        player.nametext:setTextColor(unpack(blue))
    end
end

local function highlightOtherPlayer(otherPlayers, hasturn)
    for _, otherPlayer in ipairs(otherPlayers) do
        if otherPlayer.playerid == hasturn then 
            highlightName(otherPlayer)
            return true
        end
    end
    return false
end

function drawInJail(player, homecolour)
    player[1].x = homecolour[1]-20
    player[1].y = homecolour[2]-20
    player[2].x = homecolour[1]+20
    player[2].y = homecolour[2]-20
    player[3].x = homecolour[1]-20
    player[3].y = homecolour[2]+20
    player[4].x = homecolour[1]+20
    player[4].y = homecolour[2]+20
    drawName(player.playerid,player.colour, homecolour)
    player.nametext = nametext
end

function createplayer(player)
    for i=1,4 do
       circle = display.newCircle(0,0,5)
       circle.out = false
       circle.auxlap = false
       circle.lap = false
       circle.colour = player.colour
        if player.colour == "red" then
            circle.pos = 13
            circle:setFillColor(unpack(red))
        elseif player.colour == "yellow" then 
            circle.pos = 37
            circle:setFillColor(unpack(yellow))
        elseif player.colour == "blue" then
            circle:setFillColor(unpack(blue))
            circle.pos = 61
        elseif player.colour == "green" then
            circle:setFillColor(unpack(green))
            circle.pos = 85
        end
        circle:setStrokeColor(unpack(gray))
        circle.strokeWidth = 1
        table.insert(player,circle)
    end
    comms.sendinfo(player, false)
end

createplayer(player)

local function paintTiles(pawn) 
    for i, cell in ipairs(pawn.validmoves) do
        globalboard[cell]:setFillColor(unpack(selectedTileColour))
    end
end

local function exitprison(player) --Salir de la prision

    player.out = true
    if not player.hasExitedBefore then 
        for i, pawn in ipairs(player) do
            pawn.out = true
            pawn.x = globalboard[pawn.pos].x
            pawn.y = globalboard[pawn.pos].y
        end
    else 
        reset = boardlib.resetPos(player)
        for i, pawn in ipairs(player) do
           if pawn.pos == reset then 
                pawn.out = true
                pawn.x = globalboard[pawn.pos].x
                pawn.y = globalboard[pawn.pos].y
           end 
        end
    end 

    player.hasExitedBefore = true
end


function tellHomeColour(player)
    if player.colour == "red" then
        homec = homeredpos 
    elseif player.colour == "blue" then
        homec = homebluepos 
    elseif player.colour == "green" then
        homec = homegreenpos
    elseif player.colour == "yellow" then
        homec = homeyellowpos
    end
    return homec
end

function restoreColourBoard(pawn) 
    if(pawn.validmoves ~= nil) then   

        for i, cell in ipairs(pawn.validmoves) do
            if table.indexOf(blackies, cell) == nil then
                colour = boardlib.tellColour(cell)
                if colour == "solidred" then
                    globalboard[cell]:setFillColor(unpack(red))
                elseif colour == "solidyellow" then
                    globalboard[cell]:setFillColor(unpack(yellow))
                elseif colour == "solidblue" then 
                    globalboard[cell]:setFillColor(unpack(blue))
                elseif colour == "solidgreen" then 
                    globalboard[cell]:setFillColor(unpack(green))
                elseif colour == "cyan" then 
                    globalboard[cell]:setFillColor(unpack(cyan))
                else 
                    globalboard[cell]:setFillColor(unpack(white))
                end 
            else 
                globalboard[cell]:setFillColor(unpack(gray))
            end

        end
    end
end

function restoreColourPlayer(player)
    for _, pawn in ipairs(player) do
        if player.colour == "red" then
            pawn:setFillColor(unpack(red))
        elseif player.colour == "yellow" then 
            pawn:setFillColor(unpack(yellow))
        elseif player.colour == "blue" then
            pawn:setFillColor(unpack(blue))
        elseif player.colour == "green" then
            pawn:setFillColor(unpack(green))
        end
    end
end

function playertap(event)
    if takePawn and player.out then 
        print("TAKEPAWN")
        restoreColourPlayer(player)
        pawnToTake = event.target
        event.target:setFillColor(unpack(selectedTileColour))
        event.target:toFront()
    elseif turn then
        for _,pawn in ipairs(player) do
            restoreColourBoard(pawn)
        end
        event.target.tapped = true
        if event.target.out and player.out then
            if player.rolled and not blockMessage and not (diea == 0 and dieb == 0) then
                print("--Roll info sent to server")
                possiblestr = '"possibleMoves": true,'
                pawnstr = '"pawn":' ..'"pawn' ..table.indexOf(player, event.target) .. '",'
                dicestr = '"dice":[' .. diea ..',' .. dieb.. ']'
                rollinfo = '{' .. possiblestr ..pawnstr .. dicestr .. '}'
                comms.sendMessage(rollinfo)
                blockMessage = true
                tappedpawn = event.target
            end
        end
    end
end 


function movehorizontal(player, tile)
    transition.moveTo(player, {x = tile.x, 500})
end

function removeDice()
    for _, diceobject in ipairs(dicePictures) do  
        diceobject.isVisible = false
        diceobject:removeSelf()
    end
    dicePictures = {}
end

function finishTurn(pawn)
    comms.sendinfo(player, true)
    diea = nil 
    dieb = nil
    turnText.alpha = 0
    turn = false 
    player.rolled = true
    rolldice:setEnabled(false)
    player.nametext:setTextColor(unpack(white))
    removeDice()

    print("-------------------------TURN FINISHES HERE-------------------------")
end


function tapListener(event)
    print(table.indexOf(globalboard, event.target))
    if turn then 
        pawn = tappedpawn
        if pawn ~= nil and pawn.tapped and pawn.validmoves ~= nil then 
            for _, cell in ipairs(pawn.validmoves) do 
                
                if globalboard[cell] == event.target then 
                    restoreColourBoard(pawn)
                    tile = globalboard[cell]
                    transition.moveTo(pawn, {y = tile.y, 500, transition=easing.inOutExpo, onComplete = movehorizontal(pawn, tile)})
                    pawn.pos = cell 
                    boardlib.enablelap(pawn)
                    pawn.tapped = false 
                    tappedpawn = nil 
                    
                    if pawn.validmoves[1] == cell and (diea ~= 0 and dieb ~= 0) and (diea ~= nil and dieb~=nil) then
                        if not equaldice then 
                            finishTurn(pawn)
                        else 
                            rolldice:setEnabled(true)
                            comms.sendinfo(player, false)
                        end
                        diea = 0
                        dieb = 0
                    else
                        if pawn.validmoves[2] == cell and diea ~= 0 then 
                            diea = 0
                        else 
                            dieb = 0
                        end 

                        if diea == dieb and diea == 0 then 
                            if not equaldice then
                                finishTurn(pawn)
                            else 
                                rolldice:setEnabled(true)
                                comms.sendinfo(player, false)
                                equaldice = false
                                throwdiceText.alpha = 1
                            end
                        else 
                            rolldice:setEnabled(false)
                            comms.sendinfo(player, false)
                            pawn.validmoves = nil
                            if cell == 97 then 
                                pawn:removeSelf()
                            end
                            return true
                        end
                    end
                    
                    if cell == 97 then 
                        pawn:removeSelf()
                    end
                    pawn.validmoves = nil
                    return true
                end

            end
        end 
    end
    return false
end



for i, pawn in ipairs(player) do
    pawn:addEventListener( "tap", playertap)
end

local function roll( event )
        
    if startroll then 
        if ( "ended" == event.phase ) then
            diea=math.random(1,6)
            dieb=math.random(1,6)
            rolleda = display.newImageRect(filename..diea..extension,50,50)
            rolleda.x, rolleda.y = 50, 50
            rolledb = display.newImageRect(filename..dieb..extension,50,50)
            rolledb.x, rolledb.y = 100, 50
            table.insert(dicePictures, rolleda)
            table.insert(dicePictures, rolledb)


            comms.sendMessage('{"startroll": '.. diea + dieb .. '}')
            startroll = false
            diea = nil
            dieb = nil
            rolldice:setEnabled(false)
        end
    elseif turn then
        
    
        if ( "ended" == event.phase ) then
            
            diea=math.random(1,6)
            dieb=math.random(1,6)
            rolleda = display.newImageRect(filename..diea..extension,50,50)
            rolleda.x, rolleda.y = 50, 50
            rolledb = display.newImageRect(filename..dieb..extension,50,50)
            rolledb.x, rolledb.y = 100, 50
            table.insert(dicePictures, rolleda)
            table.insert(dicePictures, rolledb)
            throwdiceText.alpha = 0
            if player.out then
                if (diea == dieb) and (diea ~= nil) then
                    equaldice = true
                    timesRolled = timesRolled + 1
                else 
                    timesRolled = 0
                    equaldice = false
                end
                player.rolled = true
                rolldice:setEnabled(false)
            else 
                if timesRolled == 2  and (diea ~= dieb)then 
                    turn = false
                    turnText.alpha = 0
                    rolldice:setEnabled(false) 
                    timesRolled = 0 
                    comms.sendinfo(player, true)
                    player.nametext:setTextColor(unpack(white))
                    removeDice()
                else 
                    timesRolled = timesRolled + 1
                end
            end
 
            if ((diea == dieb) and (diea ~= nil) and (timesRolled >= 3) and (player.out)) then 
                print("TAKETHEPAWNOUT")
                takePawn = true
                selectPawn.isVisible = true
                selectPawn:setEnabled(true)
                takealert = native.showAlert( "Felicidades", "Puedes elegir una de tus fichas para sacarla del juego.", { "Elegir ficha" }, closeAlert )
            end 
            if (diea == dieb and diea ~= nil and not player.out) then
                print("EXITPRISON")
                rolldice:setEnabled(true)
                timesRolled = 0
                exitprison(player)
            end
            print("TIMESROLLED: ", timesRolled)
        end
    end

end
 

function closeAlert( event )
    if ( event.action == "clicked" ) then
        local i = event.index
        if ( i == 1 ) then
            -- Do nothing; dialog will simply dismiss
        end
    end
end

local function sendStartGame(event)
    if ( "ended" == event.phase ) then
        comms.sendMessage('{"start": true}')
    end
end 



function takePawnOut(event)
    if ( "ended" == event.phase ) then
        if pawnToTake ~= nil then 
            takepawnindex = table.indexOf(player, pawnToTake)
            table.remove(player, takepawnindex)
            pawnToTake:removeSelf()
            takePawn = false
            pawnToTake = false
            selectPawn.isVisible = false
            selectPawn:setEnabled(false)
            comms.sendinfo(player, true)
        end
    end
end



-- Boton creado (Tipo de Widget)
rolldice = widget.newButton(
    {
        width = 130,
        height = 20,
        defaultFile = "rollbutton.png",
        id = "rolldice",
        label = "Lanzar dados",
        labelColor = { default={ 1, 1, 1, 1 }, over={ .2, .2, .2,.2} },
        onEvent = roll,
        isEnabled = true
    }
)

startbutton = widget.newButton(
    {
        width = 65,
        height = 45,
        defaultFile = "startgame.png",
        id = "startgame",
        labelColor = { default={ 1, 1, 1, 1 }, over={ .2, .2, .2,.2} },
        onEvent = sendStartGame,
        isEnabled = true
    }
)

selectPawn = widget.newButton(
    {
        width = 160,
        height = 25,
        defaultFile = "select.png",
        label = "Seleccionar ficha",
        id = "select",
        labelColor = { default={ 1, 1, 1, 1 }, over={ .2, .2, .2,.2} },
        onEvent = takePawnOut,
        isEnabled = false, 
    }
)


selectPawn.isVisible = false
rolldice.x = 83
rolldice.y = halfH *2 -15
startbutton.x = rolldice.x + 115
startbutton.y = rolldice.y
selectPawn.x = rolldice.x  + 150
selectPawn.y = rolldice.y 
testnum = 0





----------------

local function processInfo()
    data, incoming = comms.receiveInfo()
        if incoming then
            if data ~= nil then 
                message = json.decode(data)

                if not otherplayersinfo then
                    if message.newplayer ~=nil then
                        print("NEWPLAYER")
                        newPlayerid = message.playerid 
                        newPlayer = boardlib.drawOtherPlayers(message.colour)
                        newPlayer.playerid = newPlayerid
                        newPlayer.colour = message.colour
                        table.insert(otherPlayers, newPlayer)
                        otherhomecolour = tellHomeColour(newPlayer)
                        drawInJail(newPlayer, otherhomecolour)
                    elseif message.startgame then 
                        math.randomseed(message.randomnum)
                        removeDice()

                        print("START")
                        start = true 
                        otherplayersinfo = true 
                        startbutton.isVisible = false
                        startroll = true 
                        rolldice:setEnabled(true)
                        rollalert = native.showAlert( "Tire los dados", "Tire los dados para determinar que jugador empieza", { "Tirar los dados" }, closeAlert )
                    elseif message.waiting then 
                        alert = native.showAlert( "Esperando", "Seguimos esperando a más jugadores.", { "OK" }, closeAlert )
                    end
                    
                elseif start then 
                    if message.transition then 
                        otherPlayers = boardlib.transitionOtherPlayers(otherPlayers, message.playerspositions, globalboard)
                    elseif message.hasturn then
                        removeDice()
                        highlightOtherPlayer(otherPlayers, message.hasturn)
                        hasturnText.text = message.hasturn .. ' tiene el turno'
                        hasturnText.alpha = 1
                    elseif message.turngranted and message.playerid == player.playerid then 
                        resetNameHighlight(otherPlayers)
                        highlightName(player)
                        print(message.turngranted)
                        print("\n\n\n-------------------------TURN STARTS HERE-------------------------\n\n\n")
                        turn = true
                        hasturnText.alpha = 0
                        turnText.alpha = 1
                        throwdiceText.alpha = 1
                        rolldice:setEnabled(true)  
                    elseif message.validmoves then 
                        if tappedpawn ~= nil then 
                            tappedpawn.validmoves = message.validmoves
                            blockMessage = false
                            paintTiles(tappedpawn)
                        end
                    end
                    if message.jailedpawns ~= nil then 
                        if message.jailedpawns[player.playerid] ~= nil then 
                            player.out = false
                            print("GOT JAILED")
                            for _, jailedpos in ipairs(message.jailedpawns[player.playerid]) do
                                for z, pawn in ipairs(player) do 
                                    if pawn.pos == jailedpos then 
                                        pawn.out = false
                                        pawn.pos = boardlib.resetPos(player.colour)
                                        pawn.lap = false
                                        otherhome = tellHomeColour(player)
                                        pawn.x = otherhome[1]
                                        pawn.y = otherhome[2]
                                    end 
                                end
                            end 
                            
                        end
                        
                        for _, otherPlayer in ipairs(otherPlayers) do 
        
                            if message.jailedpawns[otherPlayer.playerid] ~= nil then 
                                for j, jailedpos in ipairs(message.jailedpawns[otherPlayer.playerid]) do
                                    for x, otherPawn in ipairs(otherPlayer) do 
                                        if otherPawn.pos == jailedpos then 
                                            otherPawn.pos = boardlib.resetPos(otherPlayer.colour)
                                            otherhome = tellHomeColour(otherPlayer)
                                            otherPawn.x = otherhome[1]
                                            otherPawn.y = otherhome[2]
                                        end 
                                    end
                                end
                            end
                        end

                    end
                end 
            end
        end

end

local s_loop = timer.performWithDelay(50, processInfo, -1)


--------------------------------------------------
function scene:create(event)

    local sceneGroup = self.view
    display.setDefault("background", unpack(bckgcolour))    
    skypos = boardlib.toScreen({0,-10},center)
    sky = display.newCircle(skypos[1], skypos[2],30)
    sky:setFillColor(unpack(cyan))
    
    homegenpos = {-99,92}
    homeredpos = homegenpos
    homeredpos = boardlib.toScreen(homeredpos, center)
    homered = display.newRect(homeredpos[1], homeredpos[2], 72, 78)
    homered.x = homeredpos[1]
    homered.y = homeredpos[2]

    homegreenpos = {homegenpos[1]*-1,homegenpos[2]}
    homegreenpos = boardlib.toScreen(homegreenpos, center)
    homegreen = display.newRect(homegreenpos[1], homegreenpos[2], 72, 78)
    homegreen.x = homegreenpos[1]
    homegreen.y = homegreenpos[2]

    homegenpos = {-99,-112}
    homeyellowpos = {homegenpos[1],homegenpos[2]}
    homeyellowpos = boardlib.toScreen(homeyellowpos, center)
    homeyellow = display.newRect(homeyellowpos[1], homeyellowpos[2], 72, 78)
    homeyellow.x = homeyellowpos[1]
    homeyellow.y = homeyellowpos[2]

    homebluepos = {homegenpos[1]*-1,homegenpos[2]}
    homebluepos = boardlib.toScreen(homebluepos, center)
    homeblue = display.newRect(homebluepos[1], homebluepos[2], 72, 78)
    homeblue.x = homebluepos[1]
    homeblue.y = homebluepos[2]

    


    homered:setFillColor(unpack(colourForHome))
    homeblue:setFillColor(unpack(colourForHome))
    homegreen:setFillColor(unpack(colourForHome))
    homeyellow:setFillColor(unpack(colourForHome))

    -- Se dibuja el tablero
    everything = display.newGroup()

    globalboard, blackies = boardlib.drawboard(everything, center)
    table.insert(globalboard, sky)
    for i, tile in ipairs(globalboard) do
        tile:addEventListener("tap", tapListener)
    end
    homecolour = tellHomeColour(player)
    drawInJail(player, homecolour)
   
    for i, pawn in ipairs(player) do
        pawn:toFront()
    end
    turnText = display.newText(sceneGroup, "Tu turno", display.contentCenterX, homeredpos[2] - 170, native.systemFont, 20 )
    hasturnText = display.newText(sceneGroup, " tiene el turno", display.contentCenterX, homeredpos[2] - 145, native.systemFont, 20 )
    throwdiceText = display.newText(sceneGroup, "Puedes lanzar los dados", display.contentCenterX, homeredpos[2] - 145, native.systemFont, 20 )

    turnText.alpha = 0 
    hasturnText.alpha = 0
    throwdiceText.alpha = 0
    sceneGroup:insert(everything)
    
end

function scene:show( event )
 
    local sceneGroup = self.view
    local phase = event.phase
 
    if ( phase == "will" ) then
        -- Code here runs when the scene is still off screen (but is about to come on screen)
 
    elseif ( phase == "did" ) then
        -- Code here runs when the scene is entirely on screen
 
    end
end
 
 
-- hide()
function scene:hide( event )
 
    local sceneGroup = self.view
    local phase = event.phase
 
    if ( phase == "will" ) then
        -- Code here runs when the scene is on screen (but is about to go off screen)
 
    elseif ( phase == "did" ) then
        -- Code here runs immediately after the scene goes entirely off screen
 
    end
end
 
 
-- destroy()
function scene:destroy( event )
 
    local sceneGroup = self.view
    -- Code here runs prior to the removal of scene's view
 
end
 
 
-- -----------------------------------------------------------------------------------
-- Scene event function listeners
-- -----------------------------------------------------------------------------------
scene:addEventListener( "create", scene )
scene:addEventListener( "show", scene )
scene:addEventListener( "hide", scene )
scene:addEventListener( "destroy", scene )

return scene