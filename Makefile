CC=gcc
CFLAGS=-g -Wall
MATH=-lm

all: lab8

lab8: lab8.c
	$(CC) $(CFLAGS) lab8.c -o lab8 $(MATH)
