# MARTA - Modular Active Robot Twitter Announcer

Some code I put together to build a twitter robot, inspired by 
Molly White's [twitterbot framework](http://blog.mollywhite.net/twitter-bots-pt2/).

The idea is that each module can be programmed and tested independently from the 
wrapper arount tweepy, and know as little as possible about the twitter API
(not nearly there though).

## Current modules
- niceThings: Has a list of nice messages that it sends to me
- RPS: Plays rock, paper scissors

## TODO
- niceThings: Says a nice thing to a random follower
- RPS: Keep tracks of number of games played and running scores
- General: Add some default messages about modules loaded and how to talk to them
- Bugs: Add proper hierarchical logging and testing