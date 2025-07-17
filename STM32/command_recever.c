/* command_recever.c
 ricevo i comandi dalla seriale SMT32 <- raspberry pi (UART) e li eseguo:
    - "LED_ON" accendo il LED
    - "LED_OFF" spengo il LED
    - "READ" leggo il sensore e invio la risposta
    - "RESET" riavvio la MCU (MUC = Microcontroller Unit (SMT32F103C8T6))
*/

// Inclusione delle librerie necessarie per la gestione delle periferiche STM32 e funzioni standard
#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/stm32/usart.h>
#include <string.h>
#include <libopencm3/cm3/scb.h>

void usart_setup(void);
void led_setup(void);
void usart_send_string(const char *str);


// Configurazione iniziale della USART1: (serve per comunicare con il raspberry pi)
void usart_setup(void) {
    rcc_periph_clock_enable(RCC_USART1);
    rcc_periph_clock_enable(RCC_GPIOA);

    // Configura PA9 come TX (trasmette) e PA10 come RX (riceve)
    gpio_set_mode(GPIOA, GPIO_MODE_OUTPUT_50_MHZ,
                  GPIO_CNF_OUTPUT_ALTFN_PUSHPULL, GPIO_USART1_TX);
    gpio_set_mode(GPIOA, GPIO_MODE_INPUT,
                  GPIO_CNF_INPUT_FLOAT, GPIO_USART1_RX);

    // Configura la USART1 per comunicazione seriale (9600 baud, 8N1)
    usart_set_baudrate(USART1, 9600);
    usart_set_databits(USART1, 8);
    usart_set_stopbits(USART1, USART_STOPBITS_1);
    usart_set_mode(USART1, USART_MODE_TX_RX);
    usart_set_parity(USART1, USART_PARITY_NONE);
    usart_set_flow_control(USART1, USART_FLOWCONTROL_NONE);

    // Abilita la USART1
    usart_enable(USART1);
}

// Configura il pin PA5 come output per il LED e lo spegne all'avvio
void led_setup(void) {
    rcc_periph_clock_enable(RCC_GPIOA);
    gpio_set_mode(GPIOA, GPIO_MODE_OUTPUT_2_MHZ, GPIO_CNF_OUTPUT_PUSHPULL, GPIO5);
    gpio_clear(GPIOA, GPIO5); // LED spento all'avvio
}

// Invia una stringa via USART1, carattere per carattere
void usart_send_string(const char *str) {
    while (*str) {
        usart_send_blocking(USART1, *str++);
    }
}

int main(void) {
    usart_setup();      // Inizializza la seriale
    led_setup();        // Inizializza il LED
    char buf[32];       // Buffer per il comando ricevuto
    int idx = 0;        // Indice per il buffer

    while (1) {
        // Controlla se è arrivato un nuovo carattere sulla seriale
        if (usart_get_flag(USART1, USART_SR_RXNE)) {
            char c = usart_recv(USART1);
            // Se riceve newline o il buffer è pieno, interpreta il comando
            if (c == '\n' || idx >= 31) {
                buf[idx] = 0; // Termina la stringa
                // Gestione dei comandi riconosciuti
                if (strcmp(buf, "LED_ON") == 0) {
                    gpio_set(GPIOA, GPIO5); // Accende il LED
                } else if (strcmp(buf, "LED_OFF") == 0) {
                    gpio_clear(GPIOA, GPIO5); // Spegne il LED
                } else if (strcmp(buf, "READ") == 0) {
                    // Simula lettura sensore e invia risposta (qui puoi inserire la lettura reale)
                    usart_send_string("VAL:123\n");
                } else if (strcmp(buf, "RESET") == 0) {
                    // Invia conferma e riavvia la MCU tramite reset software
                    usart_send_string("RESETTING\n");
                    scb_reset_system(); // Esegue un vero reset della MCU
                }
                idx = 0; // Pronto per il prossimo comando
            } else {
                buf[idx++] = c; // Accumula caratteri nel buffer
            }
        }
    }
}
