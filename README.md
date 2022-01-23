# Hanabi project exam by Alessandro Speciale (s287605)
Repository done to store the hanabi bot needed for the exam of computational intelligence (PoliTO).

# Credits
For this project, I worked in collaboration with Simone Sasso, another student of computational intelligence. We shared our ideas about how to proceed, what should we implement and collaborated on the external structure of the bot (like the thread handling and other unrelated-yet-necessary tasks).

The technical implementation of the two bots, however, was done in parallel, so the bot are totally different in terms of coding.

# Data structure
To make the bot note the hints given throughout the match, I use a dictionary of lists where each key is the name of the player.
Said dictionary can automatically update, tracking the index of the index card and can merge two value and color hints to note the full identity of a card.
NOTE: due to the key of the dictionary, each player should have a unique name.

# Rules
The bot is done in a rule based way: I tried to code basic rules and strategies that are generally recognized by the Hanabi community: still, I decided to not implement advanced strategies to try to make the bot more capable of playing against a large range of allies without being harmful.

The implemented rules are:

- Chop discarding: the chop is the oldest card in the player's hand that is not hinted in any way. It is an implicit rule of Hanabi players to discard the chop when there are not other useful moves available; by doing this, we can make our discard predictable by other players that can hint accordingly.

- Chop saving: given the before mentioned rule, chop saving is the technique in which the chop is hinted to save critical cards (like 5 or cards remained in single copy). This is useful to dodge dangerous discarding that can potentially harm the final score.
The chop saving is done by suggesting the value.

- Play hints: the bot can detect playable cards in the hands of other players and hint them in an univoque way (if possible). The receiver will implicitly understand the playability of the card and will play it.

- Multi play hint: if an univoque hint is impossible, the bot can hint card with multiple hint output in a coherent way; the focus of the hint, as known by Hanaby players, is either the chop or the newest card of the hand; the bot can then act accordingly.

- Chained hint (name created by me): I call "chained hints", those hints that are nor play hints or save hints but are simply hints that must be done because discarding is impossible (if there are not used note tokens) and playing a card is rissky because we don't have hints at disposal. In this case the bot can either:

    - Hint per value on the chop: this is done if there are not available hints to use; the bot suggest the chop card of a player using the value to make him think is a saving or, at least, a non-playable card and make it stall.
    - Using available hints: if hints are available, the chained hint is done on an hinted card to complete the information about that card and make the receiving player know its full identity.

- Discard until critical card: to avoid having a congestionated hand (too many cards to keep due to the hints) I prefer to discard cards that are not critical yet.

- Manage full chop: if the hand is full of hints and discarding is impossible, the player must make the drastic decision of discarding one of the hinted cards by avoiding, if possible, the critical cards.
Still, it is a dangerous move for an unfortunate match.

# Data matches

In the repository I also added some compressed folders containing the logs of a multitude of matches done with a different number of players (1000 matches per group, from 2 to 5).
The result are generally good from 2 to 4 players, giving an average score of 16.50 approximately while are less good, although still pretty nice with 5 players, giving an average score of approximately 15.10.
