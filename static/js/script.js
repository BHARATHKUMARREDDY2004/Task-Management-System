// Task Management JavaScript

document.addEventListener("DOMContentLoaded", () => {
  // Initialize the application
  initializeApp()
})

function initializeApp() {
  // Set minimum date for due date inputs to today
  const dateInputs = document.querySelectorAll('input[type="date"]')
  const today = new Date().toISOString().split("T")[0]
  dateInputs.forEach((input) => {
    if (!input.value) {
      input.min = today
    }
  })

  // Auto-hide flash messages after 5 seconds
  setTimeout(() => {
    const alerts = document.querySelectorAll(".alert")
    alerts.forEach((alert) => {
      alert.style.opacity = "0"
      alert.style.transform = "translateY(-20px)"
      setTimeout(() => {
        if (alert.parentNode) {
          alert.parentNode.removeChild(alert)
        }
      }, 300)
    })
  }, 5000)

  // Add form validation
  const forms = document.querySelectorAll("form")
  forms.forEach((form) => {
    form.addEventListener("submit", validateForm)
  })
}

function validateForm(event) {
  const form = event.target
  const titleInput = form.querySelector('input[name="title"]')

  if (titleInput && titleInput.value.trim() === "") {
    event.preventDefault()
    showNotification("Task title is required!", "error")
    titleInput.focus()
    return false
  }

  // Validate due date is not in the past (only for new tasks)
  const dueDateInput = form.querySelector('input[name="due_date"]')
  if (dueDateInput && dueDateInput.value) {
    const selectedDate = new Date(dueDateInput.value)
    const today = new Date()
    today.setHours(0, 0, 0, 0)

    if (selectedDate < today && !form.querySelector('input[name="status"]')) {
      event.preventDefault()
      showNotification("Due date cannot be in the past!", "error")
      dueDateInput.focus()
      return false
    }
  }

  return true
}

function filterTasks() {
  const statusFilter = document.getElementById("status-filter").value
  const priorityFilter = document.getElementById("priority-filter").value
  const taskCards = document.querySelectorAll(".task-card")

  taskCards.forEach((card) => {
    const taskStatus = card.getAttribute("data-status")
    const taskPriority = card.getAttribute("data-priority")

    const statusMatch = statusFilter === "all" || taskStatus === statusFilter
    const priorityMatch = priorityFilter === "all" || taskPriority === priorityFilter

    if (statusMatch && priorityMatch) {
      card.style.display = "block"
      card.style.animation = "slideIn 0.3s ease"
    } else {
      card.style.display = "none"
    }
  })

  // Update stats after filtering
  updateStats()
}

function updateTaskStatus(taskId, newStatus) {
  // Show loading state
  const statusSelect = event.target
  const originalValue = statusSelect.getAttribute("data-original-value") || statusSelect.value
  statusSelect.disabled = true

  fetch(`/api/tasks/${taskId}/status`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ status: newStatus }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to update task status")
      }
      return response.json()
    })
    .then((data) => {
      // Update the task card's data attribute
      const taskCard = statusSelect.closest(".task-card")
      taskCard.setAttribute("data-status", newStatus)

      // Update stats
      updateStats()

      // Show success notification
      showNotification("Task status updated successfully!", "success")

      // Store the new value as original
      statusSelect.setAttribute("data-original-value", newStatus)
    })
    .catch((error) => {
      console.error("Error updating task status:", error)

      // Revert the select to original value
      statusSelect.value = originalValue

      // Show error notification
      showNotification("Failed to update task status. Please try again.", "error")
    })
    .finally(() => {
      statusSelect.disabled = false
    })
}

function updateStats() {
  const taskCards = document.querySelectorAll(
    '.task-card[style*="display: block"], .task-card:not([style*="display: none"])',
  )

  let pendingCount = 0
  let progressCount = 0
  let completedCount = 0

  taskCards.forEach((card) => {
    const status = card.getAttribute("data-status")
    switch (status) {
      case "pending":
        pendingCount++
        break
      case "in_progress":
        progressCount++
        break
      case "completed":
        completedCount++
        break
    }
  })

  // Update stat cards
  const pendingElement = document.getElementById("pending-count")
  const progressElement = document.getElementById("progress-count")
  const completedElement = document.getElementById("completed-count")

  if (pendingElement) pendingElement.textContent = pendingCount
  if (progressElement) progressElement.textContent = progressCount
  if (completedElement) completedElement.textContent = completedCount
}

function showNotification(message, type = "info") {
  // Create notification element
  const notification = document.createElement("div")
  notification.className = `alert alert-${type}`
  notification.innerHTML = `
        <div style="display: flex; align-items: center;">
            <i class="fas fa-${type === "success" ? "check-circle" : "exclamation-triangle"}"></i>
            <span style="margin-left: 10px;">${message}</span>
        </div>
        <button class="alert-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `

  // Add to page
  const container = document.querySelector(".container")
  const existingMessages = document.querySelector(".flash-messages")

  if (existingMessages) {
    existingMessages.appendChild(notification)
  } else {
    const messagesContainer = document.createElement("div")
    messagesContainer.className = "flash-messages"
    messagesContainer.appendChild(notification)
    container.insertBefore(messagesContainer, container.firstChild)
  }

  // Auto-remove after 5 seconds
  setTimeout(() => {
    if (notification.parentNode) {
      notification.style.opacity = "0"
      notification.style.transform = "translateY(-20px)"
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification)
        }
      }, 300)
    }
  }, 5000)
}

// Keyboard shortcuts
document.addEventListener("keydown", (event) => {
  // Ctrl/Cmd + N: Create new task
  if ((event.ctrlKey || event.metaKey) && event.key === "n") {
    event.preventDefault()
    window.location.href = "/create"
  }

  // Escape: Go back to dashboard
  if (event.key === "Escape" && window.location.pathname !== "/") {
    window.location.href = "/"
  }
})

// Add smooth scrolling for better UX
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault()
    const target = document.querySelector(this.getAttribute("href"))
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      })
    }
  })
})

// Store original values for status selects
document.addEventListener("DOMContentLoaded", () => {
  const statusSelects = document.querySelectorAll(".status-select")
  statusSelects.forEach((select) => {
    select.setAttribute("data-original-value", select.value)
  })
})
