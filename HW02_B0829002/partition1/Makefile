# build all .go files
TARGETS = init app_checkChain app_checkLog app_checkMoney app_transaction

all: $(TARGETS)

$(TARGETS):
	go build -o $@ $@.go

.PHONY: all

rm:
	rm -f *.txt init app_checkChain app_checkLog app_checkMoney app_transaction