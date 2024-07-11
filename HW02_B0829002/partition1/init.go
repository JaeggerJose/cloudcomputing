package main


import (
    "fmt"
    "os"
	"crypto/sha256"
	"encoding/hex"
)

func main() {
	dat, err := os.Open("1.txt")
	if err != nil {
		// create file and write
		f, err := os.Create("1.txt")
		if err != nil {
			fmt.Println(err)
			return
		}
		defer f.Close()
		hash := sha256.New()
		hash.Write([]byte("cloud computing and big data"))
		f.WriteString("Sha256 of previous block: " + hex.EncodeToString(hash.Sum(nil)))
		f.WriteString("\nNect block: 2.txt\n")
		transaction := "god, angel, 1000000\n"
		f.WriteString(transaction)
		return
	} else {
		// block inited return
		fmt.Println("Block already inited")
		defer dat.Close()
		return
	}

}
