# Overview
---
This repo is a coding exercise to implement a five in a row game.

# Running
---
To run this:
 - Clone the repo
 - run `python server.py`
 - run `python client.py` (twice as need two clients to play)

#### N.B Server and clients run on 127.0.0.1:9000 by default, edit config.json to change this

### Requirements
---
 - Python 3.9+

# Design and Commentary
---

I think it is always good practice to review your own code after it is done. So here I will go over some of the design choices I made that could be questioned in 
a normal code review, and comment on why they were made (spoiler mostly due to time constraints), and what I would change given more time/knowledge.

I did set myself the hard limit of the recommended 8 hours on this, as didn't want to mislead in my abilities.

 - **Server-client connection is not HTTP:** Have little experience in prolonged server - client connections, and for first reading of docs not sure if persistent 
 connections are possible over HTTP or if they are single request only. Instead opted to learn how to use TCP sockets as proved more promising given the time constraints
   - Did consider the idea of after recieving a request from one client, and then finishing the request from the other before replying to the first client.
   e.g. Have pending requests from clients joining, so can still contact them, player 1 sends their move, and then before returning info to player 1, send the updated 
   board to player 2 and get their move
   - This approach was not followed though as I had already a number of the 8 hours recommended to work on this working on the TCP socket solution
   - This approach of juggling the connections also seems error prone, especially when the game might not always be as simple as recieve single message/send single message
 - Language choice: Python. Chose to do it in python as when working with new concepts and technologies (in this case TCP sockets) find it easier to use a more flexible
 language for a the initial prototyping. For a more permanent product, a statically typed langauge (such as java or c++) would be my choice as I find them more robust
 and easier to maintain.
 - Recieving of response from the server: In the main client loop, the client will wait for a response from the server. The function that does this simply prints everything
 recieved from the server, waiting for certain key phrases before returning. This is quite bad, and should be one of the first things to look at if this was going to become
 a user facing product, would be the first thing I would recommend changing. It is bad because any change to server responses could cause the client to become stuck in
 and infinite loop. (Also listening blocks main thread preventing player from leaving gracefully when waiting (must ctrl-c or kill process))
 - Minor edit: Would rename `is_won` method, as name `is_x` methods are normally reserved for functions that return booleans, and could cause unintended bugs if used without
 reading docstring fully.
 - Test coverage: There is minimal test coverage, only for the main functionality of the Game class, and even then it could be far more exhaustive to look for errors.
 With more time would add data driven testing and a generator to more exhaustively test for edge cases in the game. Would also test for client and server errors/edge 
 cases with regards to dropping connections at specific times.
 - Input handling: Input handling was pretty good (IMO). Check that only valid inputs are sent on the client side, and server will poll the client for a new input if the 
 input they sent is not valid.
 - Well documented: Overall well documented, good use of type hinting (IMO). Maybe abuse the new walrus (:= (assignment expression)) a bit.
 - Exception handling: There are a couple of try/except blocks that except base `Exception`. Should narrow this down to avoid quietly killing exceptions from bugs
