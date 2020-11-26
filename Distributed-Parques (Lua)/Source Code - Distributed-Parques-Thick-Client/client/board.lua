local board = {}

function board.resetPos(playercolour) 
	if playercolour == "red" then
		pos = 13
	elseif playercolour == "yellow" then 
		pos = 37
	elseif playercolour == "blue" then
		pos = 61
	elseif playercolour == "green" then
		pos = 85
	end
	return pos
end 
function board.drawOtherPlayers(playercolour)

	playerset = {}
	for i=1, 4 do
		circle = display.newCircle(0,0,5)
		circlecolour = playercolour
		if circlecolour == "red" then
			circle.pos = 13
			circle:setFillColor(1,0,0)
		elseif circlecolour == "yellow" then 
			circle.pos = 37
			circle:setFillColor(1,1,0)
		elseif circlecolour == "blue" then
			circle:setFillColor(0,0,1)
			circle.pos = 61
		elseif circlecolour == "green" then
			circle:setFillColor(0,1,0)
			circle.pos = 85
		end
		circle:setStrokeColor(.2,.2,.2)
		circle.strokeWidth = 1
		table.insert(playerset, circle)
		playerset.colour = circlecolour
	end
	

	return playerset
end 

function movehorizontal(player, tile)
    transition.moveTo(player, {x = tile.x, 500})
end

function board.transitionOtherPlayers(otherPlayers, playerspositions, globalboard)
	local positions = {}
	local playerstring = "player"
	local pawnstring = "pawn"
	for _, player in ipairs(otherPlayers) do
			positions = playerspositions[player.playerid]
			for i, pawn in ipairs(player) do 
				pawnpos = positions[pawnstring..i]
				if pawnpos ~= nil then
					if pawnpos ~= 97 then
						tile = globalboard[pawnpos]
						transition.moveTo(pawn, {y = tile.y, 500, transition=easing.inOutExpo, onComplete = movehorizontal(pawn, tile)})
						pawn.pos = pawnpos
					else 
						pawnindex = table.indexOf(player, pawn)
						table.remove(player, pawnindex)
						pawn:removeSelf()
					end
				end
		end
	end
	return otherPlayers
end

function board.toScreen(coords, center)
	ny = center[2] - coords[2]
	nx = (coords[1] + center[1])
	return {nx, ny}
end

function board.toCart(coords, center)
	cx = coords[1] - center[1]
	cy = center[2] - coords[2]
	return {cx,cy}
end

function board.enablelap(player) 
	if player.colour == "red" then
		if player.pos>20 and not player.lap then
			player.lap = true
		end
	elseif player.colour == "yellow" then
		if player.pos>44 and not player.lap then
			player.lap = true
		end
	elseif player.colour == "blue" then
		if player.pos>68 and not player.lap then
			player.lap = true
		end
	elseif player.colour == "yellow" then
		if player.pos>92 and not player.lap then
			player.lap = true
		end
	end
end

function board.tellColour(pos)

	if pos>=1 and pos<= 8 then
		return "solidred"
	elseif pos>=25 and pos<=32 then
		return "solidyellow"
	elseif pos>=49 and pos<=56 then 
		return "solidblue"
	elseif pos>=73 and pos<=80 then
		return "solidgreen"
	elseif pos == 97 then 
		return "cyan"
	else 
		return "white"
	end
end

function compareTwo(number, inferior, superior) 
	if number >= inferior then 
		if number <= superior then
			return true
		end 
	end 
	return false
end

function board.transPlayable(pos, colour, lapenabled, actualpos)
	if colour == "red" then
		if (pos>=26 and pos <=37) or (pos>=50 and pos <=61) or (pos>= 74 and pos <= 85)	then
			if(actualpos<=32 and compareTwo(pos,26,37)) or (actualpos <= 56 and compareTwo(pos,50,61)) or (actualpos<=74 and compareTwo(pos,74,85)) then
				return pos + 7
			end 
		elseif pos>=10 and pos <=20 and lapenabled then
			return pos - 8
		elseif pos==9 and lapenabled then
			return 97
		else
			return pos
		end
	end	
	if colour == "yellow" then
		if (pos>1 and pos <=13) or (pos>=50 and pos <=61) or (pos>= 74 and pos <= 85)	then
			if(actualpos<=96 and compareTwo(pos,1,13)) or (actualpos <= 56 and compareTwo(pos,50,61)) or (actualpos<=74 and compareTwo(pos,74,85)) then
				return pos + 7
			end 
		elseif pos>=34 and pos <=44 and lapenabled then
			return pos - 32
		elseif pos==33 and lapenabled then
			return 97
		else
			return pos
		end
	end	
	if colour == "blue" then
		if (pos>=26 and pos <=37) or (pos>1 and pos <=13) or (pos>= 74 and pos <= 85)	then
			if(actualpos<=32 and compareTwo(pos,26,37)) or (actualpos <= 96 and compareTwo(pos,1,13)) or (actualpos<=74 and compareTwo(pos,74,85)) then
				return pos + 7
			end 
		elseif pos>=58 and pos <=68 and lapenabled then
			return pos - 56
		elseif pos==57 and lapenabled then
			return 97
		else
			return pos
		end
	end	
	if colour == "green" then
		if (pos>=26 and pos <=37) or (pos>=50 and pos <=61) or (pos> 1 and pos <= 13)	then
			if(actualpos<=32 and compareTwo(pos,26,37)) or (actualpos <= 56 and compareTwo(pos,50,61)) or (actualpos<=96 and compareTwo(pos,1,13)) then
				return pos + 7
			end 
		elseif pos>=82 and pos <=92 and lapenabled then
			return pos - 80
		elseif pos==81 and lapenabled then
			return 97
		else
			return pos
		end
	end	
	return pos
end

function board.drawboard(displaygroup, center )
		global =  {}
		posx = 0 
		posy = 65
		diff = -12
		num = 1
		blackies = {}
		for i=1, 8 do
			screenpos = board.toScreen({posx, posy}, center)
			local f = display.newRect(displaygroup,screenpos[1], screenpos[2], 40,10)
			f.strokeWidth = 1
			f.number = num
			num = num + 1
			if i == 1 then
				f:setStrokeColor( 1, 0, 0)
				f:setFillColor(.2,.2,.2)
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(1,1,1)
				f:setFillColor(1,0,0)
			end
			table.insert(global, f)
			
			posy = posy + diff
		
		end
		posy = 65
		posx = posx-42
		for i=1, 10 do
			screenpos = board.toScreen({posx, posy}, center)
			local f = display.newRect(displaygroup,screenpos[1], screenpos[2], 40,10)
			f.strokeWidth = 1
			f.number = num
			num = num + 1
			if i == 5 then
				f:setStrokeColor( 1, 0, 0)
				f:setFillColor(.2,.2,.2)
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(1,0,0)
				f:setFillColor(1,1,1)
			end
			table.insert(global, f)
			posy = posy + diff
		
		end
		posx = posx - 27
		posy = posy + 27
		for i=1, 6 do
			screenpos = board.toScreen({posx, posy}, center)
			local f = display.newRect(displaygroup,screenpos[1], screenpos[2], 10,40)
			f.strokeWidth = 1
			f.number = num
			num = num + 1
			if i == 2 then
				f:setStrokeColor( 1, 0, 0)
				f:setFillColor(.2,.2,.2)
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(1,0,0)
				f:setFillColor(1,1,1)
			end
			table.insert(global, f)
			posx = posx + diff
		end
		redlimit = num - 1
		-- Aqui comienzan las fichas amarillas
		posy = posy - 42
		posx = posx  - diff
		refx = posx
		for i=1, 8 do
			screenpos = board.toScreen({posx, posy}, center)
			local f = display.newRect(displaygroup,screenpos[1], screenpos[2], 10,40)
			f.strokeWidth = 1
			f.number = num
			num = num + 1
			if i == 1 then
				f:setStrokeColor( 0, 0, 0)
				f:setFillColor(.2,.2,.2)
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(0,0,0)
				f:setFillColor(1,1,0)
			end
			table.insert(global, f)
			posx = posx - diff
		end
		
		posx = refx
		posy = posy - 42

		for i=1, 6 do
			screenpos = board.toScreen({posx, posy}, center)
			local f = display.newRect(displaygroup,screenpos[1], screenpos[2], 10,40)
			f.strokeWidth = 1
			f.number = num
			num = num + 1
			if i == 5 then
				f:setStrokeColor( 1, 1, 0)
				f:setFillColor(.2,.2,.2)
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(1,1,0)
				f:setFillColor(1,1,1)
			end
			
			table.insert(global, f)
			posx = posx - diff
		end
		posx =-42
		posy = posy + 15
		for i=1, 10 do
			screenpos = board.toScreen({posx, posy}, center)
			local f = display.newRect(displaygroup,screenpos[1], screenpos[2], 40,10)
			f.strokeWidth = 1
			f.number = num
			num = num + 1
			if i == 6 then
				f:setStrokeColor( 1, 1, 0)
				f:setFillColor(.2,.2,.2)
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(1,1,0)
				f:setFillColor(1,1,1)
			end
			table.insert(global, f)
			posy = posy + diff
		end
		yellowlimit = num - 1
		--Aqui comienzan las azules

		refy = posy
		posy = posy - diff
		posx = posx + 42
		for i=1, 8 do
			screenpos = board.toScreen({posx, posy}, center)
			local f = display.newRect(displaygroup,screenpos[1], screenpos[2], 40,10)
			f.strokeWidth = 1
			f.number = num
			num = num + 1
			if i == 1 then
				f:setStrokeColor(0,0,0)
				f:setFillColor(.2,.2,.2)
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(1,1,1)
				f:setFillColor(0,0,1)
			end
			table.insert(global, f)
			posy = posy - diff
		end
		posy = refy - diff
		posx = posx + 42
		for i=1, 10 do
			screenpos = board.toScreen({posx, posy}, center)
			local f = display.newRect(displaygroup,screenpos[1], screenpos[2], 40,10)
			f.strokeWidth = 1
			f.number = num
			num = num + 1
			if i == 5 then
				f:setStrokeColor(0,0,1)
				f:setFillColor(.2,.2,.2)
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(0,0,1)
				f:setFillColor(1,1,1)
			end
			table.insert(global, f)
			posy = posy - diff
		end
		posy = posy - 27
		posx = posx + 27
		for i=1, 6 do
			screenpos = board.toScreen({posx, posy}, center)
			local f = display.newRect(displaygroup,screenpos[1], screenpos[2], 10,40)
			f.strokeWidth = 1
			f.number = num
			num = num + 1
			if i == 2 then
				f:setStrokeColor(0,0,0)
				f:setFillColor(.2,.2,.2)
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(0,0,1)
				f:setFillColor(1,1,1)
			end
			table.insert(global, f)
			posx = posx - diff
		end
		bluelimit = num - 1
		--Aqui empiezan las verdes
		--print("Green", bluelimit)
		posx = posx + diff
		refx = posx 
		posy = posy + 42
		for i=1, 8 do
			screenpos = board.toScreen({posx, posy}, center)
			local f = display.newRect(displaygroup,screenpos[1], screenpos[2], 10,40)
			f.strokeWidth = 1
			f.number = num
			num = num + 1
			if i == 1 then
				f:setStrokeColor(0,0,0)
				f:setFillColor(.2,.2,.2)
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(0,0,0)
				f:setFillColor(0,1,0)
			end
			table.insert(global, f)
			posx = posx + diff
		end
		temprefx = posx
		posx = refx
		refx = temprefx
		posy = posy + 42
		for i=1, 6 do
			screenpos = board.toScreen({posx, posy}, center)
			local f = display.newRect(displaygroup,screenpos[1], screenpos[2], 10,40)
			f.strokeWidth = 1
			f.number = num
			num = num + 1
			if i == 5 then
				f:setStrokeColor(0,0,0)
				f:setFillColor(.2,.2,.2)
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(0,1,0)
				f:setFillColor(1,1,1)
			end
			table.insert(global, f)
			posx = posx + diff
		end
		posx = refx + 9
		posy = posy - 15
		
		for i=1, 10 do
			screenpos = board.toScreen({posx, posy}, center)
			local f = display.newRect(displaygroup,screenpos[1], screenpos[2], 40,10)
			f.strokeWidth = 1
			f.number = num
			num = num + 1
			if i == 6 then
				f:setStrokeColor(0,0,0)
				f:setFillColor(.2,.2,.2)
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(0,1,0)
				f:setFillColor(1,1,1)
			end
			table.insert(global, f)
			posy = posy - diff
		end
		greenlimit = num - 1
		return global, blackies
end


return board