#include <assert.h>
#include <stdio.h>

enum team
{
    AARDVARKS, BATS, CHINCHILLAS, DINGOES,
    ELEPHANTS, FOXES, GECKOS,
};

enum role
{
    HOME, AWAY
};

struct match
{
    struct match *prev_matches[2];
    enum team teams[2];
    int scores[2];
};

enum team winner(struct match *);
int rounds(struct match *);

enum team
winner(struct match *match)
{
    assert(match);
    int *scores = match->scores;
    int hscore = scores[HOME];
    int ascore = scores[AWAY];
    enum team *teams = match->teams;
    return hscore >= ascore ? teams[HOME] : teams[AWAY];
}

int
rounds(struct match *match)
{
    if (!match)
        {
            return 0;
        }
    struct match **prev_matches = match->prev_matches;
    int hrounds = 1 + rounds(prev_matches[HOME]);
    int arounds = 1 + rounds(prev_matches[AWAY]);
    return hrounds >= arounds ? hrounds : arounds;
}

int 
main()
{
    struct match qtr1 = { {NULL, NULL}, {AARDVARKS, BATS}, {10, 5} };
    struct match qtr2 = { {NULL, NULL}, {CHINCHILLAS, DINGOES}, {7, 7} };
    struct match qtr4 = { {NULL, NULL}, {FOXES, GECKOS}, {2, 3} };
    struct match semi1 = 
    { 
        {&qtr1, &qtr2}, {winner(&qtr1), winner(&qtr2)}, {9, 6} 
    };
    struct match semi2 = 
    { 
        {NULL, &qtr4}, {ELEPHANTS, winner(&qtr4)}, {2, 3} 
    };
    struct match final = 
    {
        {&semi1, &semi2}, {winner(&semi1), winner(&semi2)}, {4, 1} 
    };
    printf("Rounds: %d\n", rounds(&final));
    printf("Winner: %d\n", winner(&final));
    return 0;
}

