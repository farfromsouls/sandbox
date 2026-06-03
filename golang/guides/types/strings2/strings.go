package main

import (
	s "strings"
	"unicode"
	"fmt"
)

var f = fmt.Printf

func main() {
	// Сравнение строк без учета регистра
	f("EqualFold: %v\n", s.EqualFold("Mihalis", "MIHAlis")) // True
	f("EqualFold: %v\n", s.EqualFold("Mihalis", "MIHAli"))  // False

	// Поиск индекса с учетом регистра
	f("Index: %v\n", s.Index("Mihalis", "ha"))
	f("Index: %v\n", s.Index("Mihalis", "Ha"))

	// Проверка вхождения с одной из сторон с учетом регистра
	f("Prefix: %v\n", s.HasPrefix("Mihalis", "Mi"))
	f("Prefix: %v\n", s.HasPrefix("Mihalis", "mi"))
	f("Suffix: %v\n", s.HasSuffix("Mihalis", "is"))
	f("Suffix: %v\n", s.HasSuffix("Mihalis", "IS"))

	// Разбиение строки на срез подстрок по unicode.IsSpace параметру сплита
	t := s.Fields("This is a string!")
	f("Fields: %v\n", len(t))
	t = s.Fields("ThisIs a\tstring")
	f("Fields: %v\n", len(t))

	// Разбиение строки на срез подстрок с кастомным разделителем
	// И замена водстрок в строке 
	f("%s\n", s.Split("abcd efg", ""))
	f("%s\n", s.Replace("abcd efg", "", "_", -1))
	f("%s\n", s.Replace("abcd efg", "", "_", 4))
	f("%s\n", s.Replace("abcd efg", "", "_", 2))

	// Разбивает по строкам разделителям оставляя их внутри строк среза
	f("SplitAfter: %s\n", s.SplitAfter("123++432++", "++"))
	for _, v := range s.SplitAfter("123++432++", "++") {
		fmt.Printf("%s\n", v)
	}

	// функция-фильтр
	trimfunc := func(c rune) bool {
		return !unicode.IsLetter(c)
	}

	// фльтрация строки по символам
	f("Thimfunc %s\n", s.TrimFunc("123 abc ABC \t .", trimfunc))
}