from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# ================= DSA STRUCTURES =================

# HashMap for vote counting
votes = {"A": 0, "B": 0, "C": 0}

# Set to prevent duplicate voting
voted_users = set()

# ========== LINKED LIST IMPLEMENTATION ==========

class Node:
    def __init__(self, user, candidate):
        self.user = user
        self.candidate = candidate
        self.next = None

class VoteLinkedList:
    def __init__(self):
        self.head = None

    def add_vote(self, user, candidate):
        new_node = Node(user, candidate)

        if not self.head:
            self.head = new_node
            return

        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_node

    def get_all_votes(self):
        temp = self.head
        votes_list = []

        while temp:
            votes_list.append((temp.user, temp.candidate))
            temp = temp.next

        return votes_list

# Create Linked List object
vote_list = VoteLinkedList()

# ========== BINARY SEARCH FUNCTION ==========

def binary_search(arr, target):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return True
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return False

# ================= ROUTES =================

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Voting Page
@app.route("/vote", methods=["GET", "POST"])
def vote():
    if request.method == "POST":
        user = request.form["user"]
        candidate = request.form["candidate"]

        # Prevent duplicate voting
        if user in voted_users:
            return "You have already voted!"

        # Count vote
        votes[candidate] += 1
        voted_users.add(user)

        # Store in Linked List
        vote_list.add_vote(user, candidate)

        return redirect("/result")

    return render_template("vote.html")

# Result Page + Search
@app.route("/result", methods=["GET", "POST"])
def result():
    # Sorting results
    sorted_results = sorted(votes.items(), key=lambda x: x[1], reverse=True)

    # Winner
    winner = max(votes, key=votes.get)

    # Linked List data
    all_votes = vote_list.get_all_votes()

    # Graph data
    labels = [f"Candidate {c}" for c, v in sorted_results]
    values = [v for c, v in sorted_results]

    # Prepare user list for binary search
    users = sorted([user for user, _ in all_votes])

    search_user = None
    found = None

    # Handle search input
    if request.method == "POST":
        search_user = request.form["search_user"]
        found = binary_search(users, search_user)

    return render_template(
        "result.html",
        results=sorted_results,
        winner=winner,
        all_votes=all_votes,
        labels=labels,
        values=values,
        search_user=search_user,
        found=found
    )

# Run Server
if __name__ == "__main__":
    app.run(debug=True, port=5001)
