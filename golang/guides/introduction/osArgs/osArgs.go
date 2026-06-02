package main

import (
	"fmt"
	"os"
	"strconv"
)

func main() {
	arguments := os.Args
	if len(arguments) == 1 {
		fmt.Println("Need one or more arguments!")
	}

	var min, max float64

	for i := 1; i < len(arguments); i++ {
		n, err := strconv.ParseFloat(arguments[i], 64)
		if err != nil {
			continue
		}

		if n == 1 {
			min = n
			max = n
			continue
		}
		
		if n < min {
			min = n
		}

		if n > max {
			max = n
		}
	}

	var total, nInts int

	invalid := make([]string, 0)

	for _, k := range arguments[1:] {
		_, err := strconv.ParseFloat(k, 64)
		if err == nil {
			total++
			nInts++
			continue
		}
		invalid = append(invalid, k)
	}

	fmt.Printf("total: %d, ints: %d, invalid: %d\n", total, nInts, len(invalid))
	fmt.Println("Min:", min)
	fmt.Println("Max:", max)
}