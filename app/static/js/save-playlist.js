$(document).ready(function () {
    $("#savePlaylistButton").click(function () {
        var newPlaylistName = $("#playlistNameField").val();
        var playlistContentJson = JSON.parse({{ playlist_content.to_json() | tojson }});
        var playlistTracks = playlistContentJson["tracks"];
        var playlistDataToPost = JSON.stringify({ "name": newPlaylistName, "tracks": playlistTracks });
        console.log("Creating playlist '" + newPlaylistName + "'");

        $.ajax({
            url: "/playlist",
            type: "post",
            contentType: "application/json",
            data: playlistDataToPost,
            success: function (response) {
                console.log("Successfully created playlist '" + newPlaylistName + "'");
                document.getElementById("messageLabel").value = "Saved!";
                location.reload();
            },
            error: function (xhr) {
                console.log("Error occurred creating playlist '" + newPlaylistName + "'");
            }
        });
    });
});
