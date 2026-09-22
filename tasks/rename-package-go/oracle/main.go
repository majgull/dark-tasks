package main

import (
	"fmt"

	"app/internal/strutil"
)

func main() {
	fmt.Println(strutil.Reverse("dark"))
	fmt.Println(strutil.Initials("dark factory runner"))
}
