local composer = require( "composer" )
comms = require "communication"
json = require ("json")
playerid = ""
availablecolours = {}
otherPlayers = {}
serverAddress = ""


-- Hide status bar
display.setStatusBar( display.HiddenStatusBar )
 
-- Seed the random number generator
math.randomseed( os.time() )
 
-- Go to the menu screen
composer.gotoScene( "menu" )