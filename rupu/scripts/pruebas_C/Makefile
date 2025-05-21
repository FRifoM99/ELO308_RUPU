CFLAGS=-c -Wall -O2
LIBS = -ltof

all: tofdemo

tofdemo: main.o libtof.a
	$(CC) main.o $(LIBS) -o tofdemo

main.o: main.c
	$(CC) $(CFLAGS) main.c

libtof.a: tof.o
	ar -rc libtof.a tof.o
	sudo cp libtof.a /usr/local/lib
	sudo cp tof.h /usr/local/include

tof.o: tof.c
	$(CC) $(CFLAGS) tof.c

clean:
	rm -f *.o tofdemo libtof.a