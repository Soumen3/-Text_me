


document.addEventListener('DOMContentLoaded', function() {
	const addFriendButtons = document.querySelectorAll('.add-friend-btn');
	const acceptFriendButtons = document.querySelectorAll('.accept-friend-btn');
	const rejectFriendButtons = document.querySelectorAll('.reject-friend-btn');

	addFriendButtons.forEach(button => {
		button.addEventListener('click', function(event) {
			event.preventDefault();
			const userId = this.getAttribute('data-user-id');
			const buttonElement = this;

			fetch(`${window.location.origin}/send-request/${userId}/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': '{{ csrf_token }}'
				},
				body: JSON.stringify({ user_id: userId })
			})
			.then(response => response.json())
			.then(data => {
				if (data.success) {
					buttonElement.outerHTML = '<span class="badge text-bg-warning">Pending</span>';
				} else {
					alert('Failed to send friend request.');
				}
			})
			.catch(error => {
				console.error('Error:', error);
				alert('An error occurred.');
			});
		});
	});

	acceptFriendButtons.forEach(button => {
		button.addEventListener('click', function(event) {
			event.preventDefault();
			const userId = this.getAttribute('data-user-id');
			const buttonElement = this;

			fetch(`${window.location.origin}/accept-request/${userId}/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': '{{ csrf_token }}'
				},
				body: JSON.stringify({ user_id: userId })
			})
			.then(response => response.json())
			.then(data => {
				if (data.success) {
					buttonElement.parentElement.innerHTML = '<span class="badge text-bg-success">Friend</span>';
				} else {
					alert('Failed to accept friend request.');
				}
			})
			.catch(error => {
				console.error('Error:', error);
				alert('An error occurred.');
			});
		});
	});

	rejectFriendButtons.forEach(button => {
		button.addEventListener('click', function(event) {
			event.preventDefault();
			const userId = this.getAttribute('data-user-id');
			const buttonElement = this;

			fetch(`${window.location.origin}/reject-request/${userId}/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': '{{ csrf_token }}'
				},
				body: JSON.stringify({ user_id: userId })
			})
			.then(response => response.json())
			.then(data => {
				if (data.success) {
					buttonElement.parentElement.innerHTML = '<span class="badge text-bg-danger">Rejected</span>';
				} else {
					alert('Failed to reject friend request.');
				}
			})
			.catch(error => {
				console.error('Error:', error);
				alert('An error occurred.');
			});
		});
	});
});