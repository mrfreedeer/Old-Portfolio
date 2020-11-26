--menu.lua

local composer = require("composer")
local scene = composer.newScene()
local gotColours = false
local gotId = false
local startup = {}

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
    print("---startup", data)
    if incoming then
        if data ~= nil then 
            message = json.decode(data)
            if not gotColours then
                comms.sendMessage("false")
                if message.colours ~= nil then 
                    gotColours = true
                    print("Avaialable colours")
                    availableColours = message.colours:split(",")
                    for _, i in ipairs(availableColours) do
                        print(i)
                    end

                    comms.sendMessage("true")
                end
            elseif not gotId then 
                if message.playerid ~= nil then 
                    playerid = message.playerid
                    gotId = true
                end 
            end
        end
    end
    if gotId and gotColours then
        timer.cancel(startup)
        gotoGame()
    end
end

local function inputListener( event )
 
    if ( event.phase == "began" ) then
        -- User begins editing "defaultField"
 
    elseif ( event.phase == "ended" or event.phase == "submitted" ) then
        -- Output resulting text from "defaultField"
        serverAddress = event.target.text
        print( event.target.text )
        if comms.connect(serverAddress) then
          startup = timer.performWithDelay(50, getStartupInfo, 0)
          event.target:removeSelf()
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

    local serverText = display.newText(sceneGroup, "Ingresar dirección del servidor", display.contentCenterX, display.contentCenterY - 50, native.systemFont, 20 )
    local serverField = native.newTextField(display.contentCenterX, display.contentCenterY, 180, 30)
    sceneGroup:insert(serverField)
    
    serverField: addEventListener("userInput", inputListener)
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