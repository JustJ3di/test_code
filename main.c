#include <stdio.h>
#include <string.h>

void copy_bytes(void *dest, const void *src, size_t n) {
    memcpy(dest, src, n);
}

int main() {
    char buffer[256];
    const char *message = "Hello, this is a message to be copied!";
    size_t message_length = strlen(message) + 1; // +1 to include the null terminator

    if (message_length <= sizeof(buffer)) {
        copy_bytes(buffer, message, message_length);
        printf("Copied message: %s\n", buffer);
    } else {
        printf("Message is too long to copy!\n");
    }

    return 0;
}
