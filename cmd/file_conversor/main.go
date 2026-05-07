package main

import (
	"fmt"
)

func main() {
	fmt.Println("Hello, Go!")
	defer func() { fmt.Println("This will be printed after the panic is recovered.") }()
}
