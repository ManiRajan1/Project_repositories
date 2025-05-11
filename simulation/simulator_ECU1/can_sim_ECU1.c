// === ECU1 (C) - CAN ID 0x100 ===
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <pthread.h>
#include <linux/can.h>
#include <linux/can/raw.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <time.h>
#include "can_def.h"

int s;
struct sockaddr_can addr;
struct ifreq ifr;

unsigned char fake_crc(unsigned char *data, int len) {
    unsigned char crc = 0;
    for (int i = 0; i < len; i++) crc ^= data[i];
    return crc;
}

void *sender(void *arg) {
    struct can_frame frame;
    while (1) {
        frame.can_id  = ECU2;
        frame.can_dlc = 4;
        frame.data[0] = 0xAB;
        frame.data[1] = 0xCD;
        frame.data[2] = 0x00;
        frame.data[3] = fake_crc(frame.data, 3);

        write(s, &frame, sizeof(struct can_frame));
        printf("\033[0;32m[ECU1] Sent to ECU2 ID 0x%x\033[0m\n", ECU2);
        sleep(2);
    }
    return NULL;
}

void *receiver(void *arg) {
    struct can_frame frame;
    while (1) {
        if (read(s, &frame, sizeof(struct can_frame)) > 0) {
            if (frame.can_id == ECU1) {
                printf("\033[0;34m[ECU1] Received: ");
                for (int i = 0; i < frame.can_dlc; i++)
                    printf("%02X ", frame.data[i]);
                printf("\033[0m\n");
            } else {
                printf("\033[0;31m[ECU1] Ignored msg ID: 0x%x\033[0m\n", frame.can_id);
            }
        }
    }
    return NULL;
}

int main() {
    s = socket(PF_CAN, SOCK_RAW, CAN_RAW);
    strcpy(ifr.ifr_name, "vcan0");
    ioctl(s, SIOCGIFINDEX, &ifr);
    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;
    bind(s, (struct sockaddr *)&addr, sizeof(addr));

    pthread_t send_thread, recv_thread;
    pthread_create(&send_thread, NULL, sender, NULL);
    pthread_create(&recv_thread, NULL, receiver, NULL);

    pthread_join(send_thread, NULL);
    pthread_join(recv_thread, NULL);

    close(s);
    return 0;
}
