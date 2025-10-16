#include <stdio.h>
#include <stddef.h>
#include <stdbool.h>

struct empl
{
    char *name;
    char *title;
    int salary;
    struct empl **subords;
    int num_subords;
};

struct sal_data
{
    int salary;
    char *name;
};

struct sal_inv_pair
{
    bool found;
    struct empl *director;
    struct empl *subord;
};

typedef struct empl *org_t;

void empl_init(struct empl *, char *, char *, int, struct empl **, int);
void try_update_min_sal_data(int, char *, struct sal_data *);
void get_dept_min_sal_data(struct empl *, struct sal_data *);
void find_dept_sal_inv(struct empl *, struct sal_inv_pair *);
void example(void);

void
empl_init(struct empl *empl, char *name, char *title, 
    int salary, struct empl **subords, int nsubords)
{
    if (!empl)
    {
        return;
    }
    empl->name = name;
    empl->title = title;
    empl->salary = salary;
    empl->subords = subords;
    empl->num_subords = nsubords;
}

void
try_update_min_sal_data(int salary, char *name, 
    struct sal_data *msdata)
{
    if (!name || !msdata)
    {
        return;
    }
    if (salary < msdata->salary || msdata->salary < 0)
    {
        msdata->salary = salary;
        msdata->name = name;
    }
}

// Update MSDATA to lowest salary and holder within DIRECTOR's department
void get_dept_min_sal_data(struct empl *director, 
    struct sal_data *msdata)
{
    if (!director || !msdata)
    {
        return;
    }
    // Visit director's node
    try_update_min_sal_data(director->salary, director->name, msdata);

    struct empl **subords = director->subords;
    if (subords)
    {
        int nsubords = director->num_subords;
        for (int i = 0; i < nsubords; ++i)
        {
            // Visit direct subordinate's node
            get_dept_min_sal_data(subords[i], msdata);
        }
    }
}

void 
find_dept_sal_inv(struct empl *director, struct sal_inv_pair *invpair)
{
    if (!director || !invpair)
    {
        return;
    }
    struct empl **subords = director->subords;
    if (!subords)
    {
        return;
    }
    int nsubords = director->num_subords;
    for (int i = 0; i < nsubords; ++i)
    {
        if (invpair->found)
        {
            return;
        }
        struct empl *sub = subords[i];
        printf("Checking salary inversion between %s and %s\n",
            director->name, sub->name);
        if (sub->salary > director->salary)
        {
            invpair->found = true;
            invpair->director = director;
            invpair->subord = sub;
            return;
        }
        else 
        {
            find_dept_sal_inv(sub, invpair);
        }
    }
}

void
example(void)
{
    struct empl turner, jacobs, jones, jacobsen,
        jensen, thompson, jordan, jennings, johnson;
    struct empl *subs_thompson[1], *subs_jordan[2], *subs_jennings[2],
        *subs_johnson[3];

    empl_init(&turner, "Theresa Turner", "Backend Dev", 250000, NULL, 0);
    empl_init(&jacobs, "Joyce Jacobs", "IT Staff", 90000, NULL, 0);
    empl_init(&jones, "Jane Jones", "IT Staff", 80000, NULL, 0);
    empl_init(&jacobsen, "Juliet Jacobsen", "Account Manager", 200000, NULL, 0);
    empl_init(&jensen, "Josie Jensen", "Account Manager", 200000, NULL, 0);
    empl_init(&thompson, "Tina Thompson", "CIO", 1300000, subs_thompson, 1);
    subs_thompson[0] = &turner;
    empl_init(&jordan, "Jessica Jordan", "CTO", 600000, subs_jordan, 2);
    subs_jordan[0] = &jacobs; 
    subs_jordan[1] = &jones;
    empl_init(&jennings, "Julia Jennings", "CFO", 500000, subs_jennings, 2);
    subs_jennings[0] = &jacobsen;
    subs_jennings[1] = &jensen;
    empl_init(&johnson, "Jasmine Johnson", "CEO", 1400000, subs_johnson, 3);
    subs_johnson[0] = &thompson;
    subs_johnson[1] = &jordan;
    subs_johnson[2] = &jennings;

    org_t org = &johnson;

    struct sal_data msdata = {-1000, NULL};
    struct sal_inv_pair invpair = {false, NULL, NULL};

    get_dept_min_sal_data(org, &msdata);
    if (msdata.name)
    {
        printf("Person with lowest salary: %s\n", msdata.name);
    }

    turner.salary *= 10;
    find_dept_sal_inv(org, &invpair);
    if (invpair.found && invpair.director && invpair.subord)
    {
        printf("Salary inversion found between %s and %s\n",
            invpair.director->name, invpair.subord->name);
    }
}

int 
main()
{
    example();
    return 0;
}

