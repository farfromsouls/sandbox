package main

import "fmt"

func main() {
	aSlice := []int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
	fmt.Println(aSlice)
	l := len(aSlice)

	// первые 5
	fmt.Println(aSlice[0:5])
	fmt.Println(aSlice[:5])

	// последние 2
	fmt.Println(aSlice[l-2:l])
	fmt.Println(aSlice[l-2:])

	// первые 5
	t := aSlice[0:5:10]
	fmt.Println(len(t), cap(t))

	// элементы с индексами 2 3 4
	// емкость  10 - 2
	t = aSlice[2:5:10]
	fmt.Println(len(t), cap(t))

	// элементы с индексами 0 1 2 3 4 
	// новая емкость 6 - 0
	t = aSlice[:5:6]
	fmt.Println(len(t), cap(t))
}