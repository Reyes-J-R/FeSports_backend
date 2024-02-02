from django.shortcuts import render
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import TestModel
from .serializers import TestSerializer, UserSerializer, EventSerializer, GameSerializer, MatchSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import User, Event, Game, Match
from django.shortcuts import get_object_or_404
import random
# Create your views here.

bgmi_fields = ["kills", "deaths", "wins"]


@api_view(['GET'])
def test(request, pk):
    # event = Event.objects.get(id=pk)
    # players = [player for player in event.eventplayers.all()]
    # 
    # if event.event_type == "knockout":
    #     ko_bracket = {}
    #     for _ in range(int(len(players) / 2)):
    #         player1 = random.choice(players)
    #         players.remove(player1)
    #         player2 = random.choice(players)
    #         players.remove(player2)
    #         match = Match.objects.create(player1=player1, player2=player2, matchgame=event.eventgame, matchstate="pending")
    #         event.matches.add(match)
    #         
    #         match.save()
    #     event.save()
    #     serializer = EventSerializer(event)
    #     return Response({"event": serializer.data})
    pass
    


@api_view(['DELETE'])
def delete_items(request, pk):
    try:
        item = TestModel.objects.get(pk=pk)
        item.delete()
        return Response({"result": "success!"})
    except TestModel.DoesNotExist:
        return Response({"result: error"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response({"error":serializer.errors} )

@api_view(["GET"])
def show_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])
    if not user.check_password(request.data['password']):
         return Response({"detail": "wrong password provided"}, status=status.HTTP_401_UNAUTHORIZED )
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})

@api_view(["POST"])
def token(request):
    
    user = get_object_or_404(Token, key=request.data['token'])
    serializer = UserSerializer(instance=user.user)
    return Response({
         "user": serializer.data
    }, status=status.HTTP_200_OK) 

@api_view(["POST"])
def events(request):
    if 'event_state' in request.data.keys() and request.data['event_state'] in ("active", "pending", "ended"):
        try:
            events = Event.objects.filter(event_state=request.data['event_state'])
        except Exception as e:
            print(e)
            return Response({"event": []})
    else:
        events = Event.objects.all()
    print(events)
    events = [EventSerializer(event).data for event in events]
    for index, event in enumerate(events):
        events[index]['eventgame'] = GameSerializer(Game.objects.get(id=event['eventgame'])).data
    return Response({"event": events})

@api_view(["POST"])
def get_event(request, pk):

    event = get_object_or_404(Event, id=pk)
    game = event.eventgame
    match = event.matches.all()
    players = [UserSerializer(player).data for player in event.eventplayers.all()]
    matches = [MatchSerializer(match).data for match in event.matches.all()]
    
    
    serializer1 = EventSerializer(event)
    serializer2 = GameSerializer(game)
    return Response({"event": serializer1.data, "game": serializer2.data, "players": players, "matches": matches})

@api_view(["POST"])
def join_event(request, pk):
    user = request.data['user']
    
    event = Event.objects.get(id=pk)
    if event.eventplayers.filter(id=int(user['id'])).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    event.eventplayers.add(user['id'])
    getuser = User.objects.get(id=user['id'])
    getuser.joined_events.add(event.id)
    event.save()
    getuser.save()
    return Response(status=status.HTTP_200_OK)

@api_view(["POST"])
def leave_event(request, pk):
    user = request.data['user']
    event = Event.objects.get(id=pk)
    if not event.eventplayers.filter(id=int(user['id'])).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    event.eventplayers.remove(user['id'])
    getuser = User.objects.get(id=user['id'])
    getuser.joined_events.remove(event.id)
    event.save()
    getuser.save()
    return Response(status=status.HTTP_200_OK)

@api_view(["POST"])
def start_event(request, pk):
    event = Event.objects.get(id=pk)
    players = [player for player in event.eventplayers.all()]
    
    if event.event_state == "started":
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if event.event_type == "knockout":
        root = 1
        for _ in range(int(len(players) / 2)):
            player1 = random.choice(players)
            players.remove(player1)
            player2 = random.choice(players)
            players.remove(player2)
            match = Match.objects.create(player1=player1, player2=player2, matchgame=event.eventgame, matchstate="active", round=1, root=root)
            event.matches.add(match)
            
            match.save()
            root += 1
        event.event_state = "started"
        event.save()
        serializer = EventSerializer(event)
        return Response({"event": serializer.data})
    elif event.event_type == "league":
        for _ in range(int(len(players) // 2)):
            player1 = random.choice(players)
            players.remove(player1)
            player2 = random.choice(players)
            players.remove(player2)
            match = Match.objects.create(player1=player1, player2=player2, matchgame=event.eventgame, matchstate="active")
            event.matches.add(match)
            
        # if len(players) > 0:
        #     biematch = Match.objects.create(player1=players[0], matchgame=event.eventgame, matchstate="pending")
        #     event.matches.add(biematch)
        event.event_state = "started"
        event.save()
        return Response(status=status.HTTP_200_OK)

@api_view(["POST"])
def submit_match_result(request, pk):
    event = Event.objects.get(id=pk)
    match = Match.objects.get(id=request.data['match'])
    if event.event_type == "knockout":
            
        def match_range(round, root):
                range_len = 2**(round)
                if root % range_len != 0:
                    range_end = ((root // range_len) + 1) * range_len
                else:
                    range_end = (root // range_len) * range_len
                range_start = (range_end - range_len) + 1
                return range(range_start, range_end + 1)
        winner = User.objects.get(username=request.data['winner'])
        winner.matches_won.add(match)
        match.matchwinner = winner
        match.matchstate = "ended"
        match.player1stats = request.data['p1stats']
        match.player2stats = request.data['p2stats']
        root = match.root
        matchgame = match.matchgame
        round = match.round
        match.save()
        winner.save()
        matches = event.matches.all()
        matchrange = match_range(round, root)
        

        if 2**(match.round) == event.max_players:
            event.winner = winner
            event.event_state = "ended"
            if winner.id == match.player1.id:
                event.runner = match.player2
            else:
                event.runner = match.player1
            event.save()
            return Response(status=status.HTTP_200_OK)

        for m in matches:
            if m.root in matchrange and m.round == round + 1:
                if m.player1 is None:
                    m.player1 = winner
                else:
                    m.player2 = winner
                m.matchstate = "active"
                m.save()
                break
        else:
            
            if match.root not in list(matchrange)[int(len(matchrange)/2):]:
                newmatch = Match.objects.create(player1=winner, matchgame=matchgame, matchstate="pending", round=round+1, root=root) 
                newmatch.save()
            else:
                newmatch = Match.objects.create(player2=winner, matchgame=matchgame, matchstate="pending", round=round+1, root=root) 
                newmatch.save()
            event.matches.add(newmatch)
            event.save()
    elif event.event_type == "league":
        
        winner = request.data['winner']
        match.winner = User.objects.get(username=winner)
        match.winner.matches_won.add(match)
        match.player1stats = request.data['p1stats']
        match.player2stats = request.data['p2stats']
        match.matchstate = "ended"
        match.save()
        eventmatches = event.matches.all()
        matchedopponents = {player.id:[] for player in event.eventplayers.all()}
        for m in eventmatches:
            if m.matchstate in ("ended", "active"):
                matchedopponents[m.player1.id].append(m.player2.id)
                matchedopponents[m.player2.id].append(m.player1.id)
        activeplayers = []
        for m in eventmatches:
                if m.matchstate == "active":
                    activeplayers.append(m.player1.id)
                    activeplayers.append(m.player2.id)
        if len(activeplayers) == 0:
            finaltable = {}
            for p in event.eventplayers.all():
                player = {"played": 0, "win": 0, "loss": 0, "draw": 0, "points": 0}
                for field in event.eventgame.fields['fields']:
                    player[field] = 0
                finaltable[p.id] = player
            for m in eventmatches:
                if m.matchstate == "ended":
                    winner = m.matchwinner.id
                    player1 = m.player1.id
                    player2 = m.player2.id
                    player1stats = m.player1stats
                    player2stats = m.player2stats
                    finaltable[player1]["played"] += 1
                    finaltable[player2]["played"] += 1
                if winner == None:
                    finaltable[player1]['draw'] += 1
                    finaltable[player1]['points'] += 1
                    finaltable[player2]['draw'] += 1
                    finaltable[player2]['points'] += 1
                else:
                    finaltable[winner]['win'] += 1
                    finaltable[winner]['points'] += 3
                    if winner == player1: finaltable[player2]['loss'] += 1
                    else : finaltable[player1]['loss'] += 1
                for field in event.eventgame.fields['fields']:
                    finaltable[player1][field] += int(player1stats[field])
                    finaltable[player2][field] += int(player2stats[field])
            finaltablelist = [{p.id: finaltable[p.id]} for p in event.eventplayers.all()]
            sortedtablelist = sorted(finaltablelist, key=lambda x: (list(x.values())[0]['win'], list(x.values())[0][event.eventgame.fields['fields'][0]]), reverse=True)
            print(sortedtablelist)
            eventwinner = list(sortedtablelist[0].keys())[0]
            eventrunner = list(sortedtablelist[1].keys())[0]
            eventthird = list(sortedtablelist[2].keys())[0]
            eventwinner = User.objects.get(id=eventwinner)
            eventrunner = User.objects.get(id=eventrunner)
            eventthird = User.objects.get(id=eventthird)
            event.winner = eventwinner
            event.runner = eventrunner
            event.third = eventthird
            event.event_state = "ended"
            event.save()
        def give_next_match(player):
            for p in event.eventplayers.all():
                if p==player:
                    continue
                if player.id not in matchedopponents[p.id] and p.id not in activeplayers:
                    newmatch = Match.objects.create(player1=player, player2=p, matchstate="active", matchgame=event.eventgame)                 
                    event.matches.add(newmatch)
                    matchedopponents[player.id].append(p.id)
                    matchedopponents[p.id].append(player.id)
                    activeplayers.append(player.id)
                    activeplayers.append(p.id)
                    break
        if len(matchedopponents[match.player1.id]) < event.max_players - 1:
            give_next_match(match.player1)
        if len(matchedopponents[match.player2.id]) < event.max_players - 1:
            give_next_match(match.player2)
        return Response({"matches": [MatchSerializer(match).data for match in event.matches.all()]})
        # for player in event.eventplayers.all():
        #     if len(matchedopponents[player.id]) == event.max_players - 1:
        #         continue
        #     for player2 in event.eventplayers.all():
        #         if len(matchedopponents[player2.id]) == event.max_players - 1 or player==player2:
        #             continue
        #         if player not in matchedopponents[player2.id]:
        #             newmatch = Match.objects.create(player1=player, player2=player2, matchgame=event.eventgame, matchstate="active")
        #             event.matches.add(newmatch)


                # for mm in eventmatches:
                #     if m.player1 in (mm.player1, mm.player2):
                #         playedopponents.append(mm.player1 if m.player1 == mm.player2 else mm.player2)
                # if len(playedopponents) == event.max_players - 1:
                #     Match.objects.delete(m)
                #     continue
                # if match.player1 not in playedopponents:
                #     m.player2 = match.player1
                #     m.matchstate = "active"
                #     m.save()
                #     newmatch = Match.objects.create(player1=match.player2, matchstate="pending", matchgame=event.eventgame)
                #     event.matches.add(newmatch)
                # elif match.player2 not in playedopponents:
                #     m.player2 = match.player2
                #     m.matchstate = "active"
                #     m.save()
                #     newmatch = Match.objects.create(player1=match.player1, matchstate="pending", matchgame=event.eventgame)
                #     event.matches.add(newmatch)
                # else:
                #     continue


    return Response(status=status.HTTP_200_OK)

@api_view(["POST"])
def get_games(request):
    games = [GameSerializer(game).data for game in Game.objects.all()]

    return Response({"games": games})

@api_view(["POST"])
def get_playerstats(request):
    print(request.data['user'])
    player = User.objects.get(id=request.data['user'])
    stats = {}
    stats['events_joined'] = player.joined_events.count()
    stats['events_won'] = len(Event.objects.filter(winner=player))
    stats['matches_won'] = len(Match.objects.filter(matchwinner=player))
    stats['matches_played'] = len(Match.objects.filter(player1=player)) + len(Match.objects.filter(player2=player))
    cash_earned = 0
    credit_earned = 0
    for event in Event.objects.filter(winner=player):
        if event.reward_type == "cash":
            cash_earned += int(event.winner_reward)
        elif event.reward_type == "credit":
            credit_earned += int(event.winner_reward)
    stats['cash_earned'] = cash_earned
    stats['credits_earned'] = credit_earned


    return Response(stats)