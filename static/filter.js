window.onload = function set_display_cookie()
{
    // Init data
    var date = new Date();
    date.setTime(date.getTime() + (60*60*1000)); //Expires in an hour
    var expires = "expires=" + date.toUTCString();
    document.cookie = 'display=display=';

    // Add all spell names
    var display = document.getElementById('spell_window').children;
    for (var i=0; i < display.length; ++i)
    {
        if (display[i].tagName == 'DIV')
        {
            document.cookie += display[i].getAttribute('name') + ',';
        }
    }
    document.cookie += ';';

    // Remember form
    /*
    var form = document.getElementById('inquiry').children;
    for (var i=0; i < form.length; ++i)
    {
        if (form[i].tagName == 'INPUT' || form[i].tagName == 'SELECT')
        {
            if( form[i].checked )
            {
                document.cookie += form[i].getAttribute('name') + ';';
            }
        }
    }
    */

    // Add experation date
    document.cookie += ';' + expires;
}

$('#radio_name').change(function () {
	// make value search invisible
	$('div[name=value_search]').toggleClass("visible_block invisible_block");
	// make name search visible
	$('div[name=name_search]').toggleClass("invisible_block visible_block");
})

$('#radio_value').change(function () {
	// make name search invisible
	$('div[name=name_search]').toggleClass("visible_block invisible_block");
	// make value search visible
	$('div[name=value_search]').toggleClass("visible_block invisible_block");
})
