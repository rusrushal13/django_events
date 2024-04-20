/* Project specific Javascript goes here. */

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

$(document).ready(function () {
  $(".subscribe-btn, .unsubscribe-btn").click(function () {
    let $this = $(this);
    let eventId = $this.data("event-id");
    let isSubscribing = $this.hasClass("subscribe-btn");
    let baseUrl = "/api/event/";
    let action = isSubscribing ? "subscribe/" : "unsubscribe/";
    let url = baseUrl + eventId + "/" + action;

    let csrftoken = getCookie("csrftoken");

    $.ajax({
      url: url,
      method: "POST",
      data: {
        event_id: eventId,
        csrfmiddlewaretoken: csrftoken,
      },
      success: function () {
        let messageText = isSubscribing
          ? "Subscribed successfully."
          : "Unsubscribed successfully.";

        if (isSubscribing) {
          $this
            .removeClass("btn-primary subscribe-btn")
            .addClass("btn-danger unsubscribe-btn")
            .text("Unsubscribe");
          $("#message-container").html(
            `<div class="alert alert-success">${messageText}</div>`
          );
        } else {
          $this
            .removeClass("btn-danger unsubscribe-btn")
            .addClass("btn-primary subscribe-btn")
            .text("Subscribe");
          $("#message-container").html(
            `<div class="alert alert-danger">${messageText}</div>`
          );
        }

        setTimeout(function () {
          $("#message-container").html("");
        }, 2000);
      },
      error: function () {
        alert("An error occurred. Please try again.");
      },
    });
  });
});
