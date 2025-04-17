document.addEventListener("DOMContentLoaded", () => {
	const registerForm = document.getElementById("registerForm");
	const loginForm = document.getElementById("loginForm");
	const postForm = document.getElementById("postForm");
	let accessToken = ""; // Token to be set after login

	if (registerForm) {
		registerForm.addEventListener("submit", async (e) => {
			e.preventDefault();
			const username = document.getElementById("username").value;
			const email = document.getElementById("email").value;
			const password = document.getElementById("password").value;
			const messageDiv = document.getElementById("registerMessage");

			try {
				const response = await fetch("/register", {
					method: "POST",
					headers: { "Content-Type": "application/x-www-form-urlencoded" },
					body: new URLSearchParams({ username, email, password }),
				});

				const data = await response.json();
				if (response.ok) {
					messageDiv.textContent = data.message; // Show success message
					messageDiv.className = "message success"; // Add success styling
					setTimeout(() => {
						window.location.href = data.redirect_url; // Redirect to login page
					}, 2000); // Redirect after 2 seconds
				} else {
					messageDiv.textContent = `Error: ${data.error}`; // Show error message
					messageDiv.className = "message error"; // Add error styling
				}
			} catch (error) {
				console.error("Error:", error);
				messageDiv.textContent = "An unexpected error occurred.";
				messageDiv.className = "message error"; // Add error styling
			}
		});
	}

	if (loginForm) {
		loginForm.addEventListener("submit", async (e) => {
			e.preventDefault();
			const email = document.getElementById("loginEmail").value;
			const password = document.getElementById("loginPassword").value;
			const messageDiv = document.getElementById("loginMessage");

			try {
				const response = await fetch("/login", {
					method: "POST",
					headers: { "Content-Type": "application/x-www-form-urlencoded" },
					body: new URLSearchParams({ email, password }),
				});

				const data = await response.json();
				if (response.ok) {
					messageDiv.textContent = data.message; // Show success message
					messageDiv.className = "message success"; // Add success styling
					localStorage.setItem("accessToken", data.access_token); // Store the JWT token in localStorage
					setTimeout(() => {
						window.location.href = data.redirect_url; // Redirect to posts page
					}, 2000); // Redirect after 2 seconds
				} else {
					messageDiv.textContent = `Error: ${data.error}`; // Show error message
					messageDiv.className = "message error"; // Add error styling
				}
			} catch (error) {
				console.error("Error:", error);
				messageDiv.textContent = "An unexpected error occurred.";
				messageDiv.className = "message error"; // Add error styling
			}
		});
	}

	if (postForm) {
		postForm.addEventListener("submit", async (e) => {
			e.preventDefault();
			const title = document.getElementById("title").value;
			const description = document.getElementById("description").value;
			const price = document.getElementById("price").value;
			const postLocation = document.getElementById("location").value;
			const imageUrl = document.getElementById("imageUrl").value || null; // Set to null if empty

			const accessToken = localStorage.getItem("accessToken");

			try {
				const response = await fetch("/create_post", {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
						Authorization: `Bearer ${accessToken}`,
					},
					body: JSON.stringify({
						title,
						description,
						price,
						location: postLocation,
						image_url: imageUrl,
					}),
				});

				const data = await response.json();
				if (response.ok) {
					localStorage.setItem("postSuccessMessage", data.message);
					window.location.href = "/posts";
				} else {
					alert(`Error: ${data.error}`);
				}
			} catch (error) {
				console.error("Error:", error);
				alert("An unexpected error occurred.");
			}
		});
	}

	const successMessage = localStorage.getItem("postSuccessMessage");
	if (successMessage) {
		// Display the success message
		const messageDiv = document.createElement("div");
		messageDiv.className = "message success"; // Use the success styling
		messageDiv.textContent = successMessage;

		// Insert the message at the top of the posts list
		const postsList = document.getElementById("postsList");
		if (postsList) {
			postsList.insertAdjacentElement("beforebegin", messageDiv);
		}

		// Remove the message from localStorage after displaying it
		localStorage.removeItem("postSuccessMessage");
	}

	const deleteButtons = document.querySelectorAll(".delete-post-button");

	deleteButtons.forEach((button) => {
		button.addEventListener("click", async (e) => {
			const postId = button.getAttribute("data-post-id");
			const confirmDelete = confirm(
				"Are you sure you want to delete this post?"
			);
			if (!confirmDelete) return;

			const accessToken = localStorage.getItem("accessToken"); // Retrieve the JWT token

			try {
				const response = await fetch(`/posts/${postId}`, {
					method: "DELETE",
					headers: {
						Authorization: `Bearer ${accessToken}`,
					},
				});

				const data = await response.json();
				if (response.ok) {
					alert(data.message); // Show success message
					button.closest(".post-card").remove(); // Remove the post card from the DOM
				} else {
					alert(`Error: ${data.error}`); // Show error message
				}
			} catch (error) {
				console.error("Error:", error);
				alert("An unexpected error occurred.");
			}
		});
	});
});
