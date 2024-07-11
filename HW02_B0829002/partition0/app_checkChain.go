package main

import (
	"crypto/sha256"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"os/exec"
)

// checkBlock returns the current highest block number by checking the filesystem.
func checkBlock() int {
	i := 1
	for {
		if _, err := os.Stat(strconv.Itoa(i) + ".txt"); os.IsNotExist(err) {
			break
		}
		i++
	}
	return i
}

func main() {
	// Checking the number of arguments
	if len(os.Args) != 2 || os.Args[1] == "" {
		fmt.Println("Usage: go run app_checkChain.go or go run app_checkChain.go username")
		os.Exit(1)
	}

	currentBlock := checkBlock()
	var failedBlocks []int

	for i := 1; i < currentBlock-1; i++ {
		// Reading the entire content of the current block file
		content, err := ioutil.ReadFile(strconv.Itoa(i) + ".txt")
		if err != nil {
			fmt.Println("Error reading file:", err)
			continue
		}
		lineAll := string(content)

		// Calculating the hash of the current block
		hashObject := sha256.Sum256([]byte(lineAll))
		hashString := fmt.Sprintf("%x", hashObject)

		// Reading the next block to compare the stored hash
		nextBlockContent, err := ioutil.ReadFile(strconv.Itoa(i+1) + ".txt")
		if err != nil {
			fmt.Println("Error reading next file:", err)
			continue
		}
		lines := strings.Split(string(nextBlockContent), "\n")
		firstLine := lines[0]
		firstLineParts := strings.Split(firstLine, " ")
		if len(firstLineParts) < 5 {
			fmt.Println("Invalid format in next block's first line.")
			continue
		}
		storedHash := firstLineParts[4]
		// Removing potential trailing characters from the stored hash
		storedHash = strings.TrimSpace(storedHash)

		if hashString != storedHash {
			fmt.Printf("The blockchain has been tampered with at block %d\n", i)
			failedBlocks = append(failedBlocks, i)
		}
	}

	if len(failedBlocks) == 0 {
		fmt.Println("The blockchain is safe")
		if len(os.Args) == 2 {
			cmd := exec.Command("./app_transaction", "angel", os.Args[1], "5")
			cmd.Stdout = os.Stdout
			cmd.Stderr = os.Stderr
			cmd.Run()
		}
	} else {
		fmt.Println("The following blocks have been tampered with:", failedBlocks)
	}
}
