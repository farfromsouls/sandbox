package main

import (
	"fmt"
)

// константы в go могут быть как локальными так и глобальными
// go использует boolean, string или number в качестве типа для хранения постоянных значений
// т.к. это позволяет go быть более гибким при работе с константами

// генератор констант Iota:

type Digit int;
type Power2 int;

const PI = 3.1415926

const (
	C1 = "C1C1C1"
	C2 = "C2C2C2"
	C3 = "C3C3C3"
)

func main() {
	const s1 = 123
	var v1 float32 = s1 * 12
	fmt.Println(v1)
	fmt.Println(PI)

	// генерация констант
	const (
		Zero Digit = iota
		One
		Two
		Three
		Four
	)
	// эквивалентно 
/* 	const (
		Zero = 0
		One = 1
		Two = 2
		Three = 3
		Four = 4
	) */
	
	fmt.Println(One)
	fmt.Println(Two)

	const (
		p2_0 Power2 = 1 << iota // iota = 0
		_    // пропускает нежелательные значения
		p2_2 // iota = 2, a p2_2 = 1<<2 = 0b00000100 = 4
		_
		p2_4 // 16
		_
		p2_6 // 64
	)

	fmt.Println("2^0:", p2_0);
	fmt.Println("2^2:", p2_2);
	fmt.Println("2^4:", p2_4);
	fmt.Println("2^6:", p2_6);
}