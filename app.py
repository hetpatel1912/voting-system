from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# ================= CONFIG =================
ADMIN_PASSWORD = "admin123"

# ================= DATA STRUCTURES =================
votes = {"A": 0, "B": 0, "C": 0}
voted_users = set()

# ================= LINKED LIST =================
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

        if self.head is None:
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


vote_list = VoteLinkedList()

# ================= BINARY SEARCH =================
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

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- VOTE ----------------
@app.route("/vote", methods=["GET", "POST"])
def vote():
    if request.method == "POST":
        user = request.form["user"]
        candidate = request.form["candidate"]

        if user in voted_users:
            return "❌ You have already voted!"

        votes[candidate] += 1
        voted_users.add(user)
        vote_list.add_vote(user, candidate)

        return redirect("/result")

    return render_template("vote.html")


# ---------------- RESULT ----------------
@app.route("/result", methods=["GET", "POST"])
def result():
    sorted_results = sorted(votes.items(), key=lambda x: x[1], reverse=True)
    winner = max(votes, key=votes.get)

    all_votes = vote_list.get_all_votes()

    # Graph data
    labels = []
    values = []
    for c, v in sorted_results:
        labels.append(f"Candidate {c}")
        values.append(v)

    # Binary Search
    users = sorted([user for user, _ in all_votes])
    search_user = None
    found = None

    if request.method == "POST" and "search_user" in request.form:
        search_user = request.form["search_user"]
        found = binary_search(users, search_user)

    # 🔐 Admin control for vote history
    show_history = False
    password_error = False

    if request.method == "POST" and "admin_password" in request.form:
        if request.form["admin_password"] == ADMIN_PASSWORD:
            show_history = True
        else:
            password_error = True

    return render_template(
        "result.html",
        results=sorted_results,
        winner=winner,
        all_votes=all_votes,
        labels=labels,
        values=values,
        search_user=search_user,
        found=found,
        show_history=show_history,
        password_error=password_error
    )


# ---------------- RESET ----------------
@app.route("/reset", methods=["POST"])
def reset():
    global votes
    global voted_users
    global vote_list

    password = request.form.get("password")

    if password == ADMIN_PASSWORD:
        votes = {"A": 0, "B": 0, "C": 0}
        voted_users = set()
        vote_list = VoteLinkedList()
        return redirect("/")
    else:
        return "❌ Wrong Password!"


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)







