function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Show the delete profile picture modal when the delete button is clicked
$('#delete-picture').click(function(event) {
    event.preventDefault();
    $('#delete-picture-modal').modal('show');
});

// Send an AJAX request to delete the profile picture when the user confirms the action
$('#confirm-delete-picture').click(function(event) {
    event.preventDefault();
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: 'delete-profile-picture/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: csrftoken
        },
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        success: function(data) {
            if (data.success) {
                // Update the UI to reflect the deletion of the picture
                $('#delete-picture-modal').modal('hide');
                $('#delete-picture').hide();
                $('#profile-picture').attr('src', '/path/to/default/profile/picture');
            } else {
                alert('Error: ' + data.error);
            }
        }
    });
});

// Show the delete icon when the user hovers over the profile picture
$('.position-relative').hover(function() {
    $('#delete-picture').show();
}, function() {
    $('#delete-picture').hide();
});
