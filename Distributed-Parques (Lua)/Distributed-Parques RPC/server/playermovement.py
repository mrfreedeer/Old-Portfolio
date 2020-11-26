def check(position, currentposition, landscapes):
    firststatement = landscapes[0][0] <= position <=landscapes[0][1]
    secondstatement = landscapes[1][0] <= position <= landscapes[1][1]
    thirdstatement = landscapes[2][0] <= position <= landscapes[2][1]
    
    if landscapes[0][0] != 2:
        fourthstatement = currentposition<=landscapes[0][0]+6 and firststatement
    else:
        fourthstatement = (86<=currentposition<=96 or currentposition == 1) and firststatement

    fifthstatement = currentposition <= landscapes[1][0]+6 and secondstatement
    sixthstatement = currentposition <= landscapes[2][0]+6 and thirdstatement
    if fourthstatement or fifthstatement or sixthstatement:
        return True 
    return False

def checkValidMoves(position, currentposition, colour, lap):
    homepositions =[[10,20], [34,44], [58,68], [82,92]]
    landscapes = []

    if colour == "red":
        landscapes =[[26,37],[50,61],[74,85]]
        home = homepositions[0]
    elif colour == "yellow":
        landscapes = [[2,13], [50,61], [74,85]]
        home = homepositions[1]
    elif colour == "blue":
        landscapes = [[2,13],[26,37],[74,85]]
        home = homepositions[2]
    elif colour == "green":
        landscapes = [[2,13],[26,37],[50,61]]
        home = homepositions[3]

    if check(position, currentposition, landscapes):
        return position + 7
    elif (home[0] <= position <=home[1]) and lap:
        return position - 8
    elif position == home[0] -1 and lap:
        return 97 
    else:
        return position

def validateBoardlimit(position):
    if position > 96:
        return position - 96
    return position

def possibleMoves(pawn, diea, dieb):
    total = diea + dieb + pawn["position"]
    total = validateBoardlimit(total)
    validiea = validateBoardlimit(diea + pawn["position"])
    validieb = validateBoardlimit(dieb + pawn["position"])

    validtotal = checkValidMoves(total, pawn["position"] ,pawn["colour"], pawn["lap"])
    validiea = checkValidMoves(validiea, pawn["position"] ,pawn["colour"], pawn["lap"])
    validieb = checkValidMoves(validieb, pawn["position"] ,pawn["colour"], pawn["lap"])

    validmoves = [validtotal, validiea, validieb]

    if pawn["position"] in validmoves:
        validmoves.remove(pawn["position"])

    validmovestring = '{"validmoves": ['
    print 'Validmoves:'
    for x in validmoves:
        print x
        validmovestring += str(x) +','
    print '----ValidMoves----'
    
    if validmovestring[-1:] == ',':
        validmovestring = validmovestring[:-1]
    validmovestring += ']'

    validmovestring += '}\n' 
    return validmovestring

def createTransitionString(player,playerid):
    transtring = '"transition":true, "playerspositions": {"'
    transtring += playerid + '":{'

    for pawn, pawninfo in player.iteritems():
        if pawn not in ['out','endturn', 'updateposition']:
            transtring += '"' + str(pawn)+'":' + str(pawninfo["position"]) +','
    
    if transtring[-1:] == ',':
        transtring = transtring[:-1]

    transtring += '}}'
    
    return transtring
        