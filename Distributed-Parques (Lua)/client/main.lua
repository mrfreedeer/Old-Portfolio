local composer = require( "composer" )
comms = require "communication"
json = require ("json")
playerid = ""
availablecolours = {}
otherPlayers = {}
serverAddress = ""
time = os.date('*t')



function normalizeRGB(R,G,B)
    return {R/255, G/255, B/255}
end
red = normalizeRGB(252, 65, 23)
yellow = normalizeRGB(241, 211, 2)
blue = normalizeRGB(33, 145, 251)
green = normalizeRGB(22, 219, 101)
selectedTileColour = normalizeRGB(105, 45, 115)
gray = {.2,.2,.2}
black = {0,0,0}
colourForHome = normalizeRGB(8, 61, 119)
white = {1, 1, 1}
cyan = {0,1,1}
bckgcolour = normalizeRGB(53, 96, 90)

-- Hide status bar
display.setStatusBar( display.HiddenStatusBar )
 
-- Seed the random number generator
math.randomseed( os.time() )
 
-- Go to the menu screen
composer.gotoScene( "menu" )


function returnToMenu( event )
    if ( event.action == "clicked" ) then
        local i = event.index
        if ( i == 1 ) then
            composer.removeScene("selectColour")
            composer.removeScene("game")
            composer.gotoScene ("menu")
        end
    end
end

function myUnhandledErrorListener( event )
 
    local iHandledTheError = true
 
    if iHandledTheError then
        errorstr = '\tLo sentimos, no nos podemos comunicar con el servidor.\n'
        errorstr = errorstr .. '\tEsto puede ser porque:\n'
        errorstr = errorstr .. '\t\t\t• El servidor no está activo\n'
        errorstr = errorstr .. '\t\t\t• La partida ya está llena\n'
        errorstr = errorstr .. '\t\t\t• La dirección ingresada es errónea'

        
        erroralert = native.showAlert( "Error", errorstr, { "OK" }, returnToMenu )

        print( "Unable to connect to server", event.errorMessage )
    else
        print( "Not handling the unhandled error", event.errorMessage )
    end
    
    return iHandledTheError
end
 
Runtime:addEventListener("unhandledError", myUnhandledErrorListener)