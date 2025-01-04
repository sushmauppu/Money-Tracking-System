document.addEventListener("DOMContentLoaded", function () {
    fetch('/get_fixed_payments')
        .then(response => response.json())
        .then(data => {
            const fixedIncomesList = document.getElementById("fixed-incomes-list");
            data.forEach(income => {
                const li = document.createElement("li");
                li.textContent = `${income.Description} - $${income.Amount}`;
                fixedIncomesList.appendChild(li);
            });
        });

    document.getElementById("transaction-form").addEventListener("submit", function (e) {
        e.preventDefault();
        const date = document.getElementById("date").value;
        const description = document.getElementById("description").value;
        const amount = document.getElementById("amount").value;
        const type = document.getElementById("type").value;

        fetch('/add_transaction', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ date, description, amount, type })
        }).then(response => response.json())
          .then(result => alert(result.message));
    });
});
