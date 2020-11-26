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
			circle:setFillColor(unpack(red))
		elseif circlecolour == "yellow" then 
			circle.pos = 37
			circle:setFillColor(unpack(yellow))
		elseif circlecolour == "blue" then
			circle:setFillColor(unpack(blue))
			circle.pos = 61
		elseif circlecolour == "green" then
			circle:setFillColor(unpack(green))
			circle.pos = 85
		end
		circle:setStrokeColor(unpack(gray))
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
			if positions ~= nil then
				for i, pawn in ipairs(player) do 
					pawnpos = positions[pawnstring..i]
					if pawnpos ~= nil then
						if pawnpos ~= 97 then
							tile = globalboard[pawnpos]
							transition.moveTo(pawn, {y = tile.y, 500, transition=easing.inOutExpo, onComplete = movehorizontal(pawn, tile)})
							pawn.pos = pawnpos
						else 
							pawnindex = table.indexOf(player, pawn)
							if pawnindex ~= nil then
								table.remove(player, pawnindex)
								pawn:removeSelf()
							end
						end
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

function board.enablelap(pawn) 
	if pawn.colour == "red" then
		if pawn.pos>20 and not pawn.lap then
			pawn.lap = true
		end
	elseif pawn.colour == "yellow" then
		if pawn.pos>44 and not pawn.lap then
			pawn.lap = true
		end
	elseif pawn.colour == "blue" then
		if pawn.pos>68 and not pawn.lap then
			pawn.lap = true
		end
	elseif pawn.colour == "green" then
		if pawn.pos>92 and not pawn.lap then
			pawn.lap = true
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



function board.drawboard(displaygroup, center )
		global =  {}
		posx = 0 
		posy = 125
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
				f:setStrokeColor( unpack(red))
				f:setFillColor(unpack(gray))
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(unpack(white))
				f:setFillColor(unpack(red))
			end
			table.insert(global, f)
			
			posy = posy + diff
		
		end
		posy = 125
		posx = posx-42
		for i=1, 10 do
			screenpos = board.toScreen({posx, posy}, center)
			local f = display.newRect(displaygroup,screenpos[1], screenpos[2], 40,10)
			f.strokeWidth = 1
			f.number = num
			num = num + 1
			if i == 5 then
				f:setStrokeColor( unpack(red))
				f:setFillColor(unpack(gray))
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(unpack(red))
				f:setFillColor(unpack(white))
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
				f:setStrokeColor( unpack(red))
				f:setFillColor(unpack(gray))
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(unpack(red))
				f:setFillColor(unpack(white))
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
				f:setStrokeColor(unpack(black))
				f:setFillColor(unpack(gray))
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(unpack(black))
				f:setFillColor(unpack(yellow))
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
				f:setStrokeColor(unpack(yellow))
				f:setFillColor(unpack(gray))
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(unpack(yellow))
				f:setFillColor(unpack(white))
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
				f:setStrokeColor(unpack(yellow))
				f:setFillColor(unpack(gray))
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(unpack(yellow))
				f:setFillColor(unpack(white))
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
				f:setStrokeColor(unpack(black))
				f:setFillColor(unpack(gray))
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(unpack(white))
				f:setFillColor(unpack(blue))
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
				f:setStrokeColor(unpack(blue))
				f:setFillColor(unpack(gray))
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(unpack(blue))
				f:setFillColor(unpack(white))
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
				f:setStrokeColor(unpack(black))
				f:setFillColor(unpack(gray))
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(unpack(blue))
				f:setFillColor(unpack(white))
			end
			table.insert(global, f)
			posx = posx - diff
		end
		bluelimit = num - 1
		--Aqui empiezan las verdes
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
				f:setStrokeColor(unpack(black))
				f:setFillColor(unpack(gray))
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(unpack(black))
				f:setFillColor(unpack(green))
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
				f:setStrokeColor(unpack(black))
				f:setFillColor(unpack(gray))
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(unpack(green))
				f:setFillColor(unpack(white))
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
				f:setStrokeColor(unpack(black))
				f:setFillColor(unpack(gray))
				table.insert(blackies, num -1)
			else
				f:setStrokeColor(unpack(green))
				f:setFillColor(unpack(white))
			end
			table.insert(global, f)
			posy = posy - diff
		end
		greenlimit = num - 1

		return global, blackies
end


return board