# Makefile per STM32F103C8T6 (Blue Pill) con libopencm3
# Compila command_recever.c e genera il binario pronto per il flash

PROJECT = command_recever
BUILD_DIR = bin

CFILES = command_recever.c

DEVICE = stm32f103c8t6
OOCD_FILE = board/stm32f103c8t6.cfg

OPENCM3_DIR = ../libopencm3

include $(OPENCM3_DIR)/mk/genlink-config.mk
include $(OPENCM3_DIR)/tests/rules.mk
include $(OPENCM3_DIR)/mk/genlink-rules.mk

