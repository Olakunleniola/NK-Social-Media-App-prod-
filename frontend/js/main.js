$.ajaxSetup({
    beforeSend: function beforeSend(xhr, settings) {
        function getCookie(name) {
            let cookieValue = null;


            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');

                for (let i = 0; i < cookies.length; i += 1) {
                    const cookie = jQuery.trim(cookies[i]);

                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }

            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
    },
});


$(document).ready(function() {
    const currentPath = window.location.pathname
    // console.log(currentPath)
    $(".nav-link").each(function(){
        const linkPath = $(this).attr("href")
        if (currentPath === linkPath){
            $(this).addClass("border-b-2 border-teal-500 text-teal-400")
        }
    })

    const isDarkMode = localStorage.getItem('darkMode') === 'true';

    // Apply dark mode to the body if needed
    if (isDarkMode) {
        $("body").addClass('dark');
    }
})


$(document).on("click", ".js-toggle-modal", function(e) {
    e.preventDefault()
    $(".js-modal").toggleClass("hidden")
})

.on("click", ".js-post-submit", function(e){
    e.preventDefault();
    const $btn = $(this);
    const $textarea = $(".js-post-text");
    const text = $textarea.val().trim();
    const buttonInnerHtml = $btn.html(); 
    // console.log($('#upload').prop("files"));
    const imageFile = $('#upload').prop("files")[0];
    const formData = new FormData();
    
    formData.append('post', text);
    formData.append('image', imageFile);

    if(!text.length){return false}

    $btn.prop("disabled", true).text("Posting....");

    $.ajax({
        type: "POST",
        url: $textarea.data("post-url"),
        data: formData,
        processData: false,  // Prevent jQuery from processing data
        contentType: false,  // Prevent jQuery from setting content type

        success: (htmlData) => {    
            $(".post-container").prepend(htmlData)
            $btn.prop("disabled", false).html(buttonInnerHtml)
            $(".js-modal").addClass("hidden z-50");
            $textarea.val("");
            $('#upload').val("");
            $("#imagePreview").css("display", "none");
        },

        error: (error) => {
            console.warn(error);
            $btn.addClass("bg-red-500 text-white");
            $btn.prop("diabled", false).text("Error").css("background-color", "red");
        }
    })
})

.on("click", ".js-follow", function(e) {
    e.preventDefault()
    const action = $(this).attr("data-action")


    $.ajax({
        type: "POST",
        url: $(this).data("url") ,
        data: {
            username: $(this).data("username"),
            action: action
        },
        
        success: (data) => {    
           $(".js-follow-text").text(data.wording)
           $(".followers").text(data.followers)
           $(".following").text(data.following)
           if (action === "Follow"){
                $(this).attr("data-action", "Unfollow")
            }else {
                $(this).attr("data-action", "Follow")
           }
        },

        error: (error) => {
            console.log(error.responseText)
        }
            
    })
})

.on("click", "#js-save-edit", function(e){
    e.preventDefault();
    const profile_image = $("#upload_profile_image").prop("files")[0];
    const cover_image = $("#upload_cover_image").prop("files")[0];
    const $username = $("#username");
    const $first_name = $("#first_name");
    const $last_name = $("#last_name");
    const $email = $("#email");
    const formData = new FormData();
    formData.append("image", profile_image)
    formData.append("cover_image", cover_image)
    if ($username.val()){formData.append("username", $username.val().trim())}
    if ($first_name.val()){formData.append("first_name", $first_name.val().trim())}
    if ($last_name.val()){formData.append("last_name", $last_name.val().trim())}
    if ($email.val()){formData.append("email", $email.val().trim())}
    $(this).val("Saving....");
    
    $.ajax({
        type: "POST",
        url: $("#edit-form").data("url"),
        data: formData,
        processData: false,  // Prevent jQuery from processing data
        contentType: false,  // Prevent jQuery from setting content type

        success: (data) => {
             // Check if the response contains a redirect URL
            if (data && data.redirect) {
                // Perform the redirect
                window.location.href = data.redirect;
            } else {
                $last_name.val("");
                $first_name.val("");
                $("#error-text").text("Success!! click on profile link to see changes")        
            }
        },

        error: (error) => {
            console.warn(error.responseText)
            if (error.responseJSON){
                $("#error-text").text(error.responseJSON.error)
                $(this).val("Save");

            }else {
                $("#error-text").text(error.statusText)  
                $(this).prop("disabled", true)
                $(this).css("background-color", "red")
            }
        }   
    })

})

.on("click", ".js-sidenav-toggle", function(e){
    // console.log("clicked")
    $(".sidenav-modal").removeClass("hidden")
})

.on("click", ".hidenav", function(e){
    $(".sidenav-modal").addClass("hidden")
})

.on("click", "#js-toggle-mode", function(e){
    $("body").toggleClass("dark")
    localStorage.setItem("darkMode", $("body").hasClass("dark"))
})

.on("click", ".post-detail", function(e){
    const link = $(this).data("show")
    if (link){
        window.location.href = $(this).data("url")
    }
})



$(window).on("scroll", function(e){
    // const scrollPosition = window.scrollY;
    // window.innerWidth
    const scrollPosition = $(document).scrollTop()
    const $navigate = $("#navigate-top")

    if (scrollPosition > 900 && $(window).width() > 760){
        $($navigate).css("display", "block")
    }else {
        $($navigate).css("display", "none")
    }
})






function previewImage(input, previewTargetId) {
    const $preview = $(previewTargetId);

    if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
            $preview.attr("src", e.target.result);
            $preview.css("display", "block"); // Show the image preview
        };
        
        reader.readAsDataURL(input.files[0]);
    } else {
        $preview.attr("src", "#");
        $preview.css("display", "none");
    }
}
