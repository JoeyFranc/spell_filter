window.onload = function set_display_cookie()
{
    // Init data
    var date = new Date();
    date.setTime(date.getTime() + (60*60*1000)); //Expires in an hour
    var expires = "expires=" + date.toUTCString();
    document.cookie = 'display=';
    document.cookie += 'display='

    // Add all spell names
    var display = document.getElementById('spell_window').children;
    for (var i=0; i < display.length; ++i)
    {
        document.cookie += display[i].tagname + ',';
    }

    // Add experation date
    document.cookie += ';' + expires;
}
