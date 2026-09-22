package main

import (
	"errors"
	"fmt"
	"strconv"
	"strings"
)

// Eval evaluates a reverse-Polish expression: tokens separated by one
// or more spaces, each token either a decimal integer (an optional
// leading '-' allowed, so "-7" is a number; a leading '+' is not, so
// "+1" is a bad token) or one of the operators + - * /. An operator pops the top two values b (top) and a (below)
// and pushes a op b, so "3 4 -" is -1 and "7 2 /" is 3. Division
// truncates toward zero ("-7 2 /" is -3). Errors: division by zero
// ("division by zero"), an operator with fewer than two values on the
// stack ("stack underflow"), a token that is neither ("bad token: X"),
// and an expression that leaves the stack without exactly one value
// (including the empty expression) ("malformed expression"). On error
// the returned int is 0.
func Eval(expr string) (int, error) {
	var stack []int
	for _, tok := range strings.Fields(expr) {
		switch tok {
		case "+", "-", "*", "/":
			if len(stack) < 2 {
				return 0, errors.New("stack underflow")
			}
			b, a := stack[len(stack)-1], stack[len(stack)-2]
			stack = stack[:len(stack)-2]
			var r int
			switch tok {
			case "+":
				r = a + b
			case "-":
				r = a - b
			case "*":
				r = a * b
			case "/":
				if b == 0 {
					return 0, errors.New("division by zero")
				}
				r = a / b
			}
			stack = append(stack, r)
		default:
			n, err := strconv.Atoi(tok)
			if err != nil || tok[0] == '+' {
				return 0, fmt.Errorf("bad token: %s", tok)
			}
			stack = append(stack, n)
		}
	}
	if len(stack) != 1 {
		return 0, errors.New("malformed expression")
	}
	return stack[0], nil
}
