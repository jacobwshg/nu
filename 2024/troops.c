#include <stdio.h>
#include <string.h>

struct area_command
{
    char *name;
    int area;
    int ntroops;
    struct area_command *parent;
    struct area_command **children;
    int nchildren; 
};

void
area_comm_init(struct area_command *comm, char *name, int area, int ntroops,
    struct area_command *parent, struct area_command **children, int nchildren)
{
    if (!comm)
    {
        return;
    }
    comm->name = name;
    comm->area = area;
    comm->ntroops = ntroops;
    comm->parent = parent;
    comm->children = children;
    comm->nchildren = nchildren;
}

int
count_troops(struct area_command *comm)
{
    if (!comm)
    {
        return 0;
    }
    int ntroops = comm->ntroops;
    for (int i = 0; i < comm->nchildren; ++i)
    {
        ntroops += count_troops(comm->children[i]);
    }
    return ntroops;
}

struct area_command *
find_area_comm_by_name(char *name, struct area_command *search_root)
{
    if (!name || !search_root)
    {
        return NULL;
    }

    if (!strcmp(name, search_root->name))
    {
        return search_root;
    }
    else
    {
        for (int i = 0; i < search_root->nchildren; ++i)
        {
            struct area_command *child_res = 
                find_area_comm_by_name(name, search_root->children[i]);
            if (child_res)
            {
                return child_res;
            }
        }
        return NULL;
    }
}

int 
count_parent_troops_by_name(char *name, struct area_command *search_root)
{
    if (!name || !search_root)
    {
        return 0;
    }

    struct area_command *comm = find_area_comm_by_name(name, search_root);
    if (!comm)
    {
        return 0;
    }
    int ntroops = comm->ntroops;
    for (struct area_command *parent = comm->parent;
        parent;
        parent = parent->parent)
    {
        ntroops += parent->ntroops;
    }
    return ntroops;
}

void
example(void)
{
    struct area_command empire, inrim, ourim, tatooine, hoth;
    struct area_command *children_empire[2];
    children_empire[0] = &inrim;
    children_empire[1] = &ourim;
    struct area_command *children_ourim[2];
    children_ourim[0] = &tatooine;
    children_ourim[1] = &hoth;

    area_comm_init(&empire, "First Galactic Empire", 20000000, 100,
        NULL, children_empire, 2);
    area_comm_init(&inrim, "Inner Rim", 10000000, 2000,
        &empire, NULL, 0);
    area_comm_init(&ourim, "Outer Rim", 10000000, 1000,
        &empire, children_ourim, 2);
    area_comm_init(&tatooine, "Tatooine", 1500000, 2000,
        &ourim, NULL, 0);
    area_comm_init(&hoth, "Hoth", 700000, 2000,
        &ourim, NULL, 0);

    printf("Total number of troops under %s: %d\n", empire.name, 
        count_troops(&empire));
    printf("Total parent troops of %s: %d\n", "Tatooine",
        count_parent_troops_by_name("Tatooine", &empire));
}

int 
main()
{
    example();
    return 0;
}

