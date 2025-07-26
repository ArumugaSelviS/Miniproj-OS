#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void create_file(const char *filename) {
    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        perror("Error creating file");
        return;
    }
    fclose(file);
    printf("File '%s' created successfully\n", filename);
}

void write_to_file(const char *filename, const char *content) {
    FILE *file = fopen(filename, "a");
    if (file == NULL) {
        perror("Error opening file");
        return;
    }
    fprintf(file, "%s\n", content);
    fclose(file);
    printf("Content written to '%s' successfully\n", filename);
}

void read_file(const char *filename) {
    char buffer[256];
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error opening file");
        return;
    }
    printf("Content of '%s':\n", filename);
    while (fgets(buffer, sizeof(buffer), file)) {
        printf("%s", buffer);
    }
    fclose(file);
}

void delete_file(const char *filename) {
    char confirmation;
    printf("Are you sure you want to delete '%s'? (y/n): ", filename);
    scanf(" %c", &confirmation);
    if (confirmation == 'y' || confirmation == 'Y') {
        if (remove(filename) == 0) {
            printf("File '%s' deleted successfully\n", filename);
        } else {
            perror("Error deleting file");
        }
    } else {
        printf("Deletion of '%s' cancelled\n", filename);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <operation> <filename> [content]\n", argv[0]);
        return 1;
    }

    const char *operation = argv[1];
    const char *filename = argv[2];

    if (strcmp(operation, "create") == 0) {
        create_file(filename);
    } else if (strcmp(operation, "write") == 0 && argc == 4) {
        write_to_file(filename, argv[3]);
    } else if (strcmp(operation, "read") == 0) {
        read_file(filename);
    } else if (strcmp(operation, "delete") == 0) {
        delete_file(filename);
    } else {
        fprintf(stderr, "Invalid operation or missing arguments.\n");
    }

    return 0;
}