--menu.lua

local composer = require("composer")
local scene = composer.newScene()
local gotColours = false
local startup = {}
nameField = {}
nameText = {}
serverField = {}
serverText = {}
local function gotoGame()
    
    composer.removeScene("menu")
    composer.gotoScene("selectColour")
end


function string:split( inSplitPattern )
 
    local outResults = {}
    local theStart = 1
    local theSplitStart, theSplitEnd = string.find( self, inSplitPattern, theStart )
 
    while theSplitStart do
        table.insert( outResults, string.sub( self, theStart, theSplitStart-1 ) )
        theStart = theSplitEnd + 1
        theSplitStart, theSplitEnd = string.find( self, inSplitPattern, theStart )
    end
 
    table.insert( outResults, string.sub( self, theStart ) )
    return outResults
end

local function getStartupInfo()
    local data, incoming = comms.receiveInfo()
    if incoming then
        if data ~= nil then 
            message = json.decode(data)
            if not gotColours then
                comms.sendMessage("false")

                if message.hours ~= nil then 
                    print("--Server adjustement: ", message.hours, message.minutes, message.seconds)
                    print("--Local time before: ", time.hour, time.min, time.sec)
                    time.hour = time.hour + message.hours 
                    time.min = time.min + message.minutes
                    time.sec = time.sec + message.seconds
                    print("--Local time: ", time.hour, time.min, time.sec)
                end

                if message.colours ~= nil then 
                    gotColours = true
                    comms.sendMessage("true")
                    print("Avaialable colours")
                    availableColours = message.colours:split(",")
                    for _, i in ipairs(availableColours) do
                        print(i)
                    end

                    
                end
            end
        end
    end
    if  gotColours then
        timer.cancel(startup)
        gotoGame()
    end
end

local function serverInputListener( event )
 
    if ( event.phase == "began" ) then
        -- User begins editing "defaultField"
 
    elseif ( event.phase == "ended" or event.phase == "submitted" ) then
        -- Output resulting text from "defaultField"
        serverAddress = event.target.text
        print( event.target.text )
        if comms.connect(serverAddress) then
          startup = timer.performWithDelay(50, getStartupInfo, 0)
          event.target:removeSelf()
          comms.sendTime()
        end

 
    elseif ( event.phase == "editing" ) then
        print( event.newCharacters )
        print( event.oldText )
        print( event.startPosition )
        print( event.text )
    end
end
local function closeAlert( event )
    if ( event.action == "clicked" ) then
        local i = event.index
        if ( i == 1 ) then
            -- Do nothing; dialog will simply dismiss
        end
    end
end

local function nameInputListener( event )
 
    if ( event.phase == "began" ) then
        -- User begins editing "defaultField"
 
    elseif ( event.phase == "ended" or event.phase == "submitted" ) then
        -- Output resulting text from "defaultField"
        playerid = event.target.text
        if playerid == '' then 
            alert = native.showAlert( "Nombre vacio", "El nombre no puede estar vacio", { "Aceptar" }, closeAlert )
        else 
            print( event.target.text )
            nameText.alpha = 0
            serverText.alpha = 1
            nameField.isVisible = false
            serverField.isVisible = true 
        end
    elseif ( event.phase == "editing" ) then
        print( event.newCharacters )
        print( event.oldText )
        print( event.startPosition )
        print( event.text )
    end
end


function scene:create(event)
    local sceneGroup = self.view
    local background = display.newImageRect(sceneGroup, "menubckg.jpg", 800, 1400)
    background.x = display.contentCenterX
    background.y = display.contentCenterY

    serverText = display.newText(sceneGroup, "Ingresar dirección del servidor", display.contentCenterX, display.contentCenterY - 50, native.systemFont, 20 )
    nameText = display.newText(sceneGroup, "Ingrese su nombre", display.contentCenterX, display.contentCenterY - 50, native.systemFont, 20 )
    serverField = native.newTextField(display.contentCenterX, display.contentCenterY, 180, 30)
    nameField = native.newTextField(display.contentCenterX, display.contentCenterY, 180, 30)
    sceneGroup:insert(serverField)
    sceneGroup:insert(nameField)
    
    serverField: addEventListener("userInput", serverInputListener)
    nameField: addEventListener("userInput", nameInputListener)
    serverText.alpha = 0
  
   serverField.isVisible = false
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