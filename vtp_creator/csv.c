#define _GNU_SOURCE

#include <err.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <vtkPolyData.h>

void printList(double *list, int len)
{
    for (int i = 0; i < len; i++)
    {
        if (i != 0)
            printf(", ");
        printf("%lf", list[i]);
    }
    printf("\n");
}

double *convertLine(char *s, int lenCol)
{
    char *save;
    char *endPtr;
    double *res = malloc(lenCol * sizeof(double));
    double convert;

    for (int i = 0; i < lenCol; i++)
    {
        save = strtok_r(s, ",\n", &s);
        convert = strtod(save, &endPtr);
        res[i] = convert;
    }
    return res;
}

void initPoints(double *line, int lenCol)
{}

int main(int argc, char const *argv[])
{
    if (argc != 2)
        return 1;

    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
        return 1;

    char *line = NULL;
    size_t size;
    ssize_t lect;

    while ((lect = getline(&line, &size, file)) != -1)
    {
        double *cells = convertLine(line, 4);
        printList(cells, 4);
        free(cells);
    }
    if (line)
        free(line);

    fclose(file);
    return 0;
}
