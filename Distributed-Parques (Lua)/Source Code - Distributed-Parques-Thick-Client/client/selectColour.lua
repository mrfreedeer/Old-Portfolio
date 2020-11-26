-- selectColour

local composer = require( "composer" )
 
local scene = composer.newScene()
chosencolour = ""
-- -----------------------------------------------------------------------------------
-- Code outside of the scene event functions below will only be executed ONCE unless
-- the scene is removed entirely (not recycled) via "composer.removeScene()"
-- -----------------------------------------------------------------------------------
 
 local function redChosen()
    chosencolour = "red"
    comms.sendMessage(chosencolour)
    composer.gotoScene("game")
 end
 
 local function blueChosen()
    chosencolour = "blue"
    comms.sendMessage(chosencolour)
    composer.gotoScene("game")
 end

 local function greenChosen()
    chosencolour = "green"
    comms.sendMessage(chosencolour)
    composer.gotoScene("game")
 end

 local function yellowChosen()
    chosencolour = "yellow"
    comms.sendMessage(chosencolour)
    composer.gotoScene("game")
 end
 
-- -----------------------------------------------------------------------------------
-- Scene event functions
-- -----------------------------------------------------------------------------------
 
-- create()
function scene:create( event )
 
    local sceneGroup = self.view
    -- Code here runs when the scene is first created but has not yet appeared on screen
    local sceneGroup = self.view
    local background = display.newImageRect(sceneGroup, "menubckg.jpg", 800, 1400)
    background.x = display.contentCenterX
    background.y = display.contentCenterY

    local choosetext = display.newText(sceneGroup, "Seleccione un color:", display.contentCenterX, display.contentCenterY - 80, native.systemFont, 20 )
    texty = display.contentCenterY - 50
    if table.indexOf(availableColours, "red") ~= nil then
        local redtext = display.newText(sceneGroup, "Rojo", display.contentCenterX, texty, native.systemFont, 20)    
        texty = texty + 30
        redtext:addEventListener("tap", redChosen)
    end
    if table.indexOf(availableColours, "blue") ~= nil then
        local bluetext = display.newText(sceneGroup, "Azul", display.contentCenterX, texty, native.systemFont, 20)    
        texty = texty + 30
        bluetext:addEventListener("tap", blueChosen)
    end
    if table.indexOf(availableColours, "green") ~= nil then
        local greentext = display.newText(sceneGroup, "Verde", display.contentCenterX, texty, native.systemFont, 20)    
        texty = texty + 30
        greentext:addEventListener("tap", greenChosen)
    end
    if table.indexOf(availableColours, "yellow") ~= nil then
        local yellowtest = display.newText(sceneGroup, "Amarillo", display.contentCenterX, texty, native.systemFont, 20)    
        texty = texty + 30
        yellowtest:addEventListener("tap", yellowChosen)
    end
end
 
 
-- show()
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
-- -----------------------------------------------------------------------------------
 
return scene