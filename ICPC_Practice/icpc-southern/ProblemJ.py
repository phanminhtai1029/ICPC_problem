n = input().split()

if n[0] == n[1]:
    print("Draw")
elif (n[0] == "Rock" and n[1] == "Scissors") or (n[0] == "Scissors" and n[1] == "Paper") or (n[0] == "Paper" and n[1] == "Rock"):
    print("Player 1")
else:
    print("Player 2")
