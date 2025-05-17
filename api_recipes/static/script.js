document.addEventListener("DOMContentLoaded", function () {
  // Fetch the users from the API
  fetch("http://127.0.0.1/users/") // Replace with your actual FastAPI endpoint
    .then((response) => response.json())
    .then((data) => {
      const tableBody = document.querySelector("#users-table tbody");

      data.forEach((user) => {
        // Create a new row
        const row = document.createElement("tr");

        // Create cells for user data
        const idCell = document.createElement("td");
        idCell.textContent = user.id;

        const emailCell = document.createElement("td");
        emailCell.textContent = user.email;

        const isActiveCell = document.createElement("td");
        isActiveCell.textContent = user.is_active ? "Yes" : "No";

        const recipesCell = document.createElement("td");
        recipesCell.textContent =
          user.recipes.length > 0 ? user.recipes.join(", ") : "No Recipes";

        // Append cells to the row
        row.appendChild(idCell);
        row.appendChild(emailCell);
        row.appendChild(isActiveCell);
        row.appendChild(recipesCell);

        // Append the row to the table body
        tableBody.appendChild(row);
      });
    })
    .catch((error) => console.error("Error fetching users:", error));
});
