#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct frac
{
    int n; // numerator
    int d; // denominator
};

struct outcome
{
    char *name;
    struct frac prob;
    struct outcome **children;
    int num_children;
};

// Helper
int 
count_terminal(struct outcome *outcome)
{
    if (!outcome)
    {
        return 0;
    }
    int num_children = outcome->num_children;
    if (!num_children)
    {
        return 1;
    }
    else 
    {
        int count = 0;
        for (int i = 0; i < outcome->num_children; ++i)
        {
            count += count_terminal(outcome->children[i]);
        }
        return count;
    }
}

// Helper
struct outcome *
find_child_by_name(struct outcome *parent, char *name)
{
    if (!parent)
    {
        return NULL;
    }
    for (int i = 0; i < parent->num_children; ++i)
    {
        struct outcome *child = parent->children[i];
        if (!strcmp(child->name, name))
        {
            return child;
        }
    }
    return NULL;
}

void
event_seq_prob(struct outcome *expm, 
    char **event_names,
    int num_events, 
    struct frac *prob)
{
    if (!expm || !event_names || !prob)
    {
        return;
    }
    prob->n = 1;
    prob->d = 1;

    struct outcome *current_outcome = expm;
    for (int i = 0; i < num_events; ++i)
    {
        struct outcome *child = 
            find_child_by_name(current_outcome, event_names[i]);
        if (!child)
        {
            prob->n = 0;
            prob->d = 1;
            return;
        }
        else 
        {
            /////////
            printf("Found child \"%s\" with prob %d/%d\n", child->name, child->prob.n, child->prob.d);
            prob->n *= child->prob.n;
            prob->d *= child->prob.d;
            current_outcome = child;
        }
    }
    return;
}

void 
example1()
{
    // Example 1
    struct outcome h1 = {"H", {1, 3}, NULL, 0};
    struct outcome t1 = {"T", {2, 3}, NULL, 0};
    struct outcome h2 = {"H", {1, 4}, NULL, 0};
    struct outcome t2 = {"T", {3, 4}, NULL, 0};
    struct outcome h3 = {"H", {1, 5}, NULL, 0};
    struct outcome t3 = {"T", {4, 5}, NULL, 0};

    struct outcome *children1[2] = {&h1, &t1};
    struct outcome *children2[2] = {&h2, &t2};
    struct outcome *children3[2] = {&h3, &t3};
    struct outcome c1 = {"C1", {1, 3}, children1, 2};
    struct outcome c2 = {"C2", {1, 3}, children2, 2};
    struct outcome c3 = {"C3", {1, 3}, children3, 2};

    struct outcome *choices[3] = {&c1, &c2, &c3};
    struct outcome expm1 = {"Exp", {1, 1}, choices, 3};


}

void
example2()
{
    // Example 2
    struct outcome d13 = {"1,3", {1, 3}, NULL, 0};
    struct outcome d24 = {"2,4", {2, 4}, NULL, 0};
    struct outcome d35 = {"3,5", {3, 5}, NULL, 0};
    struct outcome *children2[3] = {&d13, &d24, &d35};

    struct outcome d12 = {"1,2", {1, 3}, children2, 3};
    struct outcome d23 = {"2,3", {1, 3}, NULL, 0};
    struct outcome d34 = {"3,4", {1, 3}, NULL, 0};
    struct outcome *children1[3] = {&d12, &d23, &d34};

    struct outcome d11 = {"1,1", {1, 3}, children1, 3};
    struct outcome d22 = {"2,2", {1, 3}, children2, 3};
    struct outcome d33 = {"3,3", {1, 3}, NULL, 0};
    struct outcome *choices[3] = {&d11, &d22, &d33};

    struct outcome expm2 = {"Exp", {1,1}, choices, 3};

    printf("Number of terminal outcomes: %d\n", 
           count_terminal(&expm2));
    
    struct frac prob = {1, 1};
    char *event_names[2] = {"2,2", "1,3"};
    event_seq_prob(&expm2, event_names, 2, &prob);
    printf("Probability of 2,2, 1,3: %d/%d\n", prob.n, prob.d);
}

int
main()
{
    example2();
    return(0);
}

